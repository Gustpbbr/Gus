---
tipo: estado-atual-sessao
atualizado: 2026-04-27T21:30-03:00
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-27 — sessão maratona Claude Code on the web)

Resolução de **5 demandas do inbox** + **R2/R6/R7 da auditoria fiscal** +
**bug 400 do curador** + **finalização da migração Mem0 → Hub Qdrant**.
Sessão deixou inbox vazio pela primeira vez. Detalhes em commits da branch
`claude/fix-curador-mem0-cleanup` (ainda aberta com R5 em andamento).

### Resumo executivo do dia

**ADR-001 Fase 3 + 4 + bugfixes** entraram em produção em 4 PRs sequenciais:

- **PR #8** (mergeado 20:27 BRT): R6 (MCP Claude Code → Hub) + R7 (patterns
  sensíveis fonte única) + #4 do inbox (gate confiança OCR Dimagem) + R2
  (5 scripts cron migram pra Hub) + fix tools TioGu (3 funções leem Hub)
- **PR #9** (mergeado ~20:50 BRT): cherry-pick fix curador 400 +
  finalização memory.py (salvar/deletar Hub-first) + bloco-âncora no
  system_prompt explicando migração
- **PR #10** (em andamento — branch `claude/fix-curador-mem0-cleanup`):
  cleanup R2 leftovers (rename `_check_mem0` → `_check_hub`, check-saude.yml
  pra Hub, mensagem desatualizada bot.py) + R5 documentação (CLAUDE.md,
  system_prompt limpeza completa, gus-15/gus-23 atualizados, este arquivo)

### Bugs críticos resolvidos

1. **Curador erro 400 'temperature and top_p'** — Hub estava vazio o dia
   inteiro porque o curador errava 100% das chamadas. Causa: `system=""`
   passado pro SDK Anthropic em chamadas Sonnet 4.6 sem tools ativava
   defaults conflitantes. Fix: prompt template vai como `system_prompt`
   (canônico) + helper `_chamar_claude_com_retry` só inclui `system` se
   truthy. Validado pós-merge: `auto_diagnostico` mostra `Hub Qdrant ✅
   2+ frags, mais recente há 0.0h`.

2. **TioGu reportando "Mem0 silêncio 25h"** — auto_diagnostico lia da
   coleção morta. Fix: `_check_mem0` (renomeado pra `_check_hub`) lê do
   Hub via `hub.store.listar`. `buscar_memorias_detalhada` e
   `buscar_memorias_gus` migrados pra Hub-first também.

3. **OCR Dimagem com nome trocado em prontuário** — risco clínico real.
   Fix: schema do Haiku Vision ganhou `confianca` (alta/media/baixa).
   `analisar_os_dimagem` bloqueia preview e pede reenvio se baixa,
   adiciona ⚠️ se média.

### Demandas resolvidas (inbox-claude-code → archive)

| # | Demanda | Resolução |
|---|---|---|
| 1 | fix-qdrant-search-bug | Já estava concluída, só faltava arquivar |
| 2 | curadoria-mem0-sonnet-nao-haiku | Superada pelo curador híbrido (Haiku × Sonnet em paralelo, não troca-fixa) |
| 3 | schema-hub-qdrant-salvar-memoria | Resolvida pela Fase 2/3/R6 (schema gus-18 completo em todas as portas) |
| 4 | ocr-confianca-baixa-nao-salvar | Implementado neste mesmo dia (gate de confiança) |
| 5 | configurar-railway-api-token | Gustavo configurou `Railway_diagnostic` no Railway |

### Configurações operacionais feitas

- `Railway_diagnostic` token configurado no Railway → `logs_railway` ativo
- Workflow `Migrar gus → gus_hub` disparado (Hub recebendo dados)
- Secrets `QDRANT_URL`/`QDRANT_API_KEY` confirmados no GitHub
- Curador híbrido salvando — Hub tem 2+ fragmentos com mais recente há minutos

### Bot agora em ~21 tools (mesma lista, mas backend Hub)

Mesmas tools de antes, internamente apontando pro Hub Qdrant. `search_memory`,
`buscar_memoria_gus`, `salvar_memoria_gus`, `deletar_memoria` lêem/escrevem
no Hub primeiro com fallback Mem0 só pra leitura (escrita Mem0 morta).

## Pendente pra próxima sessão

### Prioridade 1 — Decisão modelo curador (Fase 5 ADR-001)

- **14 dias de coleta dual** Haiku × Sonnet rolando até **12/05/2026**
- Logs em `_log/resumos-mem0/AAAA-MM-DD.md` com 1 entrada por curador
  + mesmo `hash_janela` pra parear
- Após coleta: comparar par-a-par no Obsidian, escolher modelo final
- Implica também: aposentar Mem0 SaaS totalmente (remover fallbacks no
  `gus/memory.py`, remover `MEM0_API_KEY` dos secrets, remover `mem0ai`
  do requirements)

### Prioridade 2 — Mergear PR #10 + Custom GPT

- **PR #10** (branch atual) — cleanup R2 leftovers + R5 documentação
- Após merge: TioGu lê novo `system_prompt` sem confusão sobre Mem0
- **Custom GPT Action** (DESKTOP obrigatório) — passo-a-passo em
  `gus-14-custom-gpt-setup.md`

### Prioridade 3 — Features pendentes

- **Suporte a vídeo no Telegram** — sem `filters.VIDEO` registrado em
  `gus/main.py`. Implementar = extrair áudio (ffmpeg → Whisper) + frames
  (Vision Sonnet)
- **Service Account Google Drive** — necessário pro sync pendente
  desde sempre
- **Termux + wake word "Gus" no S8** (pós-Alexa) — Opção B aprovada
- **Alexa Skill V1** (Dot 3, Polly, voz pura) — depois do Custom GPT

### Pendentes menores

- Workflow YAML do `enrich_mem0_export.py` — script existe, sem cron
- Observar dimagem A+B em produção 1-2 semanas, depois decidir tirar A
- Migrar `gus/memory.py:salvar_memorias` pra remover dependência mem0ai
  completamente (atualmente já escreve no Hub mas o módulo importa mem0)
- Limpar 4+ memórias poluídas via MCP local

## Decisões importantes tomadas (acumulado)

### Tomadas em 2026-04-27

- **ADR-001: aposentar Mem0** — wrapper mem0 self-hosted limita schema rico,
  Hub direto permite payload completo gus-18. Caminho:
  Fase 1 (Hub criado) → Fase 2 (curador) → Fase 3 (bot lê Hub) → Fase 4
  (migrar dados) → Fase 5 (aposentar Mem0)
- **Curador híbrido** Haiku × Sonnet em paralelo (14 dias) → coleta evidência
  pra decisão de modelo, não chuta
- **Patterns sensíveis em fonte única** (`gus/patterns_sensiveis.py`) — antes
  duplicado em `tools.py` + `scan_sensivel.py`, risco de drift. Adicionados
  5 patterns novos (Qdrant key, Telegram bot token, Google SA key, Google
  OAuth secret, Railway token env line)
- **OCR confiança gate** — schema do Haiku Vision auto-avalia confiança em
  3 níveis. Baixa bloqueia save. Risco clínico (nome trocado em prontuário)
  exige defesa em profundidade
- **Mensagem fallback de mídia atualizada** — "Áudio e vídeo em breve"
  estava desatualizada (áudio JÁ funciona desde sempre). Trocada por
  "Vídeo ainda não tem handler"

### Tomadas antes (2026-04-25 e anteriores, ainda válidas)

- **Alexa não é o destino final** — porta complementar. Conversa fluida =
  mobile (Custom GPT + Claude voice)
- **Câmera no Echo Show inviável via Skill** — caminho real é câmera IP
  separada (S8 velho com IP Webcam = R$ 0)
- **Wake word "Gus" no S8** = Termux + openWakeWord (Opção B), pós-Alexa
- **Conector GitHub nativo do ChatGPT recusado** — bypass de LGPD. Custom
  GPT acessa GitHub APENAS via Action REST nossa
- **Claude Chat tem write no Drive** — habilita loop assíncrono real
- **Canal unificado `dialogos/` por destinatário** — evita explosão N×N
- **Workflow Drive→GitHub cron 15min** — equilíbrio latência×custo
- **Auto-execução desabilitada V1** — Gustavo no loop pra revisar antes

## Bugs em aberto (não bloqueantes)

- DDG fallback ativa quando Tavily esgota cota
- 4+ memórias poluídas no brain `gustavo` aguardando limpeza manual via
  MCP (deletar_memoria)
- ~~Mem0 latência de indexação~~ — não importa mais, Hub indexa em segundos
- ~~Quota Retrieval API Mem0~~ — não importa mais, Mem0 morto

## Como usar este arquivo

1. Próxima sessão: ler PRIMEIRO, depois `gus-10-caminho-alexa.md` se for
   sessão de dev rumo à Alexa
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente" com o que
   ficou no meio
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-10-caminho-alexa]],
[[gus-11-tools-roadmap]], [[gus-12-portas-futuras]],
[[gus-13-tags-canonicas]], [[gus-15-decisao-migracao]],
[[gus-23-logica-qdrant-mem0]]
