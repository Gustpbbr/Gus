# textos-antigos/

Pasta de arquivamento. Guarda versões anteriores de arquivos do `gus/` que tinham
framing filosófico (referências aristotélicas, "valores centrais", "princípios
fundamentais") removido em 26/04/2026 conforme decisão do Gustavo de tratar
o projeto como 100% técnico daqui pra frente.

## Conteúdo

| Arquivo | Original | Substituído por |
|---|---|---|
| `gus-identity-v1.md` | versão pré-26/04/2026 com seção "Valores centrais" | `gus/gus-identity.md` (sem filosofia) |
| `gus-bootstrap-v1.md` | versão pré-26/04/2026 com "Princípios fundamentais" filosóficos | `gus/gus-bootstrap.md` (renomeado pra "Diretrizes operacionais") |
| `system_prompt-v1.md` | versão pré-26/04/2026 com seção "Valores" filosófica | `gus/system_prompt.md` (renomeado pra "Diretrizes operacionais") |

## Razão da mudança

Comportamentos do agente (não alucinar, verificar antes de afirmar, ser honesto
sobre limites) foram preservados, mas reformulados como **diretrizes operacionais**
ao invés de **valores filosóficos**. O que muda: framing. O que NÃO muda: o
comportamento esperado das LLMs em cada porta.

## Política de uso

Esta pasta é histórico. **Não é lida por LLMs no fluxo normal** (não está no
SessionStart hook, não é referenciada por bootstrap nem system_prompt). Existe
pra rastreabilidade — se alguém quiser saber "como era antes" ou reverter
alguma decisão, encontra aqui.

Não excluído do `sync-to-drive.yml` por enquanto. Se virar dor (poluir Drive),
adicionar `textos-antigos/` aos `EXCLUDE_PREFIXES` no script.
