---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: media
status: concluido
criado_em: 2026-05-01T00:12:00-03:00
processado_em: 2026-05-02T23:35:00-03:00
processado_por: claude-code
acao_sugerida: investigar
destino_path: hub/curador.py
contexto: "Curador hoje só processa TioGu Telegram. Conversas Claude Chat e Claude Code não viram fragmento. Decidir entre A/B/C e implementar (precisa aprovação Gustavo antes de codar)."
resolucao: |
  Opção A + C escolhida pelo Gustavo:
  - Caminho 1 (default): real-time via MCP `ingestar_fragmento` durante a conversa
  - Caminho 2 (escape): upload .md em Gus-Sync/dialogos/inbox-chat-raw/ pra
    sessões >20 turnos onde curador post-hoc agrega valor
  - Adicional: Chat também deve salvar autoreflexão sobre si-agente no
    brain `gus` (tipo=meta_reflexao | identidade_operacional | procedural)

  Implementação em `dialogos/_bootstrap/gus-bootstrap.md` (PR #81 a abrir):
  - Reescrita seção "Como você captura memória pro Hub" com 2 caminhos
  - Tabelas de tipos por brain (gustavo / gus)
  - Frequência balanceada (2-4 fragmentos/conversa típica)
  - Disciplina anti-esquecimento atualizada pra refletir 2 caminhos
  - Limpeza de referências obsoletas a Mem0 e paths renomeados (PR #77)

  Opção B (Stop hook Code expandido) NÃO implementada nesta rodada —
  curador-claude-code via cron (PR #64) já cobre Claude Code de forma
  similar. Opção C (refator agnóstico) fica pra sprint futura.
---

# Demanda — captura multiporta de conversas pro Hub

## Problema

O `hub/curador.py` roda Haiku × GPT-4o-mini em paralelo a cada 3 turnos do
Telegram, salvando fragmentos no Hub com `via=telegram-curador`. Funciona
bem pra TioGu, mas:

- **Claude Chat:** só salva fragmento se Gustavo pedir explícito
  ("salva no hub que..."). Sem captura automática.
- **Claude Code (sessões aqui):** Stop hook do retro-engine roda mas só
  extrai auto-observações no brain `user_id="gus"`, não fragmentos sobre
  Gustavo. Por isso o log mostra "Fragmentos extraídos: 0" toda hora.

**Resultado:** muito conhecimento Gustavo→Claude Chat→trabalho real fica
fora do Hub. Telegram é a única fonte de memória rica do dia-a-dia.

## Opções

### Opção A — Prompt curador no Claude Chat (rápido)

Adiciona seção em `dialogos/_bootstrap/gus-bootstrap.md` instruindo Claude
Chat a chamar `ingestar_fragmento` quando ele detectar decisão / preferência /
fato relevante durante a conversa.

- **Trabalho:** ~30 linhas no bootstrap + teste em conversa nova
- **Pró:** zero código novo, usa MCP que já existe
- **Contra:** qualidade depende do prompt — pode salvar lixo ou ignorar coisa
  importante. Sem comparação Haiku × GPT como o curador Telegram tem.

### Opção B — Stop hook Claude Code expandido (médio)

O Stop hook do retro-engine já roda no fim de cada sessão Claude Code.
Estender pra também rodar `hub.curador.curar_arquivo()` no transcript
da sessão.

- **Trabalho:** ~50 linhas no script do hook
- **Pró:** mesma lógica do curador Telegram (Haiku × GPT em paralelo,
  consistência), salva com `via=claude-code-curador`
- **Contra:** roda só no fim — perde captura em tempo real. Identificar
  trecho relevante do transcript não é trivial (transcripts longos).

### Opção C — Curador agnóstico de porta (caro/ideal)

Refatora `curar_arquivo` pra aceitar qualquer fonte de texto. Cria adapter
por porta:
- `hub/adapters/telegram.py` (existe parcial)
- `hub/adapters/claude_chat.py` (novo — endpoint `/hub/claude-chat-context`?)
- `hub/adapters/claude_code.py` (novo — Stop hook)

Mesma pipeline, mesma comparação Haiku × GPT-4o-mini, mesmo schema gus-18.

- **Trabalho:** ~1 dia + migração do que já existe
- **Pró:** zero divergência entre portas, escalável pra Custom GPT / Alexa
  no futuro
- **Contra:** sprint dedicado, não dá pra fazer em 30min

## Critério de decisão

Antes de codar, conversa com Gustavo sobre:

1. **Volume esperado:** quantas conversas Claude Chat / Code por semana ele
   tem? Se baixo → A é suficiente; se alto → B ou C valem o investimento.
2. **Tolerância a duplicação:** se A e B coexistirem e Claude Chat também
   tiver Stop hook simulado, vai duplicar fragmentos. Tolerável?
3. **Sprint disponível:** C exige 1 dia full. Vale agora ou espera?

## Recomendação inicial

**A pra ontem** (cobre Claude Chat hoje, baixíssimo custo) +
**B em paralelo** (cobre Claude Code, reusa lógica curador) +
**C quando tiver sprint dedicado** (idealiza arquitetura sem pressão).

Mas Gustavo decide. **NÃO implementa sem confirmação.**

## Onde olhar

- `hub/curador.py` — implementação atual
- `gus/llm.py` — dispatcher Anthropic / OpenAI
- `dialogos/_bootstrap/gus-bootstrap.md` — onde Opção A entraria
- `_log/retro-engine-claude-code/` — onde Opção B integraria
- Hook config: `.claude/hooks/` ou similar (verificar onde o Stop hook tá
  registrado hoje)

## Resultado esperado

Uma das 3:
1. Markdown novo `gus-31-captura-multiporta.md` com decisão A/B/C +
   implementação pequena se A.
2. PR implementando a opção escolhida.
3. "Adiada — Gustavo prefere esperar X" registrada nesta demanda como
   `status: cancelado` com justificativa.
