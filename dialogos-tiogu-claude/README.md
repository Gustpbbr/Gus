---
capturado_em: 2026-04-24T08:16:35
via: telegram
---

# Diálogos TioGu ↔ Claude Code

Canal de comunicação assíncrono entre o Tiogubot (agente Telegram do Gustavo) e o Claude Code, além de outros canais e portas que o Gus pode acessar.

## Como funciona

- **Tiogubot escreve**: a demanda da semana — o que precisa ser feito, contexto, prioridade
- **Claude Code escreve**: o que foi feito, o que não foi feito e por quê
- Um MD por semana, nomeado com a data da segunda-feira daquela semana
- As mensagens são sequenciais dentro do MD — é um diálogo registrado, e cada entrada, de ambas as partes, deve conter data e horário.

## Nomenclatura dos arquivos

```
semana-YYYY-MM-DD.md   ← data sempre referente à segunda-feira da semana
```

Exemplos:
- `semana-2026-04-21.md` — semana de 21 a 27 de abril de 2026
- `semana-2026-04-28.md` — semana de 28 de abril a 4 de maio de 2026

## Estrutura de cada MD

```markdown
## [DATA] — Agente (Tiogubot, Claude code...)
**Demanda:**
...

**Contexto:**
...

**Prioridade:** alta | média | baixa

---

## [DATA] — Claude Code
**Feito:**
...

**Não feito:**
...

**Por quê:**
...

---
```

## Protocolo

1. Gus abre o MD da semana na segunda-feira com as demandas, ou assim que solicitado (via Gustavo ou hook), a qualquer momento.
2. Claude Code lê, executa e registra sua resposta no mesmo MD
3. Se houver iteração na semana, continua no mesmo arquivo (mensagens sequenciais)
4. Na segunda seguinte, abre-se um MD novo — o anterior fica como histórico
