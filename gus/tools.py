import os
import re
import asyncio
import logging
import base64
from datetime import datetime, timezone, timedelta
import httpx
from duckduckgo_search import DDGS
from gus.memory import (
    buscar_memorias_detalhada,
    salvar_observacao_gus,
    buscar_memorias_gus,
    deletar_memoria as _deletar_memoria,
)
from gus.integrations.railway import logs_railway as _logs_railway
from gus.integrations.diagnostico import auto_diagnostico as _auto_diagnostico
from gus.integrations.wikilinks import sugerir_wikilinks as _sugerir_wikilinks
from gus.integrations.pesquisa import (
    pesquisar_pubmed as _pesquisar_pubmed,
    pesquisar_arxiv as _pesquisar_arxiv,
)
from gus.integrations.openai_chat import perguntar_gpt as _perguntar_gpt
# Padrões de dados sensíveis — fonte única em gus/patterns_sensiveis.py (R7).
# Mesma lista é usada pelo hook PreToolUse em .claude/hooks/scan_sensivel.py.
from gus.patterns_sensiveis import PATTERNS_SENSIVEIS as _PATTERNS_SENSIVEIS

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

# Caracteres permitidos em nomes de arquivo e pastas.
# Ponto permitido pra pastas hidden legítimas (.github/, .claude/, .env.example).
# Traversal (..) bloqueado explicitamente em _validar_path.
_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9\-_./]+$")


def _validar_path(path: str) -> str:
    """Valida path contra traversal e caracteres perigosos."""
    path = path.strip().lstrip("/")
    if ".." in path:
        raise ValueError(f"Path inválido (traversal): {path}")
    if not _SAFE_PATH_RE.match(path.replace(".md", "")):
        raise ValueError(f"Path contém caracteres não permitidos: {path}")
    return path


def _escanear_sensivel(content: str) -> list[str]:
    """Retorna lista dos tipos de dados sensíveis encontrados no texto."""
    encontrados = []
    for nome, padrao in _PATTERNS_SENSIVEIS.items():
        if padrao.search(content):
            encontrados.append(nome)
    return encontrados

TOOLS = [
    {
        "name": "read_from_github",
        "description": (
            "Lê o conteúdo de um arquivo Markdown do repositório do Gustavo no GitHub. "
            "Use quando precisar de contexto específico de um projeto, histórico de saúde, "
            "exames anteriores, decisões passadas, ou qualquer informação estruturada salva. "
            "Exemplos de paths: 'pessoal/saude/historico-saude.md', "
            "'phronesis-bench/semantico/phronesis-00-briefing.md', 'capturado/insight-x.md'. "
            "Por default lê do branch main. Para ler de outro branch (ex: branch de "
            "desenvolvimento, rascunho ainda não merged), passe `branch`."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho completo do arquivo no repositório, incluindo extensão (ex: 'pessoal/saude/historico-saude.md')"
                },
                "branch": {
                    "type": "string",
                    "description": "Nome do branch (ex: 'claude/get-patient-health-data-5rXVB'). Omita pra ler do main."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_github_directory",
        "description": (
            "Lista o conteúdo (arquivos e subpastas) de uma pasta do repositório do Gustavo "
            "no GitHub. Use ANTES de chutar paths — quando o usuário perguntar o que existe "
            "em uma área, ou quando você não tem certeza se um arquivo específico existe. "
            "Retorna nomes de arquivos e pastas. Para listar a raiz do repo, passe path vazio "
            "ou '.'. Por default lista do branch main; passe `branch` pra outro."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho da pasta no repositório (ex: 'pessoal/saude', 'projetos/gus'). Vazio ou '.' para a raiz."
                },
                "branch": {
                    "type": "string",
                    "description": "Nome do branch. Omita pra listar do main."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_branches",
        "description": (
            "Lista todas as branches existentes no repositório (com indicador de qual é a "
            "default — main). Use ANTES de tentar ler de uma branch específica quando o "
            "Gustavo mencionar trabalho em andamento, rascunho, ou pedir pra ver 'em qual "
            "branch tá o X'. Cada branch retorna nome + commit SHA curto + autor do último "
            "commit + data. Não recebe input."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "list_commits",
        "description": (
            "Lista commits recentes do repositório. Use quando o usuário perguntar sobre "
            "histórico, o que mudou, quando foi editado, quem modificou — qualquer coisa "
            "temporal ou de autoria. Pode filtrar por path (pasta ou arquivo) e por janela "
            "de dias. Retorna hash curto, data em horário de Brasília, autor e mensagem de "
            "cada commit."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path do arquivo ou pasta pra filtrar. Ex: 'projetos/gus', 'pessoal/saude/historico-saude.md'. Vazio pra commits do repo inteiro."
                },
                "limit": {
                    "type": "integer",
                    "description": "Quantidade máxima de commits a retornar (1 a 30). Default 10."
                },
                "since_days": {
                    "type": "integer",
                    "description": "Filtrar só commits dos últimos N dias. 0 ou omitido pra sem filtro temporal."
                }
            },
            "required": []
        }
    },
    {
        "name": "search_memory",
        "description": (
            "Busca memórias do Gustavo no Hub Qdrant (gus_hub) de forma ativa (por query "
            "específica). Mem0 SaaS é fallback se Hub falhar. Use quando o usuário perguntar "
            "sobre memórias recentes, ou quando você precisar de contexto adicional além do "
            "que já foi injetado passivamente no início da conversa. Retorna as memórias "
            "mais semanticamente próximas da query, com [tipo/area] visível."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Busca em linguagem natural (ex: 'projetos ativos', 'saúde recente', 'decisões sobre o Gus', 'construção da casa')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de memórias a retornar (1 a 20). Default 10."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_web",
        "description": (
            "Busca informações atuais na web. Use quando não tiver certeza sobre fatos recentes, "
            "eventos atuais, preços, notícias, dados técnicos ou qualquer coisa que precise de "
            "fonte externa para confirmar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termos de busca em português ou inglês"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "pesquisar_pubmed",
        "description": (
            "Busca artigos no PubMed (NCBI) — base mundial de literatura biomédica. "
            "Use pra dúvidas clínicas, anestesia, medicina interna, qualquer coisa que "
            "demande evidência científica revisada por pares. Retorna até `max_n` "
            "resultados com título, autores, journal, ano e link DOI/PMID. Sem custo "
            "(API NCBI grátis)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termos de busca (ex: 'sevoflurane pediatric MRI', 'phronesis bench medical AI')."
                },
                "max_n": {
                    "type": "integer",
                    "description": "Máximo de resultados (1 a 20). Default 10."
                },
                "since_year": {
                    "type": "integer",
                    "description": "Filtra só artigos a partir desse ano (ex: 2020)."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "pesquisar_arxiv",
        "description": (
            "Busca preprints no arXiv — repositório de artigos em IA, ML, física, "
            "matemática, etc. Use pra papers em IA (relevante pro Phronesis-Bench, MGE, "
            "TER, Axon). Categorias úteis: 'cs.AI' (IA geral), 'cs.CL' (NLP), 'cs.LG' "
            "(Machine Learning), 'cs.HC' (interação humano-computador), 'q-bio.NC' "
            "(neurociência computacional). Sem custo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termos de busca (ex: 'LLM metacognition', 'wisdom benchmark', 'neurodivergent reasoning')."
                },
                "max_n": {
                    "type": "integer",
                    "description": "Máximo de resultados (1 a 20). Default 10."
                },
                "categoria": {
                    "type": "string",
                    "description": "Filtro de categoria arXiv (ex: 'cs.AI', 'cs.LG'). Omita pra buscar em todas."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "perguntar_gpt",
        "description": (
            "Pergunta ao GPT-5 (OpenAI) pra obter segunda opinião divergente. "
            "USE quando: decisão ambígua onde vale ouvir família de modelo diferente "
            "do Claude (vieses distintos), ou quando o Gustavo pedir explicitamente "
            "'pergunta pro GPT'. NÃO USE pra: busca/fato atual (use search_web), "
            "literatura científica (use pesquisar_pubmed/arxiv), brainstorm criativo "
            "(faz sozinho). Custo médio-alto, use com moderação. Default modelo "
            "`gpt-5-mini` (barato e rápido); use `gpt-5` (caro) só pra decisões "
            "críticas; `gpt-5-nano` pra coisas triviais."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Pergunta + contexto necessário, em string única. Inclua o que Sonnet já pensou pra GPT poder divergir com base."
                },
                "modelo": {
                    "type": "string",
                    "enum": ["gpt-5", "gpt-5-mini", "gpt-5-nano"],
                    "description": "Default 'gpt-5-mini'. Use 'gpt-5' só pra decisões críticas (caro)."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "disparar_workflow",
        "description": (
            "Dispara manualmente um GitHub Action via workflow_dispatch. Use quando o "
            "Gustavo pedir pra rodar algo agora sem esperar o cron. Só funciona pra "
            "workflows que têm `workflow_dispatch:` no trigger (todos os 8 workflows "
            "atuais têm). Requer GITHUB_TOKEN com escopo 'Actions: Write'. "
            "Workflows disponíveis: `auditoria-mem0.yml`, `briefing-matinal.yml`, "
            "`check-saude.yml`, `export-mem0.yml`, `reflexao-quinzenal.yml`, "
            "`retrospectiva-semanal.yml`, `sync-to-drive.yml`, `sync-to-drive-full.yml`."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "workflow_name": {
                    "type": "string",
                    "description": "Nome do arquivo do workflow (ex: 'meta-memoria.yml', 'briefing-matinal.yml'). Deve terminar em .yml ou .yaml."
                },
                "branch": {
                    "type": "string",
                    "description": "Branch pra executar. Default 'main'."
                }
            },
            "required": ["workflow_name"]
        }
    },
    {
        "name": "sugerir_wikilinks",
        "description": (
            "Lê um arquivo .md do repo e sugere wikilinks pra outros arquivos relacionados, "
            "via Sonnet. Não modifica o arquivo — só retorna sugestões pro Gustavo aprovar. "
            "Use quando o Gustavo perguntar 'que arquivos têm a ver com X?', 'sugere conexões "
            "pra esse MD', ou após salvar um arquivo novo querendo conectar ao grafo do "
            "Obsidian. Output: lista numerada com [[wikilinks]] + motivo de cada um, mais "
            "lista dos já presentes (preservados). Custo ~$0.017 por chamada (Sonnet, não "
            "Haiku — qualidade da conexão importa mais que economia)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "arquivo": {
                    "type": "string",
                    "description": "Path do arquivo no repo (ex: 'dimagem/dia/2026-04-25.md', 'pessoal/saude/historico-saude.md'). Pode omitir extensão .md."
                },
                "branch": {
                    "type": "string",
                    "description": "Nome do branch. Omita pra ler do main."
                }
            },
            "required": ["arquivo"]
        }
    },
    {
        "name": "auto_diagnostico",
        "description": (
            "Roda health check paralelo em todos os componentes externos do Gus: "
            "GitHub PAT, Hub Qdrant (com frescor do fragmento mais recente), Anthropic API, "
            "Tavily, volume Railway (/app/data writable), workflows GH (últimos 5 runs). "
            "Retorna tabela markdown com ✅/⚠️/❌. Use quando o Gustavo perguntar "
            "'tá tudo funcionando?', 'que está quebrado?', 'roda o /check', ou quando "
            "você suspeitar que algo travou silenciosamente. Sem inputs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "logs_railway",
        "description": (
            "Puxa logs recentes do bot Gus rodando em produção no Railway. Use quando o "
            "Gustavo perguntar sobre erros, comportamento estranho, se algum salvamento no "
            "Hub Qdrant ou GitHub falhou silenciosamente, ou quando precisar auditar a "
            "operação do bot. Filtra por substring (case-insensitive) na mensagem e por "
            "janela temporal em minutos. Requer Railway_diagnostic configurado nas "
            "Variables do Railway."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "linhas": {
                    "type": "integer",
                    "description": "Máximo de logs a retornar (1-500). Default 50."
                },
                "filtro": {
                    "type": "string",
                    "description": "Substring pra filtrar mensagens. Ex: 'curador', 'Hub', 'error', 'salvar', 'dimagem'."
                },
                "since_min": {
                    "type": "integer",
                    "description": "Só logs dos últimos N minutos. Ex: 60 = última hora, 1440 = últimas 24h."
                }
            },
            "required": []
        }
    },
    {
        "name": "meta_memoria",
        "description": (
            "Retorna a META-MEMÓRIA DO GUS — o auto-conhecimento do próprio agente sobre "
            "si mesmo (quem é, como evolui, o que aprendeu sobre si, limitações conscientes, "
            "reflexões). Use quando o Gustavo perguntar sobre o Gus enquanto entidade, "
            "identidade do bot, capacidades com nuances, aprendizados. Não confundir "
            "com `auditoria_mem0()` (stats das memórias sobre o Gustavo). Dados vêm de "
            "`gus/meta-memoria.md`."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "salvar_memoria_gus",
        "description": (
            "Salva uma observação no SEU PRÓPRIO brain no Hub Qdrant (user_id='gus', "
            "separado das memórias sobre o Gustavo). Use quando perceber: "
            "(a) um padrão operacional sobre o Gustavo que afeta como você deve agir, "
            "(b) um aprendizado tático sobre você mesmo (caveat de tool, comportamento), "
            "(c) um princípio que emergiu da conversa e vale lembrar. "
            "NÃO usar pra fatos sobre o Gustavo — esses ficam no brain user_id='gustavo' "
            "automaticamente via curador híbrido a cada 3 turnos."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "observacao": {
                    "type": "string",
                    "description": "Observação curta e direta. Ex: 'Gustavo prefere crítica sem suavizar', 'Verificar antes de afirmar ausência'."
                }
            },
            "required": ["observacao"]
        }
    },
    {
        "name": "buscar_memoria_gus",
        "description": (
            "Busca nas SUAS PRÓPRIAS memórias no Hub Qdrant (user_id='gus'). Brain separado "
            "do brain do Gustavo. Use pra recuperar padrões operacionais, aprendizados sobre "
            "si, princípios que você acumulou. NÃO traz fatos sobre o Gustavo — pra isso use "
            "search_memory."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query semântica (ex: 'como devo agir', 'padrões observados', 'princípios')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de memórias (1 a 20). Default 10."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "deletar_memoria",
        "description": (
            "DELETA uma memória pelo ID (Hub Qdrant primário, Mem0 fallback pra IDs "
            "históricos pré-migração). AÇÃO IRREVERSÍVEL — não dá pra desfazer. "
            "Use SOMENTE após o Gustavo confirmar explicitamente qual memória deletar. "
            "Fluxo obrigatório: (1) `search_memory(query)` retorna memórias com IDs no "
            "formato `[id] [tipo/area] texto`; (2) você mostra ao Gustavo e PERGUNTA qual "
            "deletar; (3) só após resposta clara dele (ex: 'deleta a 2', 'pode apagar a "
            "do workflow'), você chama `deletar_memoria(memory_id=...)` com o ID exato. "
            "NUNCA chame essa tool sem confirmação explícita. NUNCA chame em loop sem "
            "perguntar entre cada uma. Se houver dúvida sobre qual ID, pergunte."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "memory_id": {
                    "type": "string",
                    "description": "ID exato da memória (UUID retornado por search_memory entre colchetes)."
                },
                "user_id": {
                    "type": "string",
                    "description": "Brain alvo: 'gustavo' (default) ou 'gus' (auto-observações). Use 'gustavo' a menos que o Gustavo peça especificamente pra apagar do brain do Gus."
                }
            },
            "required": ["memory_id"]
        }
    },
    {
        "name": "auditoria_mem0",
        "description": (
            "Retorna a auditoria do armazém de memórias — estatísticas do Hub Qdrant "
            "SOBRE O GUSTAVO (quantas, por área, frescor, duplicatas suspeitas, gaps). "
            "Use quando o Gustavo perguntar sobre o estado das memórias dele, do que tem "
            "registrado, se há duplicatas, onde tem gap. Não confundir com `meta_memoria()` "
            "(auto-conhecimento do Gus). Dados vêm de `_indices/_auditoria-mem0.md` "
            "atualizado diariamente pelo cron (nome legado, mas o conteúdo já é do Hub)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "criar_acao",
        "description": (
            "Enfileira uma ação pra ser executada no mundo real (mandar WhatsApp, email, "
            "criar evento no calendário, lembrete). Salva em 'acoes/pendentes/<id>.md' "
            "com frontmatter estruturado. Use quando o usuário pede pra FAZER ALGO (não só "
            "registrar informação — pra isso use save_to_github). Executor que processa a "
            "fila ainda não existe, então ações ficam em pendentes esperando implementação."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "tipo": {
                    "type": "string",
                    "description": "Tipo da ação: whatsapp, email, calendar, lembrete, nota",
                    "enum": ["whatsapp", "email", "calendar", "lembrete", "nota"]
                },
                "conteudo": {
                    "type": "string",
                    "description": "Corpo do MD descrevendo a ação. Deve ter seções '## Ação' (detalhes) e '## Contexto' (por que). Formato YAML ou texto, conforme o tipo."
                },
                "alto_risco": {
                    "type": "boolean",
                    "description": "true se envolve valor monetário, destinatário novo/desconhecido, palavra-gatilho (urgente, emergência), ou ação irreversível. Ações alto_risco pausam em pendentes aguardando confirmação explícita."
                }
            },
            "required": ["tipo", "conteudo"]
        }
    },
    {
        "name": "save_to_github",
        "description": (
            "Salva conteúdo como arquivo Markdown no repositório do Gustavo no GitHub. "
            "Use quando o usuário pedir explicitamente pra salvar, quando houver um insight "
            "importante que mereça ser preservado, ou após analisar um documento relevante."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nome do arquivo sem extensão (ex: 'exame-jan-2026', 'insight-phronesis')"
                },
                "content": {
                    "type": "string",
                    "description": "Conteúdo completo do arquivo em Markdown"
                },
                "folder": {
                    "type": "string",
                    "description": (
                        "Pasta no repositório. Use a mais específica possível: "
                        "'pessoal/saude' para exames/consultas/medicamentos, "
                        "'pessoal/financeiro' para extratos/notas, "
                        "'pessoal/diario' para reflexões pessoais, "
                        "'pessoal/paty-dos-alferes' para o projeto da casa, "
                        "'esportes/treinos' para treinos individuais (e atualizar 'esportes/evolucao.md'), "
                        "'leituras/livros' ou 'leituras/papers' para anotações de leitura, "
                        "'contatos' para mapa de relacionamentos não-sensível "
                        "(dados sensíveis de terceiros vão em 'sensivel/contatos'), "
                        "'familia' para registros sobre família, "
                        "'dimagem/casos' para casos clínicos didáticos com pseudônimo, "
                        "'dimagem/protocolos' para protocolos clínicos, "
                        "'dimagem/admin' para gestão da clínica, "
                        "'receitas/doces' ou 'receitas/salgadas' para receitas, "
                        "'phronesis-bench' / 'mge' / 'ter' / 'axon' para projetos específicos, "
                        "'capturado/links' para artigos/posts da web, "
                        "'capturado/ideias' para insights soltos, "
                        "'capturado/misc' para tudo sem categoria clara, "
                        "'capturado/visual' para capturas visuais. "
                        "PII/credenciais sempre em 'sensivel/<subpasta>' (não sincroniza pro Drive)."
                    )
                }
            },
            "required": ["filename", "content", "folder"]
        }
    },
    {
        "name": "rotear_arquivo",
        "description": (
            "Roteia um arquivo de dialogos/inbox-tiogu/ (ou outra inbox) pro destino "
            "correto no repo. Use APÓS o Gustavo confirmar explicitamente o roteamento "
            "no Telegram (ex: 'pode rotear', 'manda pra X', 'append em Y'). "
            "3 ações: "
            "(a) 'criar_novo' = cria arquivo NOVO em destino_path (file completo .md). "
            "Ex: ideia → 'capturado/ideias/<tema>.md'. Falha se já existe. "
            "(b) 'append' = anexa o corpo do source no fim do destino_path existente, "
            "com separador (heading com data BRT). Ex: resumo de chat → "
            "'pessoal/diario/2026-04.md'. Falha se destino não existe. "
            "(c) 'mover' = copia source completo (preservando frontmatter de demanda) "
            "pra <destino_dir>/<nome>. destino_path deve ser DIRETÓRIO (sem .md). "
            "Ex: caso clínico → 'dimagem/casos'. "
            "Após qualquer ação: source é marcado status: concluido + ## Resultado, "
            "e workflow archive-completed-demandas move pra archive/ em ≤15min. "
            "Recusa se source já estiver concluído (idempotência). "
            "Recusa se conteúdo tem dados sensíveis fora de sensivel/."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": (
                        "Path completo no repo do arquivo a rotear, relativo à raiz. "
                        "Ex: 'dialogos/inbox-tiogu/2026-04-27T22-30__reflexao.md'. "
                        "Precisa estar em uma das inboxes (dialogos/inbox-*/)."
                    )
                },
                "destino_path": {
                    "type": "string",
                    "description": (
                        "Path do destino. Pra acao=criar_novo/append: file completo "
                        "terminando em .md (ex: 'pessoal/diario/2026-04.md'). "
                        "Pra acao=mover: diretório sem .md (ex: 'dimagem/casos')."
                    )
                },
                "acao": {
                    "type": "string",
                    "description": "Uma de: 'criar_novo' | 'append' | 'mover'.",
                    "enum": ["criar_novo", "append", "mover"]
                }
            },
            "required": ["source_path", "destino_path", "acao"]
        }
    }
]


async def _read_from_github(path: str, branch: str | None = None) -> str:
    try:
        path = _validar_path(path)
    except ValueError as e:
        return str(e)

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {"ref": branch} if branch else None

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 404:
        ref_msg = f" (branch={branch})" if branch else ""
        return f"Arquivo não encontrado: `{path}`{ref_msg}"
    if response.status_code != 200:
        return f"Erro ao ler do GitHub: {response.status_code}"

    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


async def _list_github_directory(path: str, branch: str | None = None) -> str:
    """Lista arquivos e pastas de um diretório no repositório GitHub."""
    path = (path or "").strip().strip("/")
    if path and path != ".":
        try:
            path = _validar_path(path)
        except ValueError as e:
            return str(e)
    else:
        path = ""

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {"ref": branch} if branch else None

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 404:
        ref_msg = f" (branch={branch})" if branch else ""
        return f"Pasta não encontrada: `{path or '.'}`{ref_msg}"
    if response.status_code != 200:
        return f"Erro ao listar GitHub: {response.status_code}"

    items = response.json()
    if not isinstance(items, list):
        return f"`{path}` é um arquivo, não uma pasta. Use read_from_github pra ler."

    pastas = sorted([i["name"] for i in items if i["type"] == "dir"])
    arquivos = sorted([i["name"] for i in items if i["type"] == "file"])

    branch_label = f" @ `{branch}`" if branch else ""
    linhas = [f"Conteúdo de `{path or '(raiz)'}`{branch_label}:"]
    if pastas:
        linhas.append("\n**Pastas:**")
        linhas.extend(f"- {p}/" for p in pastas)
    if arquivos:
        linhas.append("\n**Arquivos:**")
        linhas.extend(f"- {a}" for a in arquivos)
    if not pastas and not arquivos:
        linhas.append("(vazio)")
    return "\n".join(linhas)


async def _list_branches() -> str:
    """Lista todas as branches do repositório com info do último commit."""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url_branches = f"https://api.github.com/repos/{repo}/branches"
    url_repo = f"https://api.github.com/repos/{repo}"

    async with httpx.AsyncClient(timeout=30) as client:
        resp_b, resp_r = await asyncio.gather(
            client.get(url_branches, headers=headers, params={"per_page": 100}),
            client.get(url_repo, headers=headers),
        )

    if resp_b.status_code != 200:
        return f"Erro ao listar branches: {resp_b.status_code}"

    default_branch = "main"
    if resp_r.status_code == 200:
        default_branch = resp_r.json().get("default_branch", "main")

    branches = resp_b.json()
    if not branches:
        return "Nenhuma branch encontrada."

    # Pra cada branch, busca info do último commit em paralelo
    async def _commit_info(branch_name: str) -> dict:
        url_commit = f"https://api.github.com/repos/{repo}/commits/{branch_name}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url_commit, headers=headers)
        if r.status_code != 200:
            return {"branch": branch_name, "sha": "?", "autor": "?", "data": "?", "msg": "(erro)"}
        d = r.json()
        autor = d.get("commit", {}).get("author", {})
        return {
            "branch": branch_name,
            "sha": d.get("sha", "")[:7],
            "autor": autor.get("name", "?"),
            "data": (autor.get("date") or "")[:10],
            "msg": (d.get("commit", {}).get("message") or "").splitlines()[0][:60],
        }

    infos = await asyncio.gather(
        *(_commit_info(b["name"]) for b in branches),
        return_exceptions=True,
    )

    linhas = [f"**{len(branches)} branches** (default: `{default_branch}`)\n"]
    for info in infos:
        if isinstance(info, Exception):
            continue
        marker = " ⭐" if info["branch"] == default_branch else ""
        linhas.append(
            f"- `{info['branch']}`{marker} — {info['sha']} · "
            f"{info['data']} · {info['autor']} · {info['msg']}"
        )
    return "\n".join(linhas)


async def _list_commits(path: str = "", limit: int = 10, since_days: int = 0) -> str:
    """Lista commits recentes, opcionalmente filtrados por path e período."""
    path = (path or "").strip().strip("/")
    if path and path != ".":
        try:
            path = _validar_path(path)
        except ValueError as e:
            return str(e)
    else:
        path = ""

    try:
        limit = max(1, min(int(limit), 30))
    except (TypeError, ValueError):
        limit = 10

    try:
        since_days = int(since_days) if since_days else 0
    except (TypeError, ValueError):
        since_days = 0

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    params: dict = {"per_page": limit}
    if path:
        params["path"] = path
    if since_days > 0:
        since_dt = datetime.now(BRT) - timedelta(days=since_days)
        params["since"] = since_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params, headers=headers)

    if response.status_code == 404:
        return f"Path não encontrado no repo: `{path}`" if path else "Repositório não encontrado."
    if response.status_code != 200:
        return f"Erro ao listar commits: {response.status_code}"

    commits = response.json()
    if not commits:
        contexto = []
        if path:
            contexto.append(f"em `{path}`")
        if since_days:
            contexto.append(f"nos últimos {since_days} dia(s)")
        return f"Nenhum commit encontrado {' '.join(contexto)}.".strip()

    cabecalho = "Últimos "
    if path and since_days:
        cabecalho = f"Commits em `{path}` nos últimos {since_days} dia(s):"
    elif path:
        cabecalho = f"Últimos {len(commits)} commits em `{path}`:"
    elif since_days:
        cabecalho = f"Commits dos últimos {since_days} dia(s):"
    else:
        cabecalho = f"Últimos {len(commits)} commits do repositório:"

    linhas = [cabecalho]
    for c in commits:
        sha_curto = c.get("sha", "")[:7]
        commit = c.get("commit", {})
        mensagem = commit.get("message", "").split("\n")[0]
        autor = commit.get("author", {}).get("name", "?")
        data_iso = commit.get("author", {}).get("date", "")
        try:
            dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
            data_fmt = dt_utc.astimezone(BRT).strftime("%Y-%m-%d %H:%M")
        except Exception:
            data_fmt = data_iso[:16]
        linhas.append(f"- `{sha_curto}` {data_fmt} — {autor} — {mensagem}")

    return "\n".join(linhas)


async def _search_tavily(query: str) -> str | None:
    """Busca via Tavily API. Retorna string formatada ou None se falhar."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": 5,
        "search_depth": "basic",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
        if response.status_code != 200:
            logger.warning(f"Tavily retornou {response.status_code}: {response.text[:200]}")
            return None
        results = response.json().get("results", [])
    except Exception as e:
        logger.warning(f"Tavily falhou: {e}")
        return None

    if not results:
        return None

    lines = [f"**{r['title']}**\n{r['content']}\nFonte: {r['url']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_ddg(query: str) -> str:
    """Fallback: busca via DuckDuckGo."""
    def _run():
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    try:
        results = await asyncio.to_thread(_run)
    except Exception as e:
        logger.error(f"Falha na busca web (DDG): {e}")
        return f"Erro na busca: {e}"

    if not results:
        return "Nenhum resultado encontrado."

    lines = [f"**{r['title']}**\n{r['body']}\nFonte: {r['href']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_web(query: str) -> str:
    """Tenta Tavily primeiro; se falhar ou sem chave, cai pro DuckDuckGo."""
    tavily_result = await _search_tavily(query)
    if tavily_result:
        return tavily_result
    return await _search_ddg(query)


async def _save_to_github(filename: str, content: str, folder: str, via: str = "telegram") -> str:
    if "/" in filename or ".." in filename:
        return f"Nome de arquivo inválido: {filename}"

    try:
        folder = _validar_path(folder)
    except ValueError as e:
        return str(e)

    # Scan de dados sensíveis — só alerta se path NÃO for sensivel/*
    if not folder.startswith("sensivel"):
        flags = _escanear_sensivel(content)
        if flags:
            return (
                f"ATENÇÃO — dados sensíveis detectados: {', '.join(flags)}.\n"
                f"Este conteúdo NÃO foi salvo. Pergunte ao Gustavo como prosseguir:\n"
                f"  (a) salvar em 'sensivel/{folder}/' ou subpasta de 'sensivel/' (não espelha no Drive)\n"
                f"  (b) forçar o save no path original '{folder}/' mesmo com dados sensíveis\n"
                f"  (c) cancelar\n"
                f"Se (a) ou (b), chamar save_to_github de novo com o folder ajustado. "
                f"Se vier nova confirmação explícita, pode salvar."
            )

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado. Adicione a variável no Railway."

    path = f"{folder}/{filename}.md"

    now = datetime.now(BRT)
    frontmatter = (
        f"---\n"
        f"capturado_em: {now.strftime('%Y-%m-%dT%H:%M:%S')}\n"
        f"via: {via}\n"
        f"---\n\n"
    )
    if not content.startswith("---\n"):
        content = frontmatter + content

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    encoded = base64.b64encode(content.encode()).decode()

    async with httpx.AsyncClient(timeout=30) as client:
        # Verifica se arquivo já existe (pega sha para update)
        sha = None
        check = await client.get(url, headers=headers)
        if check.status_code == 200:
            sha = check.json().get("sha")

        payload = {
            "message": f"capture: {filename} via Gus",
            "content": encoded,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        response = await client.put(url, json=payload, headers=headers)

    if response.status_code in (200, 201):
        action = "Atualizado" if sha else "Salvo"
        return f"{action} em `{path}` no repositório."
    else:
        logger.error(f"GitHub API error: {response.status_code} {response.text[:300]}")
        return f"Erro ao salvar no GitHub: {response.status_code}"


async def _disparar_workflow(workflow_name: str, branch: str = "main") -> str:
    """Dispara um workflow via GitHub Actions API (workflow_dispatch)."""
    if not re.match(r"^[a-z0-9\-]+\.ya?ml$", workflow_name):
        return f"Nome inválido: `{workflow_name}`. Use formato tipo 'meta-memoria.yml'."

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_name}/dispatches"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {"ref": branch or "main"}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
    except Exception as e:
        return f"Erro de rede ao disparar workflow: {e}"

    if response.status_code == 204:
        return (
            f"Workflow `{workflow_name}` disparado em branch `{branch}`. "
            f"Acompanhe em https://github.com/{repo}/actions."
        )
    if response.status_code == 404:
        return (
            f"Workflow `{workflow_name}` não encontrado. Confirme o nome em "
            f"`.github/workflows/` via list_github_directory."
        )
    if response.status_code == 403:
        return (
            f"Sem permissão pra disparar workflow (HTTP 403). "
            f"O GITHUB_TOKEN precisa de escopo 'Actions: Read and write'. "
            f"Gustavo atualiza em github.com/settings/tokens editando o PAT existente."
        )
    if response.status_code == 422:
        return (
            f"GitHub rejeitou o dispatch (422). Normalmente significa que o workflow "
            f"não tem `workflow_dispatch:` no trigger, ou o branch `{branch}` não existe."
        )
    return f"Erro inesperado {response.status_code}: {response.text[:200]}"


async def _criar_acao(tipo: str, conteudo: str, alto_risco: bool = False) -> str:
    """Enfileira uma ação em acoes/pendentes/<id>.md com frontmatter YAML padrão."""
    import uuid
    agora = datetime.now(BRT)
    acao_id = f"{agora.strftime('%Y-%m-%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"

    frontmatter = (
        f"---\n"
        f"id: {acao_id}\n"
        f"tipo: {tipo}\n"
        f"origem: telegram\n"
        f"criado_em: {agora.isoformat()}\n"
        f"status: pendente\n"
        f"alto_risco: {str(bool(alto_risco)).lower()}\n"
        f"---\n\n"
    )

    full_content = frontmatter + conteudo.strip() + "\n"

    # Salva direto sem scan — o frontmatter acima é sempre adicionado pela tool.
    # Usa save_to_github internamente, mas bypassa o scan passando conteúdo já em
    # acoes/pendentes/ que deve ter pasta sensivel/ se envolver dados privados.
    return await _save_to_github(acao_id, full_content, "acoes/pendentes")


async def executar_tool(name: str, inputs: dict) -> str:
    if name == "read_from_github":
        return await _read_from_github(inputs["path"], inputs.get("branch"))
    elif name == "list_github_directory":
        return await _list_github_directory(inputs.get("path", ""), inputs.get("branch"))
    elif name == "list_branches":
        return await _list_branches()
    elif name == "list_commits":
        return await _list_commits(
            inputs.get("path", ""),
            inputs.get("limit", 10),
            inputs.get("since_days", 0)
        )
    elif name == "search_memory":
        try:
            limit = max(1, min(int(inputs.get("limit", 10)), 20))
        except (TypeError, ValueError):
            limit = 10
        return await buscar_memorias_detalhada(inputs["query"], limit)
    elif name == "search_web":
        return await _search_web(inputs["query"])
    elif name == "pesquisar_pubmed":
        return await _pesquisar_pubmed(
            inputs["query"],
            inputs.get("max_n", 10),
            inputs.get("since_year"),
        )
    elif name == "pesquisar_arxiv":
        return await _pesquisar_arxiv(
            inputs["query"],
            inputs.get("max_n", 10),
            inputs.get("categoria"),
        )
    elif name == "perguntar_gpt":
        return await _perguntar_gpt(
            inputs["query"],
            inputs.get("modelo", "gpt-5-mini"),
        )
    elif name == "save_to_github":
        return await _save_to_github(
            inputs["filename"],
            inputs["content"],
            inputs.get("folder", "capturado")
        )
    elif name == "criar_acao":
        return await _criar_acao(
            inputs["tipo"],
            inputs["conteudo"],
            bool(inputs.get("alto_risco", False))
        )
    elif name == "meta_memoria":
        return await _read_from_github("gus/meta-memoria.md")
    elif name == "auditoria_mem0":
        return await _read_from_github("_indices/_auditoria-mem0.md")
    elif name == "salvar_memoria_gus":
        return await salvar_observacao_gus(inputs["observacao"])
    elif name == "buscar_memoria_gus":
        try:
            limit = max(1, min(int(inputs.get("limit", 10)), 20))
        except (TypeError, ValueError):
            limit = 10
        return await buscar_memorias_gus(inputs["query"], limit)
    elif name == "deletar_memoria":
        return await _deletar_memoria(
            inputs["memory_id"],
            inputs.get("user_id", "gustavo"),
        )
    elif name == "disparar_workflow":
        return await _disparar_workflow(
            inputs["workflow_name"],
            inputs.get("branch", "main")
        )
    elif name == "logs_railway":
        return await _logs_railway(
            inputs.get("linhas", 50),
            inputs.get("filtro"),
            inputs.get("since_min"),
        )
    elif name == "auto_diagnostico":
        return await _auto_diagnostico()
    elif name == "sugerir_wikilinks":
        return await _sugerir_wikilinks(
            inputs["arquivo"],
            inputs.get("branch"),
        )
    elif name == "rotear_arquivo":
        from gus.roteador import rotear_arquivo as _rotear
        return await _rotear(
            inputs["source_path"],
            inputs["destino_path"],
            inputs["acao"],
        )
    return f"Tool desconhecida: {name}"
