---
tipo: roadmap
area: gus
atualizado: 2026-04-25T14:10-03:00
---

# Roadmap de Tools — Tiogubot

Inventário completo das tools propostas, status de implementação, e decisões.
**Atualizar este arquivo a cada commit que muda status de uma tool.**

## Legenda

| Símbolo | Significado |
|---|---|
| ✅ | Concluído — código no main + testado em produção |
| 🚧 | Rascunho — código no main mas inerte / não ativado / não testado |
| ⏳ | Pendente config — código pronto, falta ação do Gustavo (key, OAuth, etc.) |
| 🔵 | Em andamento — sendo trabalhado nesta sessão |
| ⚪ | Não iniciado |
| ❌ | Descartado |

---

## Status sprint a sprint (Top 7 prioritárias)

| # | Tool | Status | Observação |
|---|---|---|---|
| 1 | `logs_railway` | 🚧 | Código no main (`741380e`). Token de teste revogado. Falta: criar novo token + validar schema GraphQL com `scripts/test_railway_logs.py` no PC. |
| 2 | `auto_diagnostico` | ✅ | Testado em produção 25/04 11:23 BRT. TioGu confirmou retorno correto (Mem0 OK há 6min, workflows OK). |
| 3a | `pesquisar_pubmed` | ⚪ | Sprint 2 |
| 3b | `pesquisar_arxiv` | ⚪ | Sprint 2 |
| 4a | `enviar_email` | ⚪ | Sprint 3. Requer adicionar escopo `gmail.send` ao OAuth Google existente |
| 4b | `criar_evento_calendario` | ⚪ | Sprint 3. Mesmo OAuth do email |
| 5 | `perguntar_gemini` | ⚪ | Sprint 2. Requer `GEMINI_API_KEY` (Gustavo cria em aistudio.google.com) |
| 6 | `texto_para_voz` (ElevenLabs) | ⚪ | Sprint 3. Requer conta ElevenLabs + voice clone opcional |
| 7 | `sugerir_wikilinks(arquivo, branch?)` | ✅ | Mergeado em main `988a222`, testado em produção 25/04 12:30 BRT. Funcional. Nuance: Haiku eventualmente sugere conexão temporal (mesma data) em vez de temática. Se aparecer muito, apertar prompt em `wikilinks.py`. |

## Tools extras concluídas fora das 7 originais

| Tool | Status | Observação |
|---|---|---|
| `list_branches()` | ✅ | Testado em produção 25/04 11:23 BRT |
| `read_from_github(path, branch?)` | ✅ | Param `branch` opcional adicionado, testado |
| `list_github_directory(path, branch?)` | ✅ | Param `branch` opcional adicionado, testado |

## Outros rascunhos no main (não-tools)

| Item | Status | Observação |
|---|---|---|
| `gus/dimagem.py` (fluxo OS determinístico) | 🚧 | Rascunho refinado (`4b99df6`). NÃO ativado em `bot.py`. Snippet de integração no docstring quando Gustavo aprovar. |
| `dimagem/convenios.json` | ✅ no repo | 19 entradas. Ativa quando `dimagem.py` for ativado. |
| `.github/scripts/enrich_mem0_export.py` | 🚧 | Rascunho (`a5e086a`). Sem workflow YAML, sem teste manual. |
| `scripts/test_railway_logs.py` | ✅ pronto | Pra Gustavo rodar local quando voltar pro PC, validar schema Railway GraphQL. |

---

## Catálogo completo (organizado por categoria)

### A. Operação do próprio Gus (autodiagnóstico)

| Tool | Prioridade | Status | Notas |
|---|---|---|---|
| `logs_railway(linhas, filtro, since_min)` | ⭐⭐⭐ | 🚧 + ⏳ | Ver Top 7 #1 |
| `status_mem0()` | ⭐⭐⭐ | ⚪ | `/v1/usage` Mem0 — quotas, requests do mês |
| `consumo_anthropic()` | ⭐⭐ | ⚪ | Anthropic console API — gasto por modelo |
| `auto_diagnostico()` | ⭐⭐⭐ | ✅ | Ver Top 7 #2 |
| `editar_arquivo(path, instrucao)` | ⭐⭐ | ⚪ | Lê + Haiku edita + salva. Mais cirúrgico que `save_to_github` |
| `criar_workflow(nome, descricao)` | ⭐ | ⚪ | Gera YAML novo de GH Action |

### B. IAs externas

| Tool | API | Prioridade | Status |
|---|---|---|---|
| `perguntar_gemini(query, contexto_longo?)` | Gemini 2.x | ⭐⭐⭐ | ⚪ |
| `perguntar_gpt(query, modelo='gpt-5')` | OpenAI | ⭐⭐ | ⚪ |
| `perguntar_perplexity(query)` | Perplexity Sonar | ⭐⭐⭐ | ⚪ |
| `traduzir(texto, alvo='en')` | DeepL | ⭐⭐ | ⚪ |

### C. Pesquisa especializada

| Tool | API | Prioridade | Status |
|---|---|---|---|
| `pesquisar_pubmed(query, max_n=10)` | NCBI E-utilities (grátis) | ⭐⭐⭐ | ⚪ |
| `pesquisar_arxiv(query)` | arXiv API (grátis) | ⭐⭐⭐ | ⚪ |
| `consultar_doi(doi)` | CrossRef (grátis) | ⭐⭐ | ⚪ |
| `consultar_anvisa(medicamento)` | DataSUS/Anvisa | ⭐ | ⚪ |
| `cid10(termo)` | DataSUS | ⭐ | ⚪ |

### D. Voz e mídia (caminho pra Alexa)

| Tool | API | Prioridade | Status |
|---|---|---|---|
| `texto_para_voz(texto, voz='gus')` | ElevenLabs ou OpenAI TTS | ⭐⭐⭐ | ⚪ |
| `gerar_imagem(prompt)` | DALL-E 3 ou Replicate | ⭐⭐ | ⚪ |
| `transcrever_url_youtube(url)` | youtube-transcript-api | ⭐⭐ | ⚪ |
| `ocr_pdf_complexo(file)` | Mathpix ou Google Vision | ⭐ | ⚪ |
| `extrair_artigo(url)` | Trafilatura (lib local) | ⭐⭐ | ⚪ |

### E. Ações no mundo real

| Tool | API | Prioridade | Status |
|---|---|---|---|
| `enviar_email(para, assunto, corpo)` | Gmail API | ⭐⭐⭐ | ⚪ |
| `enviar_whatsapp(numero, mensagem)` | Twilio ou Z-API | ⭐⭐ | ⚪ |
| `criar_evento_calendario(...)` | Google Calendar | ⭐⭐⭐ | ⚪ |
| `proximos_compromissos(janela_dias=7)` | Google Calendar | ⭐⭐⭐ | ⚪ |
| `criar_lembrete(quando, texto)` | Telegram self-message | ⭐⭐ | ⚪ |
| `criar_pr(titulo, descricao, branch)` | GitHub MCP-style | ⭐⭐ | ⚪ |

### F. Memória e grafo

| Tool | Prioridade | Status |
|---|---|---|
| `editar_memoria(id, novo_texto)` | ⭐⭐ | ⚪ |
| `deletar_memoria(memory_id, user_id?)` | ⭐⭐ | ✅ |
| `fundir_memorias(id_a, id_b)` | ⭐⭐ | ⚪ |
| `criar_wikilink(arquivo_a, arquivo_b)` | ⭐⭐⭐ | ⚪ |
| `sugerir_wikilinks(arquivo, branch?)` | ⭐⭐⭐ | ✅ |
| `commitar_resumo_dia(formato='briefing')` | ⭐⭐ | ⚪ |

### G. Domínio Dimagem

| Tool | Prioridade | Status |
|---|---|---|
| `resumo_dia_dimagem(data='hoje')` | ⭐⭐⭐ | ⚪ |
| `historico_paciente(nome)` | ⭐⭐ | ⚪ |
| `dose_pediatrica(droga, peso_kg)` | ⭐⭐ | ⚪ |
| `consultar_tuss(codigo)` | ⭐ | ⚪ |

### H. Finanças

| Tool | API | Prioridade | Status |
|---|---|---|---|
| `cotacao_moeda(de, para)` | frankfurter.app | ⭐ | ⚪ |
| `cotacao_acao(ticker)` | Brapi ou Yahoo | ⭐ | ⚪ |
| `resumo_financeiro_mes()` | lê `pessoal/financeiro/extrato-*.md` | ⭐⭐ | ⚪ |

---

## Decisões — NÃO transformar em tool

| Coisa | Por que não | Status |
|---|---|---|
| Cron de tarefas recorrentes | É workflow GH Actions ou cron Railway, não tool | ❌ decidido |
| Auto-melhoria do código do bot | Risco alto, ROI baixo | ❌ decidido |
| Tools redundantes com Mem0 (`adicionar_fato`, `lembrar_de`) | Fluxo automático de resumo a cada 3 turnos já cobre | ❌ decidido |
| Chat com pessoas (`responder_no_whatsapp_da_mae`) | Privacy + moderação. Vai por `criar_acao(alto_risco)` | ❌ decidido |
| Geração de planilha/PDF de relatório | Já tem `save_to_github` em .md, Obsidian renderiza | ❌ decidido |

---

## Decisões pendentes

| Decisão | Estado |
|---|---|
| Cron diário do `auto_diagnostico` que avisa Telegram só se quebrar | ✅ implementado (`.github/workflows/check-saude.yml`, 7h30 BRT) |
| Log auditável de resumos pro Mem0 | ✅ implementado (`gus/resumo_log.py` → `_log/resumos-mem0/AAAA-MM-DD.md`) |
| Ativar `gus/dimagem.py` em `bot.py` (handler de foto) | ❓ aguarda revisão do rascunho |
| Workflow YAML do `enrich_mem0_export.py` | ❓ aguarda primeiro teste manual |
| Validação `logs_railway` schema GraphQL via PC | ⏳ aguarda Gustavo voltar ao PC |
| Modelo do `gerar_resumo_turnos` (Haiku vs Sonnet) | ✅ Haiku mantido — log auditável compensa |
| Modelo do `gus/dimagem.py` extração | ✅ Haiku mantido (decisão Gustavo 25/04) |

---

## Histórico de status

| Data | Mudança |
|---|---|
| 2026-04-25 14:10 | **MCP `mem0-gus` atualizado pra paridade com TioGu** (`.claude/mcp/mem0_server.py`): de 3 tools simples (só brain `gustavo`, sem IDs, sem delete) pra 7 tools — 3 brain `gustavo` + 3 brain `gus` + `deletar_memoria` universal. Todas retornam IDs no formato `[uuid] texto`. Próximo: Gustavo configura `~/.claude/mem0.key` pra ativar daqui. |
| 2026-04-25 13:55 | **Tool `deletar_memoria` criada** (18ª tool). Aceita `memory_id` (UUID) e `user_id` opcional (default 'gustavo'). Search_memory atualizado pra retornar IDs no formato `[uuid] texto`. Regra de confirmação obrigatória no system_prompt antes de chamar. Motivado por memória poluída do bug `meta-memoria.yml` detectada nos logs. |
| 2026-04-25 13:42 | **Bug fix**: lista de workflows na tool `disparar_workflow` estava com 6 entradas desatualizadas (incluindo `meta-memoria.yml` inexistente, sem `check-saude.yml`). Corrigido pra 8 reais. Bug introduzido quando criei `check-saude.yml` sem atualizar a lista — o TioGu memorizou a info errada e gerou primeiro 'check-saude.yml não existe'. |
| 2026-04-25 13:35 | **Token-Efficient Tool Use ativado** (`anthropic-beta: token-efficient-tools-2025-02-19`) em `gus/llm.py:_chamar_claude_com_retry`. Beta header só passado quando tools presentes. Soma ao prompt caching: schemas de tool comprimidos pelo backend Anthropic antes de cachear. |
| 2026-04-25 13:25 | **Prompt caching ativado em `gus/llm.py`**: system prompt + 17 tools com `cache_control: ephemeral`. Economia projetada ~70% no custo de input após primeira call de uma janela de 5min. Metadata agora inclui `cache_creation` e `cache_read`. Prompt do `wikilinks.py` apertado (proíbe explicitamente conexão temporal). Regra de format literal no system_prompt reforçada (não condensar mesmo com 1 sugestão, não substituir tabela por prosa). |
| 2026-04-25 12:50 | `sugerir_wikilinks`: trocado Haiku → Sonnet 4.6 (custo de errar > economia, decisão Gustavo). Token Railway de teste revogado. Cron diário `auto_diagnostico` implementado (`.github/workflows/check-saude.yml`, 7h30 BRT, alerta Telegram só se ⚠️/❌). Log auditável de resumos pro Mem0 implementado (`gus/resumo_log.py` → `_log/resumos-mem0/AAAA-MM-DD.md`). |
| 2026-04-25 12:34 | `sugerir_wikilinks`: 🚧 → ✅ (testada em produção, retorna sugestões substantivas; nuance: TioGu pode sugerir conexão temporal, prompt pode ser apertado se virar problema). Sprint 1 fechado (exceto `logs_railway` que aguarda config). |
| 2026-04-25 11:40 | `sugerir_wikilinks(arquivo, branch?)`: ⚪ → 🚧 (criada `gus/integrations/wikilinks.py`, plugada em `tools.py` como 17ª tool, aguarda merge) |
| 2026-04-25 11:13 | `auto_diagnostico` + `list_branches` + branch param: ⚪ → ✅ (mergeados em main `741380e`, testados em produção) |
| 2026-04-25 11:00 | `logs_railway`: ⚪ → 🚧 (mergeado em main `7266a65`, mas sem token válido — Gustavo expôs token de teste no chat) |
| 2026-04-25 00:30 | `enrich_mem0_export.py`, `gus/dimagem.py`: ⚪ → 🚧 (rascunhos `a5e086a` e `4b99df6`) |
| 2026-04-24 ~22:00 | Brainstorm inicial das ~40 tools, top 7 selecionadas, roteiro de implementação acordado |

---

## Como atualizar este doc

A cada vez que mudar status de uma tool:
1. Atualizar a linha na tabela respectiva
2. Atualizar a tabela "Status sprint a sprint" se for top 7
3. Adicionar entrada em "Histórico de status" com data e mudança
4. Atualizar `atualizado:` no frontmatter
5. Commit dedicado: `docs: roadmap — <tool> <status_antigo> → <status_novo>`

Relacionado: [[gus-08-plano-proximos-passos]], [[gus-10-caminho-alexa]], [[_estado-atual]]
