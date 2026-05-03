---
tipo: inventario-auto
area: gus
atualizado: 2026-05-03 05:47 BRT
fonte: gus/tools.py:TOOLS (geração automática — não editar)
---

# Tools do TioGu — inventário auto-gerado

> **NÃO EDITAR.** Este arquivo é regenerado pelo workflow
> `sync-docs.yml` a partir de `gus/tools.py:TOOLS`. Pra mudar uma
> descrição, edite o `description` no array de tools no código.
>
> Doc curado (status, decisões, sprint) está em
> `projetos/gus/gus-11-tools-roadmap.md`.

**Total de tools ativas:** 21

| # | Nome | Descrição |
|---|---|---|
| 1 | `read_from_github` | Lê o conteúdo de um arquivo Markdown do repositório do Gustavo no GitHub. |
| 2 | `list_github_directory` | Lista o conteúdo (arquivos e subpastas) de uma pasta do repositório do Gustavo no GitHub. |
| 3 | `list_branches` | Lista todas as branches existentes no repositório (com indicador de qual é a default — main). |
| 4 | `list_commits` | Lista commits recentes do repositório. |
| 5 | `search_memory` | Busca memórias do Gustavo no Hub Qdrant (gus_hub) de forma ativa (por query específica). |
| 6 | `search_web` | Busca informações atuais na web. |
| 7 | `pesquisar_pubmed` | Busca artigos no PubMed (NCBI) — base mundial de literatura biomédica. |
| 8 | `pesquisar_arxiv` | Busca preprints no arXiv — repositório de artigos em IA, ML, física, matemática, etc. |
| 9 | `perguntar_gpt` | Pergunta ao GPT-5 (OpenAI) pra obter segunda opinião divergente. |
| 10 | `disparar_workflow` | Dispara manualmente um GitHub Action via workflow_dispatch. |
| 11 | `sugerir_wikilinks` | Lê um arquivo . |
| 12 | `auto_diagnostico` | Roda health check paralelo em todos os componentes externos do Gus: GitHub PAT, Hub Qdrant (com frescor do fragmento mais recente), Anthropic API, Tavily, volume Railway (/app/data writable), workflow… |
| 13 | `logs_railway` | Puxa logs recentes do bot Gus rodando em produção no Railway. |
| 14 | `meta_memoria` | Retorna a META-MEMÓRIA DO GUS — o auto-conhecimento do próprio agente sobre si mesmo (quem é, como evolui, o que aprendeu sobre si, limitações conscientes, reflexões). |
| 15 | `salvar_memoria_gus` | Salva uma observação no SEU PRÓPRIO brain no Hub Qdrant (user_id='gus', separado das memórias sobre o Gustavo). |
| 16 | `buscar_memoria_gus` | Busca nas SUAS PRÓPRIAS memórias no Hub Qdrant (user_id='gus'). |
| 17 | `deletar_memoria` | DELETA uma memória pelo ID (Hub Qdrant primário, Mem0 fallback pra IDs históricos pré-migração). |
| 18 | `auditoria_hub` | Retorna a auditoria do armazém de memórias — estatísticas do Hub Qdrant SOBRE O GUSTAVO (quantas, por área, frescor, duplicatas suspeitas, gaps). |
| 19 | `criar_acao` | Enfileira uma ação pra ser executada no mundo real (mandar WhatsApp, email, criar evento no calendário, lembrete). |
| 20 | `save_to_github` | Salva conteúdo como arquivo Markdown no repositório do Gustavo no GitHub. |
| 21 | `rotear_arquivo` | Roteia um arquivo de dialogos/inbox-tiogu/ (ou outra inbox) pro destino correto no repo. |

## Schemas completos

Schema de input de cada tool (parâmetros aceitos):

### `read_from_github`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `path` | string | ✓ | Caminho completo do arquivo no repositório, incluindo extensão (ex: 'pessoal/saude/historico-saude.md') |
| `branch` | string | — | Nome do branch (ex: 'claude/get-patient-health-data-5rXVB'). Omita pra ler do main. |

### `list_github_directory`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `path` | string | ✓ | Caminho da pasta no repositório (ex: 'pessoal/saude', 'projetos/gus'). Vazio ou '.' para a raiz. |
| `branch` | string | — | Nome do branch. Omita pra listar do main. |

### `list_branches`

_Sem parâmetros._

### `list_commits`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `path` | string | — | Path do arquivo ou pasta pra filtrar. Ex: 'projetos/gus', 'pessoal/saude/historico-saude.md'. Vazio pra commits do repo inteiro. |
| `limit` | integer | — | Quantidade máxima de commits a retornar (1 a 30). Default 10. |
| `since_days` | integer | — | Filtrar só commits dos últimos N dias. 0 ou omitido pra sem filtro temporal. |

### `search_memory`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Busca em linguagem natural (ex: 'projetos ativos', 'saúde recente', 'decisões sobre o Gus', 'construção da casa') |
| `limit` | integer | — | Número máximo de memórias a retornar (1 a 20). Default 10. |

### `search_web`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Termos de busca em português ou inglês |

### `pesquisar_pubmed`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Termos de busca (ex: 'sevoflurane pediatric MRI', 'phronesis bench medical AI'). |
| `max_n` | integer | — | Máximo de resultados (1 a 20). Default 10. |
| `since_year` | integer | — | Filtra só artigos a partir desse ano (ex: 2020). |

### `pesquisar_arxiv`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Termos de busca (ex: 'LLM metacognition', 'wisdom benchmark', 'neurodivergent reasoning'). |
| `max_n` | integer | — | Máximo de resultados (1 a 20). Default 10. |
| `categoria` | string | — | Filtro de categoria arXiv (ex: 'cs.AI', 'cs.LG'). Omita pra buscar em todas. |

### `perguntar_gpt`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Pergunta + contexto necessário, em string única. Inclua o que Sonnet já pensou pra GPT poder divergir com base. |
| `modelo` | string | — | Default 'gpt-5-mini'. Use 'gpt-5' só pra decisões críticas (caro). |

### `disparar_workflow`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `workflow_name` | string | ✓ | Nome do arquivo do workflow (ex: 'meta-memoria.yml', 'briefing-matinal.yml'). Deve terminar em .yml ou .yaml. |
| `branch` | string | — | Branch pra executar. Default 'main'. |

### `sugerir_wikilinks`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `arquivo` | string | ✓ | Path do arquivo no repo (ex: 'dimagem/dia/2026-04-25.md', 'pessoal/saude/historico-saude.md'). Pode omitir extensão .md. |
| `branch` | string | — | Nome do branch. Omita pra ler do main. |

### `auto_diagnostico`

_Sem parâmetros._

### `logs_railway`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `linhas` | integer | — | Máximo de logs a retornar (1-500). Default 50. |
| `filtro` | string | — | Substring pra filtrar mensagens. Ex: 'curador', 'Hub', 'error', 'salvar', 'dimagem'. |
| `since_min` | integer | — | Só logs dos últimos N minutos. Ex: 60 = última hora, 1440 = últimas 24h. |

### `meta_memoria`

_Sem parâmetros._

### `salvar_memoria_gus`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `observacao` | string | ✓ | Observação curta e direta. Ex: 'Gustavo prefere crítica sem suavizar', 'Verificar antes de afirmar ausência'. |

### `buscar_memoria_gus`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `query` | string | ✓ | Query semântica (ex: 'como devo agir', 'padrões observados', 'princípios') |
| `limit` | integer | — | Número máximo de memórias (1 a 20). Default 10. |

### `deletar_memoria`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `memory_id` | string | ✓ | ID exato da memória (UUID retornado por search_memory entre colchetes). |
| `user_id` | string | — | Brain alvo: 'gustavo' (default) ou 'gus' (auto-observações). Use 'gustavo' a menos que o Gustavo peça especificamente pra apagar do brain do Gus. |

### `auditoria_hub`

_Sem parâmetros._

### `criar_acao`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `tipo` | string | ✓ | Tipo da ação: whatsapp, email, calendar, lembrete, nota |
| `conteudo` | string | ✓ | Corpo do MD descrevendo a ação. Deve ter seções '## Ação' (detalhes) e '## Contexto' (por que). Formato YAML ou texto, conforme o tipo. |
| `alto_risco` | boolean | — | true se envolve valor monetário, destinatário novo/desconhecido, palavra-gatilho (urgente, emergência), ou ação irreversível. Ações alto_risco pausam … |

### `save_to_github`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `filename` | string | ✓ | Nome do arquivo sem extensão (ex: 'exame-jan-2026', 'insight-phronesis') |
| `content` | string | ✓ | Conteúdo completo do arquivo em Markdown |
| `folder` | string | ✓ | Pasta no repositório. Use a mais específica possível: 'pessoal/saude' para exames/consultas/medicamentos, 'pessoal/financeiro' para extratos/notas, 'p… |

### `rotear_arquivo`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `source_path` | string | ✓ | Path completo no repo do arquivo a rotear, relativo à raiz. Ex: 'dialogos/inbox-tiogu/2026-04-27T22-30__reflexao.md'. Precisa estar em uma das inboxes… |
| `destino_path` | string | ✓ | Path do destino. Pra acao=criar_novo/append: file completo terminando em .md (ex: 'pessoal/diario/2026-04.md'). Pra acao=mover: diretório sem .md (ex:… |
| `acao` | string | ✓ | Uma de: 'criar_novo' \| 'append' \| 'mover'. |

---

_Auto-gerado em 2026-05-03 05:47 BRT por `.github/scripts/gerar_lista_tools.py`._
