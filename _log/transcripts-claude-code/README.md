# Transcripts da porta Claude Code

Pasta processada pelo cron `curador-claude-code.yml` (a cada 30min).

## Como chega aqui

`.claude/hooks/retro_engine.py` (Stop hook) faz, ao fim de cada sessão Code:

1. Lê o transcript da sessão Claude Code
2. Aplica `gus.patterns_sensiveis.redact()` — substitui CPF/CNPJ/tokens/keys
   por marcadores `[REDACTED-<tipo>]`
3. Salva em `<timestamp>__<session-id>.jsonl` aqui
4. `git add + commit + push` direto (só se branch é `claude/*`, evita
   commits acidentais em main)

## Como sai daqui

Workflow `.github/workflows/curador-claude-code.yml` (cron 30min) roda
`.github/scripts/curador_claude_code.py`:

1. Lista `*.jsonl` (não-processados)
2. Pra cada arquivo, roda `hub.curador.curar_arquivo` 2x:
   - `user_id="gustavo"` → fatos sobre o Gustavo discutidos na sessão
   - `user_id="gus"` → autobiografia do agente, decisões arquiteturais
   Cada chamada usa Haiku + GPT-4o-mini em paralelo (curador híbrido)
3. Move arquivo pra `processados/AAAA-MM/`
4. Commit + push do cleanup

## Política PII

**Antes de salvar arquivo aqui, o hook redige tudo que `patterns_sensiveis`
detecta** (CPF/CNPJ, cartões, API keys Anthropic/OpenAI/Mem0/Qdrant/Tavily,
GitHub PAT, Telegram bot token, Google SA/OAuth, Railway token).

Repo é privado, mas redação é defesa em profundidade. Padrões novos vão
em `gus/patterns_sensiveis.py` — fonte única.

**Limitações conhecidas:**
- Nomes próprios não são redatados (regex não detecta nome de forma confiável)
- Dados clínicos do Dimagem dependem de tu não citar em sessão Code
  (essa porta é técnica, não clínica)

## Arquivos aqui

- `.gitkeep` — mantém pasta no git mesmo vazia
- `README.md` — este arquivo
- `*.jsonl` — transcripts pendentes de curadoria
- `processados/AAAA-MM/*.jsonl` — já processados pelo cron

## Origem

Demanda `dialogos/inbox-claude-code/2026-05-01-curador-bidirecional-cron.md`
(Caminho 2: cron GitHub Actions com secrets, em vez de hook tentar chamar
Hub direto sem env vars).
