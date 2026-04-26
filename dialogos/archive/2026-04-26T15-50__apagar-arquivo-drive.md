---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: baixa
status: concluido
criado_em: 2026-04-26T15:50:00-03:00
processado_em: 2026-04-26T12:35:00-03:00
processado_por: claude-code
---

## Resultado

Tooling criado (workflow + script). Não consigo dispatchar daqui — Gustavo
ou Tiogu precisam disparar `delete-drive-file.yml` no GitHub Actions com:

- `file_id`: `15nSghWgKGh0Ef7Vda7YSdRm1QVUTn_I`
- `mode`: `dry-run` primeiro (confirma metadata), depois `trash`

Recomendação: rodar `dry-run` antes pra garantir que o ID bate com o arquivo
certo (`_teste_para_todas_portas.md`). Se confirmar, rodar de novo com
`trash` (recuperável 30 dias) ou `delete` (irreversível).

---


# Apagar arquivo no Drive via API

## Tarefa

Apagar o seguinte arquivo no Google Drive via API:

- **Nome:** `_teste_para_todas_portas.md`
- **ID:** `15nSghWgKGh0Ef7Vda7YSdRm1QVUTn_I`
- **Pasta:** `dialogos/Demandas Gustavo/`

## Contexto

Gustavo estava escrevendo um arquivo nessa pasta pelo celular mas nao consegue editar ou criar MD no Drive pelo celular. Pediu que fosse apagado.

Claude Chat nao tem ferramenta de delete no Drive MCP -- por isso esta demanda.

-- Claude Chat | via=claude-chat | 26/04/2026