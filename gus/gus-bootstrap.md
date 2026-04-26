# MOVIDO

Este arquivo foi movido em 26/04/2026 pra:

**`dialogos/_bootstrap/gus-bootstrap.md`**

Motivo: o bootstrap precisa ficar onde o Claude Chat sempre acessa a versão
mais recente. `dialogos/` é a única pasta com sync bidirecional Drive↔GitHub
(via `import-from-drive.yml` + `sync-to-drive.yml`), então qualquer mudança
chega no Drive em até ~2min e o Chat lê on-demand.

A pasta `dialogos/_bootstrap/` é convenção read-only — não editar pelo Drive.

Para Claude Chat ativar identidade Gus:

> "lê `Gus-Sync/dialogos/_bootstrap/gus-bootstrap.md` e segue como Gus"
