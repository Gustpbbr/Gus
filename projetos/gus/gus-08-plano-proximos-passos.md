---
tipo: documentacao-projeto
projeto: gus
parte: 8-plano-proximos-passos
atualizado: 2026-04-24
---

# Gus — Plano dos próximos passos (Níveis 2 e 3, execução local)

Lista curada do que dá pra fazer **só com código** (sem depender de serviços externos como Google Cloud, AWS, OpenAI Whisper, Alexa Developer Account). Cada item é autônomo — pode ser implementado sozinho ou em combo. Ordem por valor × esforço.

## Visão geral rápida

| ID  | Item                              | Esforço | Depende de ação externa? |
|-----|-----------------------------------|---------|--------------------------|
| A   | Rate limiting no bot              | 15min   | Não                      |
| B   | Backup Mem0 em JSON               | 10min   | Não                      |
| C   | Briefing matinal automático       | 30min   | 3 secrets no GitHub      |
| D   | Retrospectiva semanal automática  | 30min   | Mesmos secrets do C      |
| E   | Relatório de custos agregado      | 15min   | Volume Railway (ideal)   |
| F   | Esqueleto da fila de ações        | 30min   | Não                      |
| G   | Atualizar `_estado-atual.md`      | 5min    | Não                      |
| H   | Guia prático de uso diário        | 15min   | Não                      |

## Combos recomendados

- **(C)+(D)+(E)** — automações proativas. ~80min. Transforma bot de reativo pra antecipatório.
- **(A)+(B)+(G)** — defensiva + doc atualizada. ~30min. Baixo risco, valor consistente.
- **(F)** isolado — fundação de Nível 4 mesmo antes de executores externos.
- **(H)** isolado — qualidade de vida pro Gustavo quando esquecer o que o bot sabe fazer.

---

## A) Rate limiting no bot

**Problema:** hoje, se alguém (ou um loop) disparar mensagens em série, o bot responde tudo até bater `HARD_LIMIT_USD_MONTH`. Custa antes de proteger.

**Solução:** contar mensagens por janela de 60s por chat_id. Se passar do limite, responder amigavelmente.

**Passos:**
1. Em `gus/bot.py`, adicionar:
   ```python
   from collections import deque
   message_timestamps: dict[str, deque] = {}
   RATE_LIMIT = int(os.getenv("RATE_LIMIT_MSG_PER_MINUTE", "20"))
   ```
2. Modificar `_verificar_limite(update)` pra também verificar timestamps:
   - Obter `deque` do chat_id atual, criar se não existir
   - Remover timestamps mais velhos que 60s
   - Se `len(deque) >= RATE_LIMIT`, responder `"Tô recebendo muito rápido. Aguenta 1min."` e retornar False
   - Senão, append `time.time()` e retornar True
3. Syntax check local (`ast.parse`)
4. Commit + merge pra `main` + push → Railway redeploya

**Esforço:** 15min. **Risco:** zero (state em memória, reseta em redeploy).
**Teste:** manda 25 mensagens rápidas no bot, última deve ser recusada.

## B) Backup Mem0 em JSON estruturado

**Problema:** o export diário é `.md` legível mas perde metadata (IDs, timestamps precisos). Se precisar restaurar Mem0, não dá pra re-importar clean.

**Solução:** gerar `.json` completo junto com o `.md`.

**Passos:**
1. Em `.github/scripts/export_mem0.py`, após escrever `.md`:
   ```python
   OUTPUT_JSON = "gus-memoria-export.json"
   with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
       json.dump(memories, f, ensure_ascii=False, indent=2, default=str)
   ```
2. Em `.github/workflows/export-mem0.yml`, ajustar:
   ```yaml
   git add gus-memoria-export.md gus-memoria-export.json
   ```
3. Commit + merge + push → próxima execução cron (3h BRT) já exporta ambos

**Esforço:** 10min. **Risco:** zero.
**Teste:** `workflow_dispatch` manual, confirmar que ambos os arquivos aparecem em `main`.

## C) Briefing matinal automático

**Problema:** Gus é reativo. Um bom agente antecipa.

**Solução:** GitHub Action cron 7h BRT em dias úteis. Lê Mem0 + commits + índices, gera 3-5 linhas via Claude Haiku, posta no Telegram via Bot API direta (não depende do bot estar em polling).

**Passos:**

1. **Criar script** `.github/scripts/briefing_matinal.py`:
   - Importa `mem0ai`, `anthropic`, `httpx`
   - Carrega env: `MEM0_API_KEY`, `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GITHUB_TOKEN`
   - Queries:
     - `client.search` no Mem0 com queries tipo "pendências", "próximos passos"
     - GitHub commits últimas 24h (`list_commits(since_days=1)`)
     - Data do dia + compromissos do calendário (se tool existir futuramente)
   - Prompt pro Claude Haiku:
     ```
     Gere briefing matinal de 3-5 linhas pro Gustavo.
     Tom: português informal, direto, sem formatação.
     Inclua: o que tá em aberto, o que foi feito ontem, 1 sugestão pro dia.
     Contexto: <memórias + commits>
     ```
   - `httpx.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": briefing})`

2. **Criar workflow** `.github/workflows/briefing-matinal.yml`:
   ```yaml
   name: Briefing matinal
   on:
     schedule:
       - cron: '0 10 * * 1-5'   # 7h BRT segunda-sexta
     workflow_dispatch:
   jobs:
     briefing:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         - run: pip install mem0ai==0.1.29 anthropic==0.40.0 httpx==0.27.0
         - env:
             MEM0_API_KEY: ${{ secrets.MEM0_API_KEY }}
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
             TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
             TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           run: python .github/scripts/briefing_matinal.py
   ```

3. **Secrets novos no GitHub** (ação tua, 1min):
   - `TELEGRAM_BOT_TOKEN` — token do Tiogubot
   - `TELEGRAM_CHAT_ID` — `495256549`
   - `ANTHROPIC_API_KEY` — mesma do Railway

4. Commit + merge + push
5. Testar via `workflow_dispatch` manual na aba Actions
6. Confirmar mensagem chegou no Telegram

**Esforço:** 30min dev + 1min tua ação nos secrets.
**Riscos:** dependência de 3 APIs externas simultâneas. Se Anthropic tiver overload no horário, briefing não sai (silencioso).
**Mitigação futura:** retry no script igual ao que já tem em `llm.py`.

## D) Retrospectiva semanal automática

**Problema:** perder visão do que foi feito na semana. Gustavo tende a abrir muitas frentes e esquecer o progresso.

**Solução:** toda sexta 20h BRT, gera um MD estruturado com resumo da semana, commita em `pessoal/diario/semana-AAAA-WW.md`.

**Passos:**

1. **Criar script** `.github/scripts/retrospectiva_semanal.py`:
   - Coleta de dados (últimos 7 dias):
     - Memórias adicionadas no Mem0 (via `client.get_all` filtrando por `created_at`)
     - Commits (`list_commits(since_days=7)`)
     - Índices modificados em `_indices/` (via comparação git)
     - Novos arquivos criados (git log --diff-filter=A)
   - Prompt pro Claude Sonnet (este merece qualidade):
     ```
     Você recebe um dump de atividade da última semana do Gustavo.
     Gere um MD estruturado em português BR:
     
     ## Resumo executivo (3 linhas)
     ## Atividades por área (projetos, saúde, dimagem, capturado)
     ## Decisões tomadas
     ## Pendências identificadas
     ## Próxima semana — 1-2 sugestões
     
     Seja específico, use wikilinks pra arquivos mencionados.
     ```
   - Escreve em `pessoal/diario/semana-{YYYY-WW}.md` (cria pasta se não existir)
   - Opcional: post no Telegram com o link + 2 linhas de resumo

2. **Criar workflow** `.github/workflows/retrospectiva-semanal.yml`:
   ```yaml
   name: Retrospectiva semanal
   on:
     schedule:
       - cron: '0 23 * * 5'   # sexta 20h BRT
     workflow_dispatch:
   jobs:
     retrospectiva:
       runs-on: ubuntu-latest
       permissions:
         contents: write
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0   # precisamos de histórico pro git log
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         - run: pip install mem0ai==0.1.29 anthropic==0.40.0 httpx==0.27.0
         - env: <...mesmo bloco do briefing...>
           run: python .github/scripts/retrospectiva_semanal.py
         - name: Commit
           run: |
             git config user.name "gus-bot"
             git config user.email "gus-bot@users.noreply.github.com"
             git add pessoal/diario/
             git diff --staged --quiet || git commit -m "auto: retrospectiva semana $(date +%Y-%W)"
             git push
   ```

3. Reutiliza os 3 secrets do (C). Sem ação tua adicional.

4. Commit + merge + push
5. Testar via `workflow_dispatch`

**Esforço:** 30min dev.
**Valor:** altíssimo — transforma dispersão crônica em visão cronológica revisável.

## E) Relatório de custos agregado

**Problema:** hoje custo mensal tá em `logs/gus_metrics.jsonl` dentro do container Railway. Em redeploy, perde tudo. `HARD_LIMIT_USD_MONTH` pode ser burlado sem querer.

**Solução simples agora (sem volume Railway):**

1. Adicionar comando `/custo` em `bot.py`:
   ```python
   async def handle_custo(update, context):
       if not _autorizado(str(update.effective_chat.id)):
           return
       total = custo_mes_atual()
       await update.message.reply_text(
           f"Custo do mês atual: US${total:.4f} de US${HARD_LIMIT:.2f} "
           f"({100*total/HARD_LIMIT:.1f}%)\n\n"
           f"Observação: reseta em cada redeploy. Pra histórico preciso "
           f"precisa volume Railway persistente."
       )
   ```
2. Registrar handler em `main.py`: `app.add_handler(CommandHandler("custo", handle_custo))`
3. Commit + merge + push

**Solução completa (requer volume Railway):**

4. Railway → Services → Gus → Settings → **Volumes** → New Volume → mount path `/app/logs` → 1GB
5. Redeploy. Logs persistem.
6. Opcional futuro: script cron interno no bot que gera `_indices/custos-AAAA-MM.md` toda 2ª feira.

**Esforço:** 15min comando + 5min tua ação no Railway pro volume.

## F) Esqueleto da fila de ações

**Objetivo:** preparar arquitetura pra Nível 4. Ações ficam em pendentes, sem executor ainda (Twilio, Gmail entram depois).

**Passos:**

1. **Criar estrutura:**
   - `acoes/README.md` — regras, tipos (whatsapp, email, calendar, lembrete, nota), formato do frontmatter
   - `acoes/pendentes/.gitkeep`
   - `acoes/concluidas/.gitkeep`
   - `acoes/lembretes-ativos.md` — placeholder com explicação

2. **Nova tool em `gus/tools.py`**:
   ```python
   async def _criar_acao(tipo: str, conteudo: str, alto_risco: bool = False) -> str:
       import uuid
       from datetime import datetime
       agora = datetime.now(BRT)
       acao_id = f"{agora.strftime('%Y-%m-%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"
       frontmatter = (
           f"---\n"
           f"id: {acao_id}\n"
           f"tipo: {tipo}\n"
           f"origem: telegram\n"
           f"criado_em: {agora.isoformat()}\n"
           f"status: pendente\n"
           f"alto_risco: {str(alto_risco).lower()}\n"
           f"---\n\n"
       )
       full = frontmatter + conteudo
       return await _save_to_github(acao_id, full, "acoes/pendentes")
   ```
   Adicionar em `TOOLS` e `executar_tool`.

3. **Atualizar `system_prompt.md`**:
   - Seção nova: "Ações vs notas"
   - Criar ação: quando Gustavo pede pra **fazer algo no mundo real** (mandar msg, agendar, lembrar)
   - Criar nota (`save_to_github`): quando só precisa registrar informação
   - Ação alto_risco=true: valor monetário, destinatário novo, palavra-gatilho

4. Commit + merge + push

**Esforço:** 30min.
**Bloqueio futuro:** executor (Twilio, Gmail, Calendar) é trabalho à parte. Por enquanto ações ficam em pendentes esperando implementação.

## G) Atualizar `_estado-atual.md`

**Passos:**

1. Read atual
2. Seção "Última sessão": adicionar bullets pós-08h:
   - `search_memory` tool criada (commit `009d25b` → rebase `f69f71b`)
   - Retry exponencial + fallback Haiku (commit `0e964e0`)
   - Fix Haiku alias (commit `d89c7c1`)
   - Fluxo bot validado em produção (6/6 testes passaram)
3. "Pendências pra próxima sessão": atualizar pra refletir o que está em aberto
4. Commit + push

**Esforço:** 5min.

## H) Guia prático de uso diário

**Passos:**

1. Criar `projetos/gus/gus-08-guia-uso-diario.md` com seções:
   - **Captura rápida**: "como salvar um exame", "como registrar uma ideia", "como transcrever PDF"
   - **Consultas**: "me lembra de X", "o que tu sabe sobre Y", "busca na web Z"
   - **Histórico**: "o que mudou essa semana", "última edição em A", "últimos commits em B"
   - **Dados sensíveis**: "quando o scan aparece", "como forçar", "pasta `sensivel/`"
   - **Troubleshooting**: "API sobrecarregada", "bot silenciou", "memória estranha"
2. Commit + push

**Esforço:** 15min.

---

## Plano de execução recomendado

Se fosse fazer tudo num dia:

1. **G** (5min) — atualiza doc primeiro pra próxima sessão pegar o fio
2. **A** (15min) — rate limiting como reforço base
3. **B** (10min) — backup JSON rápido
4. **H** (15min) — guia de uso enquanto memória fresca
5. **F** (30min) — fila de ações preparando Nível 4
6. **C** (30min) — briefing matinal (primeiro item com ação tua)
7. **D** (30min) — retrospectiva aproveita secrets do C
8. **E** (15min) — comando `/custo` rápido; volume Railway é decisão à parte

**Total:** ~2h30 de código + ~10min de tua ação (3 secrets + opcionalmente volume).

Se escolher só um combo, a recomendação forte é **(G)+(A)+(B)+(H)** — 45min total, zero dependência externa, deixa o sistema mais robusto e auto-documentado antes do próximo avanço.

---

## Decisões pendentes (não abordadas aqui)

Ficam pra outro dia:
- Drive sync (bloqueio Google Cloud — WIF ou desligar policy)
- Custom GPT no ChatGPT (Fase 3, porta de voz mobile)
- Whisper áudio (pré-requisito: OpenAI key nova)
- Google Calendar (pré-requisito: Service Account + scopes)
- Alexa Skill (Nível 5, muito trabalho pesado em AWS)

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-04-seguranca-protecao]], [[gus-05-portas-capacidades]], [[gus-06-autonomia-acoes]], [[_estado-atual]]
