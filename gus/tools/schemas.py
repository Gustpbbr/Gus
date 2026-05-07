"""Schemas das tools expostas ao LLM (Anthropic format).

Cada entrada tem `name` (chave do dispatcher), `description` (vai pro
modelo) e `input_schema` (JSON Schema dos parâmetros aceitos).

Schemas são imutáveis no runtime — Anthropic faz prompt caching da lista
inteira em `_build_tools_cached`. Anchor de cache é por nome (estável),
não por posição.

Doc curado de status/sprint/decisões em `projetos/gus/gus-11-tools-roadmap.md`.
Inventário fiel auto-gerado em `projetos/gus/_tools-inventario.md` pelo
workflow `sync-docs.yml`.
"""

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
            "com `auditoria_hub()` (stats das memórias sobre o Gustavo). Dados vêm de "
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
        "name": "auditoria_hub",
        "description": (
            "Retorna a auditoria do armazém de memórias — estatísticas do Hub Qdrant "
            "SOBRE O GUSTAVO (quantas, por área, frescor, duplicatas suspeitas, gaps). "
            "Use quando o Gustavo perguntar sobre o estado das memórias dele, do que tem "
            "registrado, se há duplicatas, onde tem gap. Não confundir com `meta_memoria()` "
            "(auto-conhecimento do Gus). Dados vêm de `_indices/_auditoria-hub.md` "
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
