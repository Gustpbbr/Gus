---
capturado_em: 2026-04-24T08:35:00
via: claude-code
tipo: futuro
status: ideia
---

# fut-14 — Tool `criar_demanda` no bot

## Dor identificada

O protocolo em `dialogos-tiogu-claude/` depende do bot **lembrar de registrar** cada demanda que surge naturalmente na conversa com o Gustavo. Hoje, se o Gustavo diz *"isso devia ser corrigido"* e o bot concorda, a demanda não vira commit — fica só na mensagem do Telegram. Gustavo é quem precisa lembrar de pedir o registro formal.

Caso concreto: 2026-04-24, bot sugeriu fix no timestamp do system prompt. Ficou só na conversa. Nunca chegou em `dialogos-tiogu-claude/semana-2026-04-21.md` — Claude Code teve que registrar retroativamente.

## Proposta

Nova tool no bot: `criar_demanda(titulo, contexto, prioridade)`.

**Comportamento:**
- Bot identifica na conversa um padrão "isso deveria ser feito" ou "precisaria de fix"
- Pergunta ao Gustavo: *"Registro como demanda no diálogo da semana?"*
- Com confirmação explícita, chama `criar_demanda`
- Tool adiciona entrada no MD da semana corrente em `dialogos-tiogu-claude/`
- Formato padronizado: `## AAAA-MM-DD — Gus\n\n**Demanda:**\n...\n\n**Contexto:**\n...\n\n**Prioridade:** X`

## Implementação técnica

Arquivo: `gus/tools.py`, nova função `_criar_demanda(titulo, contexto, prioridade)`.

```python
async def _criar_demanda(titulo: str, contexto: str, prioridade: str = "média") -> str:
    """Registra demanda em dialogos-tiogu-claude/semana-AAAA-MM-DD.md (segunda da semana corrente)."""
    agora = datetime.now(BRT)
    # Calcular segunda-feira da semana atual
    dias_desde_segunda = agora.weekday()
    segunda = agora - timedelta(days=dias_desde_segunda)
    arquivo = f"dialogos-tiogu-claude/semana-{segunda.strftime('%Y-%m-%d')}.md"

    # Ler arquivo existente via read_from_github
    conteudo_atual = await _read_from_github(arquivo)
    if conteudo_atual.startswith("Arquivo não encontrado"):
        # Cria arquivo novo da semana com header
        conteudo_atual = (
            f"---\ncapturado_em: {agora.isoformat()}\nvia: telegram\n---\n\n"
            f"# Semana {segunda.strftime('%d')}–{(segunda + timedelta(days=6)).strftime('%d de %B de %Y')}\n\n---\n"
        )

    # Append da nova demanda
    nova_entrada = (
        f"\n\n## {agora.strftime('%Y-%m-%d')} — Gus\n\n"
        f"**Demanda:**\n{titulo}\n\n"
        f"**Contexto:**\n{contexto}\n\n"
        f"**Prioridade:** {prioridade}\n\n"
        f"---\n\n_Aguardando resposta do Claude Code._\n"
    )

    novo_conteudo = conteudo_atual + nova_entrada
    # Salva
    filename = arquivo.split("/")[-1].replace(".md", "")
    folder = "/".join(arquivo.split("/")[:-1])
    return await _save_to_github(filename, novo_conteudo, folder)
```

## Schema pra TOOLS array

```json
{
    "name": "criar_demanda",
    "description": "Registra uma demanda no protocolo dialogos-tiogu-claude/. Use quando o Gustavo concordar que algo precisa virar trabalho de dev pro Claude Code. SEMPRE peça confirmação explícita antes de chamar — não registre especulação.",
    "input_schema": {
        "type": "object",
        "properties": {
            "titulo": {"type": "string", "description": "Demanda em 1-2 linhas"},
            "contexto": {"type": "string", "description": "Por que, de onde veio, cenário relevante"},
            "prioridade": {"type": "string", "enum": ["baixa", "média", "alta"]}
        },
        "required": ["titulo", "contexto"]
    }
}
```

## Regras adicionais no system prompt

Em `system_prompt.md`, nova seção:

> **Quando algo precisa virar demanda pro Claude Code:**
> - Durante a conversa, se você identificar que algo precisa de dev (fix de código, feature nova, melhoria arquitetural), **antes de chamar `criar_demanda`, pergunte ao Gustavo:** *"Registro como demanda no diálogo dessa semana?"*
> - Só chame a tool com confirmação explícita.
> - Não infle o protocolo: observação genérica ("poderia ser melhor") não vira demanda. Só coisas com escopo definível.

## Pré-requisitos

- Nenhum externo
- Código pronto no repo atual (read_from_github + save_to_github já existem)

## Esforço estimado

~20min código + commit + merge. Baixo risco, alto valor pro protocolo.

## Status

Ideia registrada 2026-04-24. Pode ser implementada a qualquer momento — priorizar quando o protocolo estiver sendo usado ativamente e fricção de "lembrar de pedir" virar dor real.
