---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-05-02T22:36:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: investigar
destino_path: gus/bot.py + .claude/hooks/ + api/neurogus.html + .github/scripts/gerar_estado_claude_chat.py
contexto: "Continuidade cross-porta: cada porta detecta atividade recente das outras (via Hub criado_em + via) e oferece retomada explícita ao usuário. Hoje o Hub é compartilhado mas nenhuma porta usa esse dado pra coerência cross-canal."
---

# Demanda — Continuidade cross-porta via Hub

## TL;DR

O Hub Qdrant é compartilhado entre todas as portas (Telegram, Claude
Code, Claude Chat, futura Custom GPT) desde a Fase 3 do ADR-001. Cada
fragmento carrega `criado_em` (timestamp) e `via` (origem). **Nenhuma
porta hoje usa esses dados pra oferecer "quer continuar de onde
parou na outra porta?".** Esta demanda especifica a feature em cada
porta — implementação distribuída, dado universal.

## Por que agora

1. Hub é jovem (~6 dias). Pré-Hub, dado não existia em forma utilizável.
2. Foco da semana foi infra (PRs MCP 49-60). Continuidade cross-porta
   é UX que precisa decisão consciente, não emerge do backend.
3. Multiportalidade só é real se o usuário **sentir** que é a mesma
   entidade. Hoje cada porta começa do zero — atrito que invalida o
   conceito de "1 Gus em vários canais".

## Estado atual (o que JÁ funciona)

- Hub `gus_hub` compartilhado, `criado_em` + `via` em todo fragmento
- Snapshot `dialogos/_bootstrap/gus-estado-atual.md` (cron 15min) com
  fragmentos das últimas 6h — usado pelo Claude Chat no boot
- `projetos/gus/_estado-atual.md` — handoff entre sessões Claude Code,
  atualizado manualmente ao fim de cada sessão
- `via` canônico: `telegram-claude`, `claude-code`, `claude-chat`,
  `custom-gpt`, `manual`, `curador`, `api`, `workflow-*`

## O que NÃO existe (a fazer)

Nenhuma porta hoje:
- Detecta "última atividade na outra porta há X tempo"
- Oferece retomada explícita ao boot
- Sinaliza visualmente "veio do canal Y"

## Proposta por porta

### 1. Telegram (TioGu) — `gus/bot.py`

**Gatilho:** primeira mensagem após >2h sem atividade nesse canal.

**Lógica:**
```python
async def detectar_continuidade(user_id: str = "gustavo") -> str | None:
    """Busca atividade em outras portas desde a última msg no Telegram."""
    fragmentos = await asyncio.to_thread(
        recentes, user_id, limit=10, incluir_esquecidos=False
    )
    outras_portas = [
        f for f in fragmentos
        if f.get("via") not in ("telegram-claude", None)
        and recente(f["criado_em"], horas=6)
    ]
    if not outras_portas:
        return None
    porta_alvo = outras_portas[0]
    return f"Você esteve no {porta_alvo['via']} há {fmt_delta(porta_alvo['criado_em'])} falando sobre {porta_alvo['conteudo'][:60]}... continuar daí ou novo assunto?"
```

**Custo:** ~30 LoC. Aciona uma vez por "abertura" — não polui chat ativo.

### 2. Claude Code (esta porta) — SessionStart hook

**Gatilho:** boot da sessão.

**Lógica:** ler `dialogos/_bootstrap/gus-estado-atual.md` (já existe)
+ filtrar últimos N fragmentos com `via in ('telegram-claude',
'claude-chat', 'custom-gpt')` e `criado_em > 1h atrás`. Injeta no
contexto inicial como nota: "Última atividade em outras portas: ..."

**Custo:** ~15 LoC no `.claude/hooks/session-start-continuidade.sh` ou
extender o hook `SessionStart` existente.

### 3. Claude Chat — extender `gerar-estado-claude-chat.yml`

**Gatilho:** já roda 15min em 15min.

**Lógica:** adicionar seção "Última atividade no TioGu" no topo do MD:
```
## Atividade recente em outras portas
- TioGu (telegram): há 23min — "discussão sobre Dimagem"
- Claude Code: há 2h12min — "Fase 1 backend SSE mergeada"
```

**Custo:** ~20 LoC em `.github/scripts/gerar_estado_claude_chat.py`.

### 4. NeuroGus — `api/neurogus.html`

**Gatilho:** boot do frontend.

**Lógica:** após `fetchInitial()`, calcular fragmento mais recente de
cada porta. Mostrar no header (ou banner topo):
```
última atividade — TioGu há 2h32min — sobre dimagem [clica pra ir até]
```

Clicar abre o painel lateral no fragmento e centraliza câmera nele.

**Custo:** ~25 LoC no `api/neurogus.html` (Parte 2 do plano).

### 5. Custom GPT (futura porta)

Mesma lógica do Telegram — implementar quando a porta entrar.
Pré-requisito: nada novo (`via=custom-gpt` já é canônico).

## Decisões abertas

1. **Threshold de "atividade recente"** por porta:
   - Telegram: >2h sem msg → trigger?
   - Claude Code: sempre trigger no boot (mesmo se ativo recente)?
   - NeuroGus: só mostra se >30min (senão é redundante)?

2. **Como apresentar o convite:**
   - Telegram: 1 msg do bot ao boot?
   - Claude Code: nota no contexto (já existe via SessionStart)?
   - NeuroGus: banner top recolhível? ícone de sino?

3. **Frequência da regeneração `gus-estado-atual.md`:**
   - Hoje 15min. Suficiente pra Claude Chat. Pra TioGu/NeuroGus
     consultarem direto, queremos isso live (cada call) ou cache?

4. **Conflito de fontes:**
   - O `via` do fragmento pode não bater com a porta real (ex:
     fragmento criado por workflow tem `via=workflow-X`). Lista
     branca: só mostra fragmentos com via humano-direto.

5. **Privacidade entre portas:**
   - LGPD: dados sensíveis (Dimagem) não devem aparecer no NeuroGus
     PWA. Filtro: ignorar `area=dimagem` na lógica de continuidade?

## Implementação sugerida — ordem

1. **Fase A** (Claude Code): hook `SessionStart` ler `gus-estado-atual.md`
   e injetar 1 linha no contexto. Trivial, ganho imediato.
2. **Fase B** (NeuroGus): banner header com link pro fragmento mais
   recente. Combina com a Parte 2 do plano NeuroGus.
3. **Fase C** (Claude Chat): adicionar seção "atividade recente" no
   `gerar-estado-claude-chat.yml`. Trivial.
4. **Fase D** (Telegram): handler de retomada no `bot.py`. Mais
   delicado — precisa não atrapalhar fluxo natural.
5. **Fase E** (Custom GPT): quando a porta entrar.

## Critério de pronto

- [ ] Cada porta ativa detecta atividade recente cross-canal
- [ ] Usuário recebe convite explícito de retomada (não silencioso)
- [ ] `via` é respeitado — só fragmentos humano-diretos contam
- [ ] LGPD: `area=dimagem` filtrado em portas não-locais
- [ ] Doc atualizado: `gus-XX-continuidade-cross-porta.md` em `projetos/gus/`

## Cross-references

- gus-12 (portas futuras) — diretriz "1 brain, N portas"
- gus-13 (tags canônicas) — define `via`
- gus-18 (schema indexação) — define `criado_em`
- gus-30.1 (NeuroGus decisões) — Fase 2 do NeuroGus pode incluir
- ADR-001 — Hub compartilhado é pré-requisito (resolvido)
