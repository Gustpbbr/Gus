---
tipo: limpeza-candidatos
gerado_em: 2026-05-03T00:15:10.000287-03:00
total_candidatos: 357
jaccard_threshold: 0.7
---

# Limpeza Hub — candidatos a delete

Gerado por `.github/scripts/limpeza_hub_dryrun.py` em 03/05/2026 às 00:15 BRT. **Nada foi deletado** — este é o relatório dryrun pra Gustavo aprovar.

## Como aprovar

1. Revise cada candidato abaixo. Se um deve ser **mantido** (não deletar), copie o ID e adicione em `_indices/_limpeza-hub-rejeitados.txt` (um ID por linha).
2. Se aprova **todos** os candidatos: deixe `_limpeza-hub-rejeitados.txt` vazio (ou inexistente).
3. Rode `limpeza_hub_aplicar.py` (workflow `limpeza-hub-aplicar.yml`) — deleta todos os candidatos *exceto* os listados em rejeitados.

Trilha de auditoria automática em `_log/deletar-hub/AAAA-MM-DD.jsonl` (item 1.3 do plano). Snapshot completo de cada delete pra recovery se precisar.

## Resumo
- **Total de candidatos:** 357
- **Por severidade:** forte=327, medio=30
- **Por razão:** CROSS-BRAIN=2, DUPLICATA semântica do fragmento mais antigo `13f751e3-76f6-46f7-87ee-2d4a5b4183f0` (Jaccard ≥ 0.7). Manter 'As demandas paradas são=4, DUPLICATA semântica do fragmento mais antigo `15554770-64b2-4cad-a7c6-d7cd3f3b83fa` (Jaccard ≥ 0.7). Manter 'O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h....'=1, DUPLICATA semântica do fragmento mais antigo `24de68a8-ff3f-45b6-915f-d2a03e00e87b` (Jaccard ≥ 0.7). Manter 'O bot possui uma funcionalidade de caching de prompts que reduz o custo de input...'=1, DUPLICATA semântica do fragmento mais antigo `2c85c5ed-0b80-413e-8a5c-ad2f612cbef9` (Jaccard ≥ 0.7). Manter 'O bot Telegram (TioGu) opera com um sistema multi-porta usando Hub Qdrant como m...'=2, DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'=15, DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros=7, DUPLICATA semântica do fragmento mais antigo `3744f3c7-6ff7-472d-b7bc-eac54ab61f94` (Jaccard ≥ 0.7). Manter 'A convenção de nomenclatura dos arquivos JSON é <paciente_id>__<data_coleta>__<l...'=1, DUPLICATA semântica do fragmento mais antigo `391e1f0e-b212-4f4d-9007-8aaf3bf79b03` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-port...'=3, DUPLICATA semântica do fragmento mais antigo `43d0fcc6-b67e-4946-9256-b6ff29374154` (Jaccard ≥ 0.7). Manter 'O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot das 03h....'=2, DUPLICATA semântica do fragmento mais antigo `459efb6f-d142-4bf5-b505-080da3a2c61b` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta utiliza o Hub Qdrant como memória central, GitHub como con...'=2, DUPLICATA semântica do fragmento mais antigo `4b4473d3-a02d-4c07-9235-ac30e53d88a3` (Jaccard ≥ 0.7). Manter 'A captura multiporta do Claude Chat precisa de um gatilho proativo no Chat, e is...'=1, DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'=6, DUPLICATA semântica do fragmento mais antigo `4ffeb68c-9480-41cb-b5b4-f47a1e406973` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa....'=4, DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'=5, DUPLICATA semântica do fragmento mais antigo `52eb9ac7-4846-487f-865e-4c685420a21f` (Jaccard ≥ 0.7). Manter 'O Arquivo `gus-estado-atual.md` (27/04) está desatualizado em relação aos PRs #5...'=2, DUPLICATA semântica do fragmento mais antigo `559b1f78-6b75-45f0-8f32-8c1e0728bd96` (Jaccard ≥ 0.7). Manter 'O projeto utiliza um sistema multi-porta com Hub Qdrant como memória central....'=1, DUPLICATA semântica do fragmento mais antigo `593497ee-c359-4164-a3f2-78e668819b43` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`....'=1, DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'=6, DUPLICATA semântica do fragmento mais antigo `627be3c7-fca0-4fd6-88f1-86f678cd8b60` (Jaccard ≥ 0.7). Manter 'A captura do Claude Code via cron salva transcript redatado, e o cron processa v...'=1, DUPLICATA semântica do fragmento mais antigo `679c5bb8-76e4-4ba3-87eb-74b52f528c69` (Jaccard ≥ 0.7). Manter 'O core obrigatório deve ser lido em toda aba nova=1, DUPLICATA semântica do fragmento mais antigo `6a882dc0-b241-4316-98f2-1c5a4d366487` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta com Hub Qdrant é a memória central do projeto Gus....'=3, DUPLICATA semântica do fragmento mais antigo `6c44e7af-5fdf-4969-8f58-73a3c834323a` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`=3, DUPLICATA semântica do fragmento mais antigo `70a8d959-cb6a-4d60-b47c-598662ac0ba2` (Jaccard ≥ 0.7). Manter 'O arquivo projetos/gus/_estado-atual.md informa onde paramos na sessão anterior....'=1, DUPLICATA semântica do fragmento mais antigo `75e6e624-cbfa-4af0-9fab-836864ce85b7` (Jaccard ≥ 0.7). Manter 'O Hub teve 19 fragmentos no brain `gustavo`, e o sistema estava ocioso nas últim...'=1, DUPLICATA semântica do fragmento mais antigo `774231d1-e03a-401e-a757-17f8f89e8b9a` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` da pasta `projetos/gus` está desatualizado desde 27/04....'=4, DUPLICATA semântica do fragmento mais antigo `786baeaa-e0cb-41db-8c32-b2a22eb9d325` (Jaccard ≥ 0.7). Manter 'O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é um snapshot do Hub gerado ...'=1, DUPLICATA semântica do fragmento mais antigo `79d2e601-8103-48ec-85d5-95b787c62dd9` (Jaccard ≥ 0.7). Manter 'A captura Claude Code via cron processa transcripts redatados, cron salva transc...'=1, DUPLICATA semântica do fragmento mais antigo `8058cd9e-a825-4d63-b848-ebd766bcb4b8` (Jaccard ≥ 0.7). Manter 'O "_estado-atual.md" está desatualizado e precisa de revisão....'=1, DUPLICATA semântica do fragmento mais antigo `823eab03-34c5-498e-a2da-c756983bbc6d` (Jaccard ≥ 0.7). Manter 'O bot TioGu tem uma arquitetura baseada em um sistema multi-porta com Hub Qdrant...'=1, DUPLICATA semântica do fragmento mais antigo `839e1b47-b1c5-4585-8bc5-fa93a6ff2ff0` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros=2, DUPLICATA semântica do fragmento mais antigo `84dca0e2-47a0-4592-b8fe-9e54cf881d9b` (Jaccard ≥ 0.7). Manter 'A auditoria identificou a necessidade de integrar uma lógica clara para hierarqu...'=1, DUPLICATA semântica do fragmento mais antigo `85f98b86-b768-4fd5-82c2-3cc216794652` (Jaccard ≥ 0.7). Manter 'As duas demandas pendentes em dialogos/inbox/ são=1, DUPLICATA semântica do fragmento mais antigo `87857940-8e7d-4728-b18b-add306aa7294` (Jaccard ≥ 0.7). Manter 'O arquivo `dialogos/_bootstrap/gus-bootstrap.md` é o manual operacional do Gus, ...'=2, DUPLICATA semântica do fragmento mais antigo `8b78e267-65e1-4167-a763-6180054c9f31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs está no código e nos docs `gus-XX` atualizados, enquanto ...'=1, DUPLICATA semântica do fragmento mais antigo `8d9942c9-b4dc-4341-a7cf-1fac28957e82` (Jaccard ≥ 0.7). Manter 'No TioGu há um sistema multi-porta (Telegram, Claude Code, Claude Chat) com Hub ...'=3, DUPLICATA semântica do fragmento mais antigo `8ec5aa19-6659-4c55-8d06-8ccf96721bcc` (Jaccard ≥ 0.7). Manter 'Decisão sobre o drive sync precisa ser feita=1, DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'=6, DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'=6, DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'=5, DUPLICATA semântica do fragmento mais antigo `a20dbbce-0e07-46fe-aa3c-fa3da3f244d9` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` e `gus-26-status-consolidado.md` estão desatualizados e não...'=2, DUPLICATA semântica do fragmento mais antigo `a26681e1-c75c-4d08-80c2-d7cdd867d02a` (Jaccard ≥ 0.7). Manter 'O bot TioGu é um sistema multi-porta que se conecta ao Telegram e utiliza o Hub ...'=1, DUPLICATA semântica do fragmento mais antigo `a2d802c7-ae1d-4925-8849-d303169f49d9` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proat...'=2, DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'=6, DUPLICATA semântica do fragmento mais antigo `a865bbc0-f532-42c6-88a1-dd81a8ee765b` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant + curador híbrido coleta dual rola até 12/05....'=1, DUPLICATA semântica do fragmento mais antigo `b2ec58bb-6275-4216-9844-a4b1cb0467f1` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'=4, DUPLICATA semântica do fragmento mais antigo `b5cb7a3c-0000-49e8-b30d-aa41abd3f431` (Jaccard ≥ 0.7). Manter 'Identidade e arquitetura do projeto Gus, com sistema multi-porta (Telegram, Clau...'=3, DUPLICATA semântica do fragmento mais antigo `bdffd3e9-4144-4007-a025-5ca78ddc0829` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta tem o Hub Qdrant como memória central....'=2, DUPLICATA semântica do fragmento mais antigo `bf8ec5aa-dccb-49a0-b18d-c997184a2d75` (Jaccard ≥ 0.7). Manter 'As demandas pendentes são=1, DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'=6, DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`=5, DUPLICATA semântica do fragmento mais antigo `c891788f-4176-4c8c-9830-d26cb3c72906` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant está na Fase 4 da migração Mem0....'=1, DUPLICATA semântica do fragmento mais antigo `cfff1d65-1e8f-455a-80d6-2d669b368f66` (Jaccard ≥ 0.7). Manter 'Os 4 documentos pendentes são=1, DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'=13, DUPLICATA semântica do fragmento mais antigo `d60091e2-0729-4fd6-915c-ac47a1277cc5` (Jaccard ≥ 0.7). Manter 'As demandas paradas são=3, DUPLICATA semântica do fragmento mais antigo `d62f9fc2-1671-4220-88f5-d2c3ceb54d06` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`....'=3, DUPLICATA semântica do fragmento mais antigo `dc6bf108-7ec0-4a56-9f2f-820d27202d31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'=4, DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'=6, DUPLICATA semântica do fragmento mais antigo `e2876493-006e-449e-924e-c7f0ada4dffa` (Jaccard ≥ 0.7). Manter 'O Hub está ocioso há 6 horas....'=1, DUPLICATA semântica do fragmento mais antigo `e4af60ca-b56b-4bf7-bebb-2c6aeb36eb4b` (Jaccard ≥ 0.7). Manter 'O arquivo _estado-atual.md está desatualizado com relação aos últimos PRs....'=1, DUPLICATA semântica do fragmento mais antigo `e753d23a-7899-4e60-8b50-a94d0fb4ec99` (Jaccard ≥ 0.7). Manter 'Os quatro arquivos `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/...'=3, DUPLICATA semântica do fragmento mais antigo `e7dd8057-58b1-4b38-98fe-3900a18ba5e3` (Jaccard ≥ 0.7). Manter 'A captura Claude Code via cron salva transcripts redatados e o cron processa via...'=1, DUPLICATA semântica do fragmento mais antigo `e9710909-43c4-4b70-a417-efb1cebd0629` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` está desatualizado e não reflete as últimas atualizações do...'=1, DUPLICATA semântica do fragmento mais antigo `ec632dc4-38a3-40d4-b811-74be9485bc76` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`=2, DUPLICATA semântica do fragmento mais antigo `f161207b-8608-4bb7-be08-084ff25f3d67` (Jaccard ≥ 0.7). Manter '`_frontmatter-referencia.md` é um template e não é uma demanda....'=2, DUPLICATA semântica do fragmento mais antigo `f184bc91-cd10-4ca7-9c36-c7054d3b689c` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` do projeto está desatualizado desde 27/04/2026....'=1, DUPLICATA semântica do fragmento mais antigo `f221a7c4-7bc6-4bd4-a904-f11722c2f1a9` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`=2, DUPLICATA semântica do fragmento mais antigo `f4a8f8ba-3b25-48f9-abd1-166a2434a121` (Jaccard ≥ 0.7). Manter 'Os 4 documentos fundamentais para qualquer aba nova são `dialogos/_bootstrap/gus...'=1, DUPLICATA semântica do fragmento mais antigo `f584e27e-d458-4b41-a921-481bca2c8256` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` pode ser resolvida por 3 opções=1, META-LIXO=135, UNCLASSIFIED=30
- **Por brain:** gus=182, gustavo=175

## Brain `gus` — severidade forte (170 candidatos)

### `032ef70b-317d-49f3-a1ef-8e74ad4e3dcc`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `07ab179e-356f-4f50-85da-612b619a4918`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `0bd895f1-23e0-4ed4-91b8-8d8927804046`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.

### `0d41602c-df68-43b7-aa82-2421ca05cfb8`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** o arquivo `claude-chat` contém 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e o `_frontmatter-referencia

### `101d6130-b7ba-4b3b-a18a-7cbb1769ccc7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram, TioGu, possui 21 tools, multimídia, prompt caching, e operação em Railway.

### `12c222ce-eea6-4001-96f7-6f2eefdd3f07`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e opera a partir do Hub Qdrant.

### `18ea6196-18b5-4afa-8c72-e25d79083e1a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui aproximadamente 21 tools e utiliza técnicas de caching de prompts para melhorar a performance.

### `19c7f73a-00c3-4472-9e14-0338d2c01e28`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em dialogos/inbox-claude-code/

### `1c60571d-5338-4f3f-b846-6b06d087b7fc`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `1dd1dde1-67ad-4585-ab50-7a990c8ceed7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `26c739cb-5f17-42f5-8411-b58b9e32941d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.

### `31e879ec-1c1b-4d94-8b8b-8d5a30a031db`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `326fb6b2-c33d-4cf4-8100-fd20a8a3319b`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto possui 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.

### `3e85be50-a929-447a-965b-c3717172b3c1`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em dialogos/inbox-claude-code/

### `4bf85d21-2d2c-47f0-b106-90f3fca1ee39`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e `_frontmatter-referencia.md` que é só template.

### `4c102491-40de-4f26-a8a3-4289cbd9139e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem ~21 tools, multimídia, e prompt caching, em produção Railway.

### `4da809c8-54c0-4c8e-9e05-d379a19f0079`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.

### `506a64e4-381a-474b-973e-e723d8ea7ae6`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, em produção Railway.

### `5488dacf-a224-4be3-b59f-a09e30591269`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `611c990f-49cc-40c2-abe9-f19748865b75`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui cerca de 21 tools com multimídia e prompt caching implementados.

### `67316d8e-a8ca-4120-987e-a230a8112d65`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram, chamado TioGu, possui aproximadamente 21 ferramentas, multimídia, prompt caching, e está em produção no Railway.

### `67db18e0-7a4c-44d1-af35-e9220d8efbb6`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O arquivo untracked é um log do retro-engine desta sessão.

### `78a3940e-b4be-4fd0-82f0-5eb92d276d3d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (este é um template, não é

### `79d52ee0-622b-4b8e-a7ee-e686ec6e1f85`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas na pasta `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é template, não é d

### `7a90c08d-db9d-47e9-a4ef-4df5dbc9a557`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot TioGu tem 21 tools, multimídia e prompt caching implementados.

### `7b560548-e73c-4e69-bacb-2d1b1832fbe7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto tem 4 demandas pendentes no 'dialogos/inbox-claude-code/'.

### `7e82caf9-9fbc-4e43-9978-89372ed5c2dd`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só um templ

### `8106e04c-6bc2-4436-8d4c-323a393130bc`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O log do retro-engine está em `claude/greeting-checkin-94weM`.

### `83edfaac-d113-4972-9c21-5c012b7fc631`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `85d3bcf1-80a7-466f-873a-0bcddc6a310c`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é um template, não u

### `891e0bb1-3483-4cf6-b14e-713f8ef5138f`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot TioGu possui 21 ferramentas, incluindo ferramentas de mídia como Claude Vision, PDF nativo e Whisper.

### `8f0e1f20-aeda-4e3f-9be3-0e778e199659`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram, TioGu, possui cerca de 21 ferramentas, multimídia, prompt caching e está em produção no Railway.

### `8f1f6109-ff45-46b1-abf4-26f1436a5df6`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em dialogos/inbox-claude-code/.

### `93d102f2-47b1-4fb2-be5d-893c444e1879`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A auditoria do Chat foi concluída com correções.

### `96304a0d-3331-43ec-9b07-81a3463dc703`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) já possui mais de 21 ferramentas, multimídia e prompt caching em produção.

### `972da787-c9cc-473e-ba3c-6135edcff058`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A arquitetura do TioGu inclui um bot Telegram com 21 tools, multimídia, e prompt caching.

### `9a69ac12-cc13-4089-9119-1e5d4a9a5e18`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O retro-engine registra erros quando a variável `ANTHROPIC_API_KEY` está ausente, resultando em um log no formato de no-op.

### `9aa8e4c8-8bd8-4372-ac79-a31fbaaf4718`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.

### `9cda2d1a-8536-4908-aa28-fcb6fd0a64c1`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui cerca de 21 tools, multimídia, prompt caching, e está em produção na Railway.

### `a3fcaa8a-09a1-4dd6-9778-e547319a0b44`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto Gus possui 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `a876246f-bff9-4d93-a184-ccc46e52b9ad`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O arquivo untracked é o log do retro-engine dessa sessão, que indica um 'no-op' devido à falta de chave.

### `a8b62d4b-435e-4794-a0d0-75d771b4c5a3`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `ad677a0f-37d6-42cb-af59-bd2c1ebd622e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A construção de um bot para o Telegram (TioGu) está em andamento, com cerca de 21 ferramentas integradas.

### `ae9c17e7-c813-45f6-805b-c1ef940dc410`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.

### `b060baa5-5cf5-41fb-bcb5-5c5b7018a9fe`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O arquivo untracked é um log do retro-engine informando 'no-op: anthropic_missing' devido à falta da variável `ANTHROPIC_API_KEY`.

### `b5ac338b-e2b9-4cd1-a746-71a8773b53aa`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `b7427b14-c20a-4287-a761-777c53206c87`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `c129e203-38c3-4a3d-be4d-0962fe9a3b1e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.

### `c159235a-c065-4fc8-91bc-135f713f390c`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.

### `c25fe049-9a54-46a3-bde7-72dbc859be9a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em dialogos/inbox-claude-code/

### `c6ebaeee-a960-4748-98cb-8d24403aba2e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.

### `cc0f238c-ae50-4848-a1c1-65be76a59037`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `d2b702e8-55e7-4450-8dc0-cd2efe94ccd7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O retro-engine registra 'no-op: anthropic_missing' e segue.

### `d3b82543-5eaf-488b-9b3f-3f2bffbb1652`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O terminal do bot Telegram (TioGu) possui ~21 tools, multimídia, e prompt caching.

### `d62f9fc2-1671-4220-88f5-d2c3ceb54d06`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `d6cbf3a5-587b-4f50-ae39-a33873520f60`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (template, não é demanda).

### `d7c2c6f7-da96-42bb-9afe-85eca6911d81`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas no diretório dialogos/inbox-claude-code.

### `de137d0e-2bad-4024-b2ee-9273a6b63d1b`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Tem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.

### `ea2d55f7-8564-4973-a910-fdb41b58aa72`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.

### `ec632dc4-38a3-40d4-b811-74be9485bc76`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.

### `ee6b1624-4e24-43b1-97f4-60b0f815b0dc`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram possui ~21 ferramentas distintas implementadas.

### `eeab7828-5e15-4c24-aea5-4abf331795e2`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em dialogos/inbox-claude-code/

### `f004a4af-433e-431e-a140-55c2ae012a56`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.

### `f07dd224-6dd5-48d4-a90e-a1a9fcdf37d2`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) é composto por 21 tools e possui multimídia, prompt caching, e funciona em produção no Railway.

### `f221a7c4-7bc6-4bd4-a904-f11722c2f1a9`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).

### `f8333710-87b8-47bc-8e4d-183addf40c90`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `fb8943b6-2f50-40c8-b619-6f95cda04d66`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/' para serem analisadas.

### `afc059b7-c9fa-462a-bf9f-7d50b421e0b9`
- **Razão:** CROSS-BRAIN: fragmento no brain `gus` mas conteúdo é fato sobre Gustavo (deveria estar em `gustavo`). Recomendado: deletar daqui — se valer recuperar, importa via Fase 5.6 (legacy-mem0-saas backup)
- **Texto:** Nasci em Vitória.

### `c8d68c55-5f7b-4cbb-8ea7-b1183750b5a7`
- **Razão:** CROSS-BRAIN: fragmento no brain `gus` mas conteúdo é fato sobre Gustavo (deveria estar em `gustavo`). Recomendado: deletar daqui — se valer recuperar, importa via Fase 5.6 (legacy-mem0-saas backup)
- **Texto:** Nasci em Vitória.

### `350cd425-4895-431c-a2f5-d81ae0e06c36`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` está desatualizado — git log mostra muita coisa depois.

### `3f7535d8-6f4e-481f-9db7-3be1799770bc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `9a5a14bb-9d7a-4a91-b0b4-db62873c182b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O _estado-atual.md está desatualizado — o git log mostra muita coisa depois.

### `0142cd23-4d05-4b6d-99a0-77345c38a0d5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `591271cd-9c61-4213-babb-b71cbdaaacbb`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `11bd1304-a9a7-4e51-a493-7b4f46f7ee53`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.

### `12ab65e8-c03c-4786-8732-0f8f3c1f3e4a`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — o git log mostra muita coisa depois.

### `ac4a0caf-dc87-4e5b-81e0-86bd790f25b3`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `eff6200f-8dba-4279-b50d-f622c768d47e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67).

### `c99b1aa0-6c5c-4450-8ed6-5c379c3900d5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `32ea69cb-25cc-474a-b57f-779e1d0ae0fc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `d955900c-0a6c-4ffd-91aa-e5f62719d78a`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `405081ab-fc30-4982-8a23-042b09f1bc62`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.

### `61b34cdb-94f7-4d34-88aa-f633b2327065`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois.

### `379c71ae-0206-4af9-a1f3-266b526af9a5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2e7a49cb-6a90-401c-95db-c9eac9782712` (Jaccard ≥ 0.7). Manter 'O arquivo `_estado-atual.md` está desatualizado — git log mostra muita coisa dep...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `bbf4b749-a292-49ef-ae6e-9c010b9e99af`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` foi parcialmente resolvida pelo PR #67, mas ainda falta um gatilho no Chat.

### `9f6212e8-4e2e-4a4d-a71c-ed4bea0fbb78`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** Demanda `2026-05-01-captura-multiporta-curador.md` parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.

### `1b7bd08a-f8d8-4d5d-8158-d8f40657138d`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.

### `01781bc5-41fe-4773-852c-e9f66fdbca6d`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.

### `dca21376-c24e-4679-802e-698c65c83c38`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.

### `472370b9-9ce6-43b1-ab6c-86ccf35727a2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `5b609d4b-e75e-403f-9aa2-6795bbea4703` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.

### `91cec628-4bfc-4afe-ba00-8bbe07308d56`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d62f9fc2-1671-4220-88f5-d2c3ceb54d06` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`....'
- **Texto:** Existem três demandas paradas em `dialogos/inbox-claude-code/`.

### `3133a2c7-d340-488c-b0da-8cf8a8d78eba`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d62f9fc2-1671-4220-88f5-d2c3ceb54d06` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`....'
- **Texto:** Existem três demandas paradas em `dialogos/inbox-claude-code/`.

### `06a610ff-91d8-4ec8-b1ec-f900133b56b2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d62f9fc2-1671-4220-88f5-d2c3ceb54d06` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`....'
- **Texto:** Tem três demandas paradas em dialogos/inbox-claude-code/

### `064e6b66-1821-4789-92ba-75889736d206`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e753d23a-7899-4e60-8b50-a94d0fb4ec99` (Jaccard ≥ 0.7). Manter 'Os quatro arquivos `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/...'
- **Texto:** Os 4 arquivos obrigatórios para o contexto em toda aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_estad

### `ab1f2d26-8f29-4b8e-b06a-772d2d9d5bc0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e753d23a-7899-4e60-8b50-a94d0fb4ec99` (Jaccard ≥ 0.7). Manter 'Os quatro arquivos `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/...'
- **Texto:** Os arquivos `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md` e `projetos/gus/_estado-atual.md` fornecem 80% do contexto para qua

### `ceedef45-7526-4f4b-ac57-05564eae8a52`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e753d23a-7899-4e60-8b50-a94d0fb4ec99` (Jaccard ≥ 0.7). Manter 'Os quatro arquivos `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/...'
- **Texto:** Os arquivos obrigatórios para qualquer aba nova são: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md` e `projetos/gus/_estado-at

### `d7895fa8-3f8f-4351-8403-ccb1c6ecd072`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `ec632dc4-38a3-40d4-b811-74be9485bc76` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiport...'
- **Texto:** Na pasta `dialogos/inbox-claude-code/` estão 4 demandas pendentes: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só temp

### `68489161-055b-4184-a450-783c6c6e6408`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `ec632dc4-38a3-40d4-b811-74be9485bc76` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiport...'
- **Texto:** Os nomes das demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e o `_frontmatter-referencia.md` é um template.

### `9d63362a-ad0e-470b-991f-faa7a66ba3f9`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `4699d997-7635-43a1-bbc8-fa508dae986e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** O usuário está na porta Code, branch `claude/initial-setup-iWTfL`.

### `50e9c912-15e8-4bd3-9b8d-52e8be43d422`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** O Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `0d9cf3b5-da3b-4553-9102-dff1ed1944a1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `401956ec-8f0b-4117-895b-6e81dd9197b8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** O Gustavo está trabalhando na porta Code, branch `claude/initial-setup-iWTfL`.

### `c510ecaf-e530-4e6d-bd1b-39d2f8169642`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c37bf446-12f1-4481-a170-5cd6c6e17494` (Jaccard ≥ 0.7). Manter 'O usuário está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** O Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `df942945-0b89-4f76-a078-8603927a61e1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4ffeb68c-9480-41cb-b5b4-f47a1e406973` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa....'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `11ffe73d-c0d5-41c1-982e-9d6ca8dfcc12`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4ffeb68c-9480-41cb-b5b4-f47a1e406973` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa....'
- **Texto:** A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa e precisa ser resolvida.

### `b2cedbfa-8a04-425c-abad-4aad2bdd84d8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4ffeb68c-9480-41cb-b5b4-f47a1e406973` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa....'
- **Texto:** A demanda '2026-05-01-drive-sync-oauth-fix.md' está ativa e precisa de decisão sobre o sync do Drive.

### `3277cb08-58e7-452f-b46d-8cc30e68fbdf`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4ffeb68c-9480-41cb-b5b4-f47a1e406973` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa....'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `12a0e682-df06-4a86-92cb-955f38bfc3da`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8d9942c9-b4dc-4341-a7cf-1fac28957e82` (Jaccard ≥ 0.7). Manter 'No TioGu há um sistema multi-porta (Telegram, Claude Code, Claude Chat) com Hub ...'
- **Texto:** O sistema multi-porta conecta Telegram, Claude Code, Claude Chat, com Hub Qdrant como memória central.

### `2c7b4649-3e39-4561-83a5-be5029359d4b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8d9942c9-b4dc-4341-a7cf-1fac28957e82` (Jaccard ≥ 0.7). Manter 'No TioGu há um sistema multi-porta (Telegram, Claude Code, Claude Chat) com Hub ...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat) usa Hub Qdrant como memória central e GitHub como conhecimento.

### `504c5179-79b0-4da7-acc1-1a67f314615f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8d9942c9-b4dc-4341-a7cf-1fac28957e82` (Jaccard ≥ 0.7). Manter 'No TioGu há um sistema multi-porta (Telegram, Claude Code, Claude Chat) com Hub ...'
- **Texto:** Sistema multi-porta (Telegram, Claude Code, Claude Chat) com Hub Qdrant como memória central e GitHub como conhecimento.

### `49203088-eac1-4448-aa24-3fae6cab5954`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `13f751e3-76f6-46f7-87ee-2d4a5b4183f0` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** As demandas paradas são: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md, _frontmatter-referencia.md.

### `441c24e9-8700-42a0-95fc-75c8dc1cdade`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `13f751e3-76f6-46f7-87ee-2d4a5b4183f0` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** As demandas paradas são: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md.

### `ff16dabc-eca6-488a-8236-a2f7b8525acc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `13f751e3-76f6-46f7-87ee-2d4a5b4183f0` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.

### `1f662f95-1340-4081-8e2a-e4904153dd68`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `13f751e3-76f6-46f7-87ee-2d4a5b4183f0` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** Listagem das demandas paradas: '2026-05-01-captura-multiporta-curador.md', '2026-05-01-drive-sync-oauth-fix.md', '_frontmatter-referencia.md'.

### `1582698e-b82a-4ba3-953b-6191ee430167`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c891788f-4176-4c8c-9830-d26cb3c72906` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant está na Fase 4 da migração Mem0....'
- **Texto:** O Hub está na fase 4 da migração Mem0 para Hub Qdrant.

### `18953601-7358-4783-a0fe-6bef9a644fa0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8058cd9e-a825-4d63-b848-ebd766bcb4b8` (Jaccard ≥ 0.7). Manter 'O "_estado-atual.md" está desatualizado e precisa de revisão....'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado e precisa ser revisado.

### `1b215c53-cb43-4f49-8385-d0b7a7363bfb`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e7dd8057-58b1-4b38-98fe-3900a18ba5e3` (Jaccard ≥ 0.7). Manter 'A captura Claude Code via cron salva transcripts redatados e o cron processa via...'
- **Texto:** A captura Claude Code via cron salva transcripts redatados, e o cron processa via curador a cada 30 minutos.

### `8011b7cb-57b3-467f-932e-c9f05241fc8b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `52eb9ac7-4846-487f-865e-4c685420a21f` (Jaccard ≥ 0.7). Manter 'O Arquivo `gus-estado-atual.md` (27/04) está desatualizado em relação aos PRs #5...'
- **Texto:** O '_estado-atual.md' de 27/04 está desatualizado em relação aos PRs mais recentes.

### `227feb1f-0182-4611-b14c-dceb1f1d4967`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `52eb9ac7-4846-487f-865e-4c685420a21f` (Jaccard ≥ 0.7). Manter 'O Arquivo `gus-estado-atual.md` (27/04) está desatualizado em relação aos PRs #5...'
- **Texto:** O `_estado-atual.md` está desatualizado em relação a PRs recentes.

### `ba195c79-d89d-491b-a6de-9f12dc14cb56`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f161207b-8608-4bb7-be08-084ff25f3d67` (Jaccard ≥ 0.7). Manter '`_frontmatter-referencia.md` é um template e não é uma demanda....'
- **Texto:** `_frontmatter-referencia.md` é um template e não é uma demanda.

### `2721b630-3bc8-4117-ad35-335e518984d8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f161207b-8608-4bb7-be08-084ff25f3d67` (Jaccard ≥ 0.7). Manter '`_frontmatter-referencia.md` é um template e não é uma demanda....'
- **Texto:** '_frontmatter-referencia.md' é um template, não uma demanda.

### `28080e79-9a32-4535-8c10-3f0d78e7520b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8b78e267-65e1-4167-a763-6180054c9f31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs está no código e nos docs `gus-XX` atualizados, enquanto ...'
- **Texto:** O estado final dos PRs já está no código + nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente está.

### `cc9830ab-521d-4a53-8941-9b3e8a127d5f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2c85c5ed-0b80-413e-8a5c-ad2f612cbef9` (Jaccard ≥ 0.7). Manter 'O bot Telegram (TioGu) opera com um sistema multi-porta usando Hub Qdrant como m...'
- **Texto:** O bot Telegram (TioGu) é um sistema multi-porta com Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.

### `d17a8150-2484-47e0-8750-b71f9bc9661b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `2c85c5ed-0b80-413e-8a5c-ad2f612cbef9` (Jaccard ≥ 0.7). Manter 'O bot Telegram (TioGu) opera com um sistema multi-porta usando Hub Qdrant como m...'
- **Texto:** O sistema multi-porta tem o Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.

### `30199240-c83c-4a16-8fc0-d3744992c5d8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `459efb6f-d142-4bf5-b505-080da3a2c61b` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta utiliza o Hub Qdrant como memória central, GitHub como con...'
- **Texto:** O TioGu utiliza um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.

### `6209d8fd-7cff-4acb-bc7f-6ddb09692cc0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `459efb6f-d142-4bf5-b505-080da3a2c61b` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta utiliza o Hub Qdrant como memória central, GitHub como con...'
- **Texto:** O sistema multi-porta utiliza Hub Qdrant como memória central.

### `e15750c0-edae-419e-9b46-11fd39ac5672`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `bdffd3e9-4144-4007-a025-5ca78ddc0829` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta tem o Hub Qdrant como memória central....'
- **Texto:** O sistema multi-porta tem Hub Qdrant como memória central.

### `35826dae-e1d0-488f-880b-00d64cb5b8b0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `bdffd3e9-4144-4007-a025-5ca78ddc0829` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta tem o Hub Qdrant como memória central....'
- **Texto:** A abordagem atual do sistema multi-porta e do Hub Qdrant como memória central foi documentada.

### `3825eb69-cef6-432e-926b-23a8b3c59361`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f221a7c4-7bc6-4bd4-a904-f11722c2f1a9` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-mult...'
- **Texto:** Há três demandas paradas em dialogos/inbox-claude-code/: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md (este é um template, não é demanda).

### `ef08fe7a-0fe8-414f-a4ac-a16251d5a225`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f221a7c4-7bc6-4bd4-a904-f11722c2f1a9` (Jaccard ≥ 0.7). Manter 'Há 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-mult...'
- **Texto:** Existem três demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é d

### `7b152337-512c-47e3-9071-390211001025`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código + nos docs gus-XX atualizados.

### `38877c53-cd44-478e-aa99-4a331893a361`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** No estado final dos PRs já está no código + nos docs gus-XX atualizados.

### `d9b72ad5-c7e6-4a90-b6f8-8f468e15528f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código + nos docs gus-XX atualizados.

### `71c22b64-51e3-4d05-85a7-d0d0e6e9ebaa`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código e nos docs gus-XX atualizados.

### `497cda5b-99dc-4336-a64e-2e210853ae2f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** o estado final dos PRs já está no código + nos docs gus-XX atualizados.

### `ff6e29d7-b3ce-47be-ad1f-6069b43270f5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `956401b6-b89e-4868-a462-2077fa855983` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs está no código e nos documentos atualizados.

### `58fbd48b-dd80-4ba6-847c-9dc80e4ca84a`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b5cb7a3c-0000-49e8-b30d-aa41abd3f431` (Jaccard ≥ 0.7). Manter 'Identidade e arquitetura do projeto Gus, com sistema multi-porta (Telegram, Clau...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) opera com um Hub Qdrant como memória central.

### `3d4b46cb-e68e-4a96-908b-2895783e5c10`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b5cb7a3c-0000-49e8-b30d-aa41abd3f431` (Jaccard ≥ 0.7). Manter 'Identidade e arquitetura do projeto Gus, com sistema multi-porta (Telegram, Clau...'
- **Texto:** O projeto Gus possui um sistema multi-porta que conecta Telegram, Claude Code, Claude Chat, além de futuros como Custom GPT e Alexa, com um Hub Qdrant como memória central.

### `9695d747-5e64-4adc-be33-166938065e69`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b5cb7a3c-0000-49e8-b30d-aa41abd3f431` (Jaccard ≥ 0.7). Manter 'Identidade e arquitetura do projeto Gus, com sistema multi-porta (Telegram, Clau...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) utiliza o Hub Qdrant como memória central.

### `3df1ee4c-23a6-4f7a-8823-a1aa2163e630`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a865bbc0-f532-42c6-88a1-dd81a8ee765b` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant + curador híbrido coleta dual rola até 12/05....'
- **Texto:** O curador híbrido coleta dual rola até 12/05.

### `761c2cad-4906-4a1e-8d0e-6aaf79c48eb7`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `43d0fcc6-b67e-4946-9256-b6ff29374154` (Jaccard ≥ 0.7). Manter 'O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot das 03h....'
- **Texto:** O Hub é mais fresco do que `gus-estado-atual.md`, que é um snapshot gerado às 03h.

### `ded231c6-5b88-462d-b6b5-d01b5bbc0a3c`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `43d0fcc6-b67e-4946-9256-b6ff29374154` (Jaccard ≥ 0.7). Manter 'O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot das 03h....'
- **Texto:** O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h.

### `4619c606-ab9f-42f1-b44f-77736abdb637`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e2876493-006e-449e-924e-c7f0ada4dffa` (Jaccard ≥ 0.7). Manter 'O Hub está ocioso há 6 horas....'
- **Texto:** O Hub está ocioso nas últimas 6 horas.

### `689621f3-4494-41d4-8dc6-5ba2e3d8b0a1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa, sugerindo que o refresh token OAuth pode ter expirado.

### `48a3a8bd-71a4-4b1d-ba6f-e817f8696e87`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e pode ter a hipótese de que o refresh token OAuth expirou.

### `5044dd04-03c7-4d30-b84d-a390a7eeaa11`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'
- **Texto:** O Drive sync está parado — demanda `2026-05-01-drive-sync-oauth-fix.md` ativa. Hipótese: refresh token OAuth expirou.

### `e4aaf847-da4c-4a07-8427-313a77813d3e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese de refresh token OAuth expirado.

### `f1c4a301-7b70-4697-8ddc-b1fc7d5581e0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `9c25e476-1285-430f-aeb8-191ab349be4d` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve a hipótese d...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e relacionada ao refresh token OAuth que pode ter expirado.

### `4a4f09df-4e39-4b9b-8cc8-07f7de4c8952`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6a882dc0-b241-4316-98f2-1c5a4d366487` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta com Hub Qdrant é a memória central do projeto Gus....'
- **Texto:** O Hub Qdrant é a memória central do sistema multi-porta.

### `56002b6c-7d72-4a3d-85a9-ace2e775b0d8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6a882dc0-b241-4316-98f2-1c5a4d366487` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta com Hub Qdrant é a memória central do projeto Gus....'
- **Texto:** O bot Telegram usa um sistema multi-porta com o Hub Qdrant como memória central.

### `ad123099-012a-42d3-bdac-264b6132d277`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6a882dc0-b241-4316-98f2-1c5a4d366487` (Jaccard ≥ 0.7). Manter 'O sistema multi-porta com Hub Qdrant é a memória central do projeto Gus....'
- **Texto:** O Hub Qdrant é utilizado como a memória central do sistema multi-porta.

### `8aa3c2cf-e0ec-4079-944d-242c7fcf22ee`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `559b1f78-6b75-45f0-8f32-8c1e0728bd96` (Jaccard ≥ 0.7). Manter 'O projeto utiliza um sistema multi-porta com Hub Qdrant como memória central....'
- **Texto:** O projeto Gus integra o sistema multi-porta com Hub Qdrant como memória central.

### `999a3322-f54b-4abe-9a27-b6e6c6c65d7d`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `839e1b47-b1c5-4585-8bc5-fa93a6ff2ff0` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant (`gus_hub`) como memória central + GitHub `Gustpbbr/Gus` como conhecimento + Drive como espelho.

### `5862b26a-831b-4548-b01b-4f8598ff6520`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `839e1b47-b1c5-4585-8bc5-fa93a6ff2ff0` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O projeto Gus tem um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.

### `5af68fb4-072f-4fb4-87a9-c8d0106b2e32`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `75e6e624-cbfa-4af0-9fab-836864ce85b7` (Jaccard ≥ 0.7). Manter 'O Hub teve 19 fragmentos no brain `gustavo`, e o sistema estava ocioso nas últim...'
- **Texto:** O Hub tem 19 fragmentos no brain `gustavo`, sistema ocioso nas últimas 6 horas.

### `7ccf5cb7-ac4e-4a19-a77d-5ddee8da7c45`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `627be3c7-fca0-4fd6-88f1-86f678cd8b60` (Jaccard ≥ 0.7). Manter 'A captura do Claude Code via cron salva transcript redatado, e o cron processa v...'
- **Texto:** Captura Claude Code via cron (PR #64, 01/05) — hook Stop salva transcript redatado, cron processa via curador 2x.

### `8f3a2cbb-921d-4466-8ae6-e86b6ffdfa0b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `70a8d959-cb6a-4d60-b47c-598662ac0ba2` (Jaccard ≥ 0.7). Manter 'O arquivo projetos/gus/_estado-atual.md informa onde paramos na sessão anterior....'
- **Texto:** O arquivo `projetos/gus/_estado-atual.md` mostra onde paramos na sessão anterior.

### `72525822-200c-45a6-998c-952ae16f786e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `bf8ec5aa-dccb-49a0-b18d-c997184a2d75` (Jaccard ≥ 0.7). Manter 'As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pen...'
- **Texto:** As demandas pendentes no inbox-claude-code incluem captura-multiporta-curador, drive-sync-oauth-fix, e pendencias-claude-chat-consolidacao.

### `d1c01427-0b32-4423-91f6-ea457128cf29`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `774231d1-e03a-401e-a757-17f8f89e8b9a` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` da pasta `projetos/gus` está desatualizado desde 27/04....'
- **Texto:** O `_estado-atual.md` da pasta projetos/gus está desatualizado e é de 27/04.

### `bcbea87f-68ac-4afd-adbd-814c5a1a080a`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `774231d1-e03a-401e-a757-17f8f89e8b9a` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` da pasta `projetos/gus` está desatualizado desde 27/04....'
- **Texto:** O `_estado-atual.md` da pasta projetos/gus está desatualizado desde 27/04.

### `a477a3b2-0891-4b86-a15c-f791d79161b0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `774231d1-e03a-401e-a757-17f8f89e8b9a` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` da pasta `projetos/gus` está desatualizado desde 27/04....'
- **Texto:** O `_estado-atual.md` está desatualizado desde 27/04.

### `dda2a16e-f4b5-4a9e-a9ae-aae91492dc81`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `774231d1-e03a-401e-a757-17f8f89e8b9a` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` da pasta `projetos/gus` está desatualizado desde 27/04....'
- **Texto:** O `_estado-atual.md` da pasta projetos/gus está desatualizado, datado de 27/04.

### `7799fa97-77a8-47fa-bca0-9862dc79b4e0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8ec5aa19-6659-4c55-8d06-8ccf96721bcc` (Jaccard ≥ 0.7). Manter 'Decisão sobre o drive sync precisa ser feita: reset OAuth, Service Account ou ap...'
- **Texto:** A decisão sobre o Drive sync ainda precisa ser feita: pode ser reset OAuth, Service Account, ou aposentar completamente.

### `a8e9d4d5-13dc-49fd-a2e3-388ce8237fc6`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `85f98b86-b768-4fd5-82c2-3cc216794652` (Jaccard ≥ 0.7). Manter 'As duas demandas pendentes em dialogos/inbox/ são: 2026-05-01-drive-sync-oauth-f...'
- **Texto:** As 2 demandas pendentes são `2026-05-01-drive-sync-oauth-fix.md` e `2026-05-01-captura-multiporta-curador.md`.

### `a6017436-fb88-423e-bbe4-0d736dac06e2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f584e27e-d458-4b41-a921-481bca2c8256` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` pode ser resolvida por 3 opções: ...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` pode ter o refresh token OAuth expirado — opções: reset OAuth, Service Account ou aposentar Drive sync.

### `a6c5a45e-a894-4621-8728-dd31a8d15bf6`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f4a8f8ba-3b25-48f9-abd1-166a2434a121` (Jaccard ≥ 0.7). Manter 'Os 4 documentos fundamentais para qualquer aba nova são `dialogos/_bootstrap/gus...'
- **Texto:** Os principais documentos obrigatórios para qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_est

### `ade258df-f5fd-43b5-952e-908cfe28c4d1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e9710909-43c4-4b70-a417-efb1cebd0629` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` está desatualizado e não reflete as últimas atualizações do...'
- **Texto:** O arquivo _estado-atual.md (27/04) está desatualizado e não reflete as últimas atualizações do git.

### `b4f9b6f6-cd79-4b72-8481-8adec33b594e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `f184bc91-cd10-4ca7-9c36-c7054d3b689c` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` do projeto está desatualizado desde 27/04/2026....'
- **Texto:** O arquivo `_estado-atual.md` está desatualizado desde 27/04/2026.

### `edeb7d07-8233-4f82-82b8-e8f277e3785e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `cfff1d65-1e8f-455a-80d6-2d669b368f66` (Jaccard ≥ 0.7). Manter 'Os 4 documentos pendentes são: captura-multiporta-curador, drive-sync-oauth-fix,...'
- **Texto:** O projeto tem quatro demandas pendentes: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um arquivo de template.

## Brain `gus` — severidade medio (12 candidatos)

### `0571de21-d4a8-491c-9648-ea326674a9b7`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** As informações foram registradas como memórias pessoais de Gustavo sobre filmes, gostos e experiências de vida.

### `325d51f5-00c1-428d-857b-3b10f70a3b73`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Gosto de mergulho com cilindro.

### `335e9d53-b4f8-4e74-ba58-38d9f1e47d97`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Gosto de lasanha.

### `3c90982e-aa5c-4c7e-8139-1acaf5d3b2f3`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Gosto de mergulho com cilindro.

### `46a52a89-5ec9-493d-9241-f44180882efc`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Meu filme preferido é Moulin Rouge.

### `47962975-311a-48eb-a727-bdcce29820e1`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Amei o filme do Michael Jackson.

### `4a1f6600-4c3b-4087-8db4-8a6439e1d11c`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Gosto de lasanha.

### `657347c7-b2b7-48b0-bbbe-b7d645478a7e`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Já tive um cachorro chamado Ralph.

### `863b1659-f7b8-4a5e-ad06-d401862a277d`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Para OS do Dimagem, o padrão de resposta obrigatório é:

OS Dimagem detectada (DD/MM/AAAA):
  + NOME · EXAME(S) · Convênio · —

Pacientes já no MD do dia (N):
| NOME | DATA | EXAME | PLANO | — |
...



### `9ce9a144-71c2-4587-b6f5-79385b400445`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Amei o filme do Michael Jackson.

### `a0211b7b-2a68-4e0b-9454-457c1d6b0b3b`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Meu filme preferido é Moulin Rouge.

### `f53183d9-de99-48d3-92f3-5051b229cc7e`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** Já tive um cachorro chamado Ralph.

## Brain `gustavo` — severidade forte (157 candidatos)

### `11ee6292-6906-4820-89b0-56005b7b6490`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.

### `17ba67f9-a0bb-4a2c-96df-8ab15fe39fab`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `197f5c64-323f-4f5d-8018-d89ac8afd4fc`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e está em produção.

### `1cc7c09a-0324-4a84-8253-2e37357c8306`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram possui ~21 ferramentas distintas implementadas.

### `1e2f645a-b47f-4a6d-bad2-2d42d4653f58`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `25a73b47-904f-45fc-a707-ca8ffc9ea1fd`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.

### `2a913367-8b32-44ba-bd92-6da7cf12ebcf`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/` no projeto.

### `2e698a75-778e-474b-a053-8141e1c47dc3`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O hook do retro-engine registra 'no-op: anthropic_missing' e continua a execução normalmente, seguindo o fluxo padrão.

### `2e9ab5df-c5b3-4806-b8b8-e305e83273a7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `2f5d2c55-9acc-4dab-a126-b4068b2b9621`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O arquivo de log do retro-engine gerou uma mensagem de erro 'anthropic_missing'.

### `3163aab6-f206-4648-b810-b8a70e398d94`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.

### `3569cd9f-63a3-43dd-a003-e5ac624b4521`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui cerca de 21 tools e está em produção no Railway.

### `3ae83f5d-3ba3-496d-a550-60473db77ab9`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, em produção Railway.

### `3ede6ef6-2312-4570-8c97-f0142cb0fe7d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A auditoria do Chat envolve tanto a porta Claude Chat (claude.ai) quanto o sistema operacional que a alimenta.

### `412b8a37-4893-4337-b05a-2570cd0d0c28`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) conta com ~21 tools, multimídia, caching de prompts e foi desenvolvido para operar continuamente em Railway.

### `43f8754a-5606-493b-89fd-00250d3e8bb5`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas na pasta `dialogos/inbox-claude-code/`.

### `441c248c-0b53-4e2a-8aba-ce078f6c989d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.

### `474e334c-efb3-4f4a-a777-a91e857beb2d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** 1. Gustavo quer que o Gus tenha capacidade de disparar todos os 8 workflows disponíveis manualmente (auditoria-mem0, briefing-matinal, check-saude, export-mem0, reflexao-quinzenal, retrospectiva-seman

### `47e69c03-ffe7-4f77-bf85-7fc7905f85c3`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e usa o Hub Qdrant como memória central.

### `4d107112-c42f-48bd-858a-f4414ff09a3a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `58191f85-adc2-4d8e-9d8d-6aa24b617cfe`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `593497ee-c359-4164-a3f2-78e668819b43`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `5b04f14c-575e-4d2d-9c04-c2d127ce98bf`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Os JSONs estruturados na pasta designada devem ser registrados.

### `5cc4a7d0-f327-4f8f-b47e-893661b7f83d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é dema

### `5e82d968-6f8b-4633-a37c-f84901a369b8`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.

### `63b7efb0-0cc2-4032-a4a8-941cd9be3e40`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Gus viu 4 demandas pendentes no `dialogos/inbox-claude-code/`.

### `6430c832-35ad-4810-b2d2-25bdb88d887e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`. As demandas são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template chamado `_frontmatte

### `64fac931-f007-47cc-a047-6f2586462977`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `6c44e7af-5fdf-4969-8f58-73a3c834323a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.

### `6ccbd02b-91db-4b75-9329-b994fcb21f0d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O resumo do log do retro-engine para esta sessão é: 'Fragmentos extraídos: 0, Salvos no Hub: 0, Erros: anthropic_missing'.

### `6d3bac7b-6536-465c-9142-401d99d51e4b`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O log do retro-engine registrou um no-op por falta de `ANTHROPIC_API_KEY` no ambiente.

### `74fab2c8-f6d9-4e9a-9556-338a54af4112`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em dialogos/inbox-claude-code/.

### `791ba715-411d-45d7-957e-e49d1abc031e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.

### `8a565c5a-036e-446c-b5f7-c8f0370e049c`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `8d245742-b849-469e-ab36-706bb4a56691`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `907a961e-889c-4dce-9748-a92dfa1288ef`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.

### `962a9564-4e03-4e18-a602-2cd502f36de0`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.

### `9bc41fae-cab9-40b2-ab3b-9088973291b5`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em dialogos/inbox-claude-code/: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md (este é template, não é demanda).

### `9cb9ffed-94eb-4e3a-b620-6cc212c021d9`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Atualmente, o TioGu apresenta 21 ferramentas, que estão organizadas em um arquivo chamado tools.py. Essas ferramentas incluem funções para manipulação de mídia e interação com APIs de LLM.

### `a33b0c64-f2ef-4761-9e90-49ae7775d80a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O commit do log do retro-engine foi realizado na branch `claude/project-discussion-fkfA8`.

### `a6254d36-b7d7-4073-9505-1112fa8fda00`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `a719a311-29fc-4af4-be3a-1b4911b5c0ea`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram, chamado TioGu, possui cerca de 21 ferramentas, multimídia, prompt caching e comunicação com o Hub Qdrant.

### `a8062889-2016-4e2a-8547-1bfa26d6e408`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Foram criados 2 JSONs estruturados com exames laboratoriais.

### `aac607f7-80af-4c62-966c-a21dd36e818a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Os JSONs estruturados de exames LAFE de novembro de 2019 estão no caminho Gus-Sync/pessoal/saude/gus__2019-11-18__lafe.json.

### `ad2018ed-8953-418f-afb9-be4f6ff372e9`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.

### `b0d1665f-f7cf-41d4-b11d-d166258afd83`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.

### `b4b4e2da-2dbf-4303-be4e-db15f4159290`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.

### `b7d98063-98d5-42c1-b98a-1dd48a46b753`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.

### `bf9c4684-95df-46f9-9997-20ecf3615f5e`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem 21 tools, multimídia, prompt caching e está em produção no Railway.

### `bfc91e32-2677-4a37-9e65-339e248da48a`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.

### `c01dc92d-6ce1-4acd-9a8c-548e603a02f7`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** A auditoria do Chat foi concluída e vários problemas foram identificados, incluindo questões de segurança, confiabilidade e arquitetura.

### `c12b221c-ee3b-4600-843e-b980cbe2ff67`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.

### `c3c8707d-621f-4406-af1f-8d35e188c55d`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.

### `c6fc24ab-bf64-4a6b-9c1f-bffba32fd365`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (template, não é demanda).

### `cd3757a2-c195-46bf-b82f-23648e729ccf`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.

### `d2144b70-4ad4-4e69-ad11-84fd346d619f`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.

### `d4088d24-3b71-4b4d-acd6-90aa0fbb8708`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram, TioGu, possui cerca de 21 ferramentas.

### `d474f322-9ced-4728-a6d3-a70ece317685`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, e está em produção no Railway.

### `d59e6091-8147-4a58-9705-53a776131c74`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O sistema usa um Bot Telegram chamado TioGu, que possui cerca de 21 ferramentas.

### `d5d4f0e2-bcf0-4081-ba9c-e11e1b29ee6c`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é d

### `dccdb3c2-eb99-47ce-93f7-8bbdbb8e5408`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Há 3 demandas paradas em dialogos/inbox-claude-code/

### `dcfc8d5f-db8b-4af8-b33f-d744bf580fdf`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram possui ~21 tools, multimídia, prompt caching em produção.

### `de09038a-ba2a-458f-925f-b17f8dcf2aef`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Os logs do retro-engine indicam 'no-op: anthropic_missing' devido à falta da variável ANTHROPIC_API_KEY na porta Code.

### `ec7013c7-846d-40cc-922d-6b8d23a34b16`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Os JSONs estruturados na pasta designada devem ser registrados.

### `f5a0ac4a-8ba6-4a33-a8a6-e879db1f8d42`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O log do retro-engine desta sessão não conseguiu extrair fragmentos devido à falta de `ANTHROPIC_API_KEY`.

### `f9addcd5-df9d-4827-b6f8-93911d6b36a6`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.

### `fa09b00a-c2c3-453d-9a6c-69af865fc5a5`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e opera em Railway.

### `fba7614c-8ec7-4bd3-af9f-183a5d5ea0d3`
- **Razão:** META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico
- **Texto:** Os JSONs estruturados de exames LAFE de janeiro de 2026 estão no caminho Gus-Sync/pessoal/saude/gus__2026-01-27__lafe.json.

### `e0e4d167-c367-4939-a613-5bea5386b7b3`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.

### `a8e62519-9563-4f19-8ebb-3294b3e2adbc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda de captura multiporta Claude Chat (`2026-05-01-captura-multiporta-curador.md`) está parcialmente resolvida, mas falta o gatilho proativo no Chat.

### `b38c5979-ec69-452a-b929-772292d940f0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.

### `7acf539b-a947-41c5-8929-9c9f140168e7`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.

### `1a3014c4-fee6-4d45-8df5-f0e25bcbc87c`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.

### `034f0fd0-2e3d-4d7d-bc7e-5367cc26eeff`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `8fcd312e-4042-426d-9da3-38f36dd6a048` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` é parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.

### `03e7576c-baeb-4d18-b2db-cffbcb60f24b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `79d2e601-8103-48ec-85d5-95b787c62dd9` (Jaccard ≥ 0.7). Manter 'A captura Claude Code via cron processa transcripts redatados, cron salva transc...'
- **Texto:** A captura Claude Code via cron salva transcripts redatados a cada 30 minutos.

### `39fae098-b279-4fd0-8656-f0b8d4d82868`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `9f515f94-fcb6-454d-9356-76868f7b0cdd`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois.

### `84663395-6141-4537-bc6b-6ad124db85fa`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** `gus-estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.

### `70363d48-3d06-4aee-828b-137acdbff4f5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` está bem desatualizado - o git log mostra muita coisa depois.

### `0c4e3b97-25a4-4354-aebc-1248f121a8b6`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `862e5300-44d2-42b1-afb3-e044986bfd5e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.

### `ae66e8b1-6942-4117-bf9f-21da121c2528`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `6362eb2b-ceeb-4092-97c0-44b2fccc3356`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `f3141a5a-d48d-4d28-986d-ef84ef3aecbe`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado em relação ao git log que mostra muita coisa depois.

### `cf2f79f3-cf85-4342-aba8-7064a2ad1c34`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — o git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67).

### `96bf8cbb-a341-425d-b1dd-03656bb467d5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `d9dc1854-423f-4331-9501-6932cd238180`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `bb648b8a-e88b-44b1-8491-375c769d2224`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d4a304d8-1482-4ba0-a801-443a34e8f1fb` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa...'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).

### `12a0ac32-9540-44c4-aea8-d9dea9d23570`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `87857940-8e7d-4728-b18b-add306aa7294` (Jaccard ≥ 0.7). Manter 'O arquivo `dialogos/_bootstrap/gus-bootstrap.md` é o manual operacional do Gus, ...'
- **Texto:** O arquivo 'dialogos/_bootstrap/gus-bootstrap.md' é o manual operacional do Gus, contendo as regras de comportamento e como cada porta usa o Hub.

### `0e28a744-94fe-4ab1-a1c2-b95bf3932f13`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `87857940-8e7d-4728-b18b-add306aa7294` (Jaccard ≥ 0.7). Manter 'O arquivo `dialogos/_bootstrap/gus-bootstrap.md` é o manual operacional do Gus, ...'
- **Texto:** O manual operacional do Gus, regras de comportamento e como cada porta usa o Hub estão no arquivo `dialogos/_bootstrap/gus-bootstrap.md`.

### `4cb234e1-0b18-4710-8d54-2b185dc7d247`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `85e9ff8a-f383-4b91-b525-1564fa149ad8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `11d2eb39-72f5-42db-96a7-c361830a0141`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `ffeedd0a-2f62-4426-85c5-cc948147be92`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.

### `ded7724a-f85d-4204-93ac-e07ed129e2d8`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.

### `2c0fc065-e966-4758-ab83-54a911e88cfe`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4dcda02d-b813-4a1e-8b98-b02bd2d38384` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decis...'
- **Texto:** A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.

### `567ab796-00fe-4664-b3e2-6db9648d7cd2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `593497ee-c359-4164-a3f2-78e668819b43` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`....'
- **Texto:** Existem três demandas paradas em `dialogos/inbox-claude-code/`.

### `76c7553a-bee8-41a8-ab66-2f44a0cb3ea2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `15554770-64b2-4cad-a7c6-d7cd3f3b83fa` (Jaccard ≥ 0.7). Manter 'O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h....'
- **Texto:** O Hub é mais fresco que `gus-estado-atual.md` (que é snapshot das 03h).

### `3beef49d-2466-414a-a32a-2a1f84194468`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.

### `1d2d166f-8c54-4969-877e-f578c85b5a4c`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.

### `94722ee0-f393-4451-ae65-adb57db10616`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `d3217996-1f0b-466f-9b2a-4703eabfd291`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.

### `24160757-ef37-496b-a351-729725c1cdfc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `51fd36cd-a2e7-4349-8968-fc7c021737d2` (Jaccard ≥ 0.7). Manter 'Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`....'
- **Texto:** Gus está na porta Code, branch `claude/initial-setup-iWTfL`.

### `f9e3fb57-90a9-4829-9b13-81dfd1e45f4c`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d60091e2-0729-4fd6-915c-ac47a1277cc5` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** Os arquivos incluem `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.

### `7146d9d8-2be4-4003-a58e-fb20338eda17`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d60091e2-0729-4fd6-915c-ac47a1277cc5` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** As demandas paradas são: '2026-05-01-captura-multiporta-curador.md', '2026-05-01-drive-sync-oauth-fix.md', e '_frontmatter-referencia.md'.

### `210f9c5f-55d7-461b-b798-0c27924dee06`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `d60091e2-0729-4fd6-915c-ac47a1277cc5` (Jaccard ≥ 0.7). Manter 'As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01...'
- **Texto:** Os arquivos das demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.

### `241d81c1-f0b1-4c82-bdfd-ce89b26ac0c1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `823eab03-34c5-498e-a2da-c756983bbc6d` (Jaccard ≥ 0.7). Manter 'O bot TioGu tem uma arquitetura baseada em um sistema multi-porta com Hub Qdrant...'
- **Texto:** O bot TioGu utiliza um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.

### `ae36fb96-0190-4e1a-a4c9-74341db15a6d`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `24de68a8-ff3f-45b6-915f-d2a03e00e87b` (Jaccard ≥ 0.7). Manter 'O bot possui uma funcionalidade de caching de prompts que reduz o custo de input...'
- **Texto:** O bot possui prompt caching que reduz o custo de input em janelas de 5 minutos.

### `ede0b581-84df-4e2f-a4ea-585b5f515b9b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6c44e7af-5fdf-4969-8f58-73a3c834323a` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiport...'
- **Texto:** Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.

### `407238bb-36b7-4143-b9a2-fc9d38eaf530`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6c44e7af-5fdf-4969-8f58-73a3c834323a` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiport...'
- **Texto:** As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.

### `4b78f038-155e-4874-a720-925a5ef6905b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `6c44e7af-5fdf-4969-8f58-73a3c834323a` (Jaccard ≥ 0.7). Manter 'Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiport...'
- **Texto:** As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.

### `b9a1c965-49f6-4924-8280-5088f50d8ce9`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b2ec58bb-6275-4216-9844-a4b1cb0467f1` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67.

### `26fdde1b-665a-4355-8ba0-ffc4c8c33c28`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b2ec58bb-6275-4216-9844-a4b1cb0467f1` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida.

### `2ada262a-3b26-4886-9bb7-400cabde5308`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b2ec58bb-6275-4216-9844-a4b1cb0467f1` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.

### `71ab0497-8486-4201-8586-2e62fa421b13`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `b2ec58bb-6275-4216-9844-a4b1cb0467f1` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida...'
- **Texto:** A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.

### `cab7aa77-6a3a-4324-84e8-a3090db02d82`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado.

### `278a217e-c4ec-4713-bf55-d88c23f0f0c6`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` (27/04) está bem desatualizado.

### `81ab7bbd-5535-40d6-bf50-a09ce48417de`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` de 27/04 está desatualizado e não reflete PRs #57, #60, #63, #64, #67.

### `31f90fff-5423-45c4-b4ca-1c18aa0673f1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado e não reflete PRs #57, #60, #63, #64, #67.

### `68014ecc-f10a-4cf2-bdbd-66dd8539c959`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` está desatualizado, com data de 27/04.

### `6f8f27e9-ab72-4ba7-9ccc-99ea5568c41b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e029d738-b5fb-4086-b907-2ffca1e9a07b` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` (27/04) está desatualizado em relação ao git log....'
- **Texto:** O `_estado-atual.md` (27/04) está desatualizado.

### `e4c26156-95ac-4c9d-b9fd-fca8a761267e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** A demanda para Drive sync está ativa, com a hipótese de que o refresh token OAuth expirou.

### `5a18b566-3dc6-4ba2-b96d-7b7478320d74`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.

### `e6b5b067-d747-4915-ac3a-4412ee3c542e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa. Hipótese: refresh token OAuth expirou.

### `2a8ac1a7-30d5-4c14-9ca6-c8fdffa150dc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** O Drive sync está parado e a demanda '2026-05-01-drive-sync-oauth-fix.md' está ativa. A hipótese é que o refresh token OAuth expirou.

### `c7fef6b4-2acb-4018-9245-47b6e25616fc`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.

### `a0607331-d993-4259-acae-2cb7107c0719`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a5b801a7-95bd-4ca6-9786-23bf4bf4616e` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o r...'
- **Texto:** A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.

### `62ba8ee3-f56e-4b6a-95d1-d3727b6b13a5`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central + GitHub como conhecimento + Drive como espelho.

### `54c83a41-2d3e-4c8f-8363-8e23ca25960f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem o Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.

### `6ea8d14a-141e-4bca-85ab-43dd6e2eb9a9`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem como memória central o Hub Qdrant.

### `972b8eea-7b43-46aa-b0e2-4d4dd5643c8b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) utiliza o Hub Qdrant como memória central.

### `2c745f28-c214-4be9-a261-28336bdabef1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.

### `db784ef8-0708-4356-8862-c4535bad4c57`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O projeto Gus é um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.

### `e68be862-500b-4259-b142-1974c2d1900e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `35a887f9-2fcd-47d0-9f1a-04cb21a310de` (Jaccard ≥ 0.7). Manter 'Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Al...'
- **Texto:** O sistema multi-porta inclui Telegram, Claude Code, e Claude Chat, com Hub Qdrant como memória central.

### `c548335d-b2a9-45ce-bc70-d4d66ad68c04`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura...'
- **Texto:** Três demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (esse é template, não é demanda)

### `8721109f-3f6d-4883-b9cb-3dbac636188e`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura...'
- **Texto:** As demandas paradas em `dialogos/inbox-claude-code/` são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.

### `acd74892-817e-4bbf-833d-23c57dcdb6a3`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura...'
- **Texto:** O projeto contém três demandas paradas em dialogos/inbox-claude-code: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md.

### `63732ae2-aa3f-4527-aef6-97acb66cc029`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura...'
- **Texto:** As demandas paradas em `dialogos/inbox-claude-code/` incluem: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (template, não demanda).

### `acb561e7-44ea-4b1a-8f80-d243bc0d9ebd`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `c3c8707d-621f-4406-af1f-8d35e188c55d` (Jaccard ≥ 0.7). Manter 'Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura...'
- **Texto:** Três demandas estão paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é dem

### `31a2ed0b-6160-494e-8684-9fc67123eca0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `786baeaa-e0cb-41db-8c32-b2a22eb9d325` (Jaccard ≥ 0.7). Manter 'O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é um snapshot do Hub gerado ...'
- **Texto:** O arquivo `_estado-atual.md` foi gerado pelo cron às 03h e é um snapshot do Hub.

### `c50f2fce-916b-4851-8220-81b8ce501ee2`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `3744f3c7-6ff7-472d-b7bc-eac54ab61f94` (Jaccard ≥ 0.7). Manter 'A convenção de nomenclatura dos arquivos JSON é <paciente_id>__<data_coleta>__<l...'
- **Texto:** A convenção de nomenclatura de arquivos dos exames utiliza o formato <paciente_id>__<data_coleta>__<lab_curto>.json.

### `d78cdd87-0be5-4c15-8f0d-a6969a04060b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `391e1f0e-b212-4f4d-9007-8aaf3bf79b03` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-port...'
- **Texto:** O sistema multi-porta usa o Hub Qdrant como memória central.

### `85cf1be7-42df-4e45-b3d9-c23bc6a586f1`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `391e1f0e-b212-4f4d-9007-8aaf3bf79b03` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-port...'
- **Texto:** O sistema multi-porta possui o Hub Qdrant como memória central.

### `52e00069-4d25-4c78-9e75-db1b4ab755d7`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `391e1f0e-b212-4f4d-9007-8aaf3bf79b03` (Jaccard ≥ 0.7). Manter 'O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-port...'
- **Texto:** O sistema multi-porta do projeto Gus tem o Hub Qdrant como memória central.

### `f04edd94-f468-498a-ab94-0843d6b25330`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `4b4473d3-a02d-4c07-9235-ac30e53d88a3` (Jaccard ≥ 0.7). Manter 'A captura multiporta do Claude Chat precisa de um gatilho proativo no Chat, e is...'
- **Texto:** A captura multiporta no Claude Chat precisa de um gatilho proativo que não está implementado.

### `af668708-1e55-4a13-a0db-3c12b316182f`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a2d802c7-ae1d-4925-8849-d303169f49d9` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proat...'
- **Texto:** A demanda 2026-05-01-captura-multiporta-curador.md precisa de um gatilho proativo no Chat.

### `58d049b3-03ec-4e9a-aed4-d5e9de586689`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a2d802c7-ae1d-4925-8849-d303169f49d9` (Jaccard ≥ 0.7). Manter 'A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proat...'
- **Texto:** A demanda '2026-05-01-captura-multiporta-curador.md' precisa de uma mudança de gatilho proativo no Chat.

### `e8c44942-ace0-46ad-8a6f-bf54cd57d003`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `dc6bf108-7ec0-4a56-9f2f-820d27202d31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código e nos documentos gus-XX atualizados.

### `61abdf8d-8fbc-4e5c-bbd5-d868af518091`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `dc6bf108-7ec0-4a56-9f2f-820d27202d31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código e nos documentos gus-XX atualizados.

### `58fd08ab-bbd9-416a-a054-2c77ab7afef4`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `dc6bf108-7ec0-4a56-9f2f-820d27202d31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código + nos docs gus-XX atualizados.

### `58fad4f9-c76e-4ed6-98f0-c1263947880c`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `dc6bf108-7ec0-4a56-9f2f-820d27202d31` (Jaccard ≥ 0.7). Manter 'O estado final dos PRs já está no código e nos documentos gus-XX atualizados....'
- **Texto:** O estado final dos PRs já está no código e nos docs gus-XX atualizados.

### `e117e55f-4695-4250-858a-6f4a8ca38841`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `679c5bb8-76e4-4ba3-87eb-74b52f528c69` (Jaccard ≥ 0.7). Manter 'O core obrigatório deve ser lido em toda aba nova: dialogos/_bootstrap/gus-boots...'
- **Texto:** O core obrigatório em toda aba nova inclui 4 arquivos: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md`, e `projetos/gus/_estado

### `7419d36d-36cf-4462-9d15-decb246d19e0`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `84dca0e2-47a0-4592-b8fe-9e54cf881d9b` (Jaccard ≥ 0.7). Manter 'A auditoria identificou a necessidade de integrar uma lógica clara para hierarqu...'
- **Texto:** A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.

### `e9ddfccb-5e4d-4964-9593-54bc030e686b`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a20dbbce-0e07-46fe-aa3c-fa3da3f244d9` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` e `gus-26-status-consolidado.md` estão desatualizados e não...'
- **Texto:** Foi identificado que o '_estado-atual.md' e o 'gus-26-status-consolidado.md' estão desatualizados em relação a PRs recentes.

### `a58364d0-adb7-43a2-9899-bae924b4dacd`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a20dbbce-0e07-46fe-aa3c-fa3da3f244d9` (Jaccard ≥ 0.7). Manter 'O `_estado-atual.md` e `gus-26-status-consolidado.md` estão desatualizados e não...'
- **Texto:** O `_estado-atual.md` (27/04) e `gus-26-status-consolidado.md` (26/04) estão desatualizados.

### `b2104908-4320-4549-908a-1b668de2f1bb`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `a26681e1-c75c-4d08-80c2-d7cdd867d02a` (Jaccard ≥ 0.7). Manter 'O bot TioGu é um sistema multi-porta que se conecta ao Telegram e utiliza o Hub ...'
- **Texto:** O bot Telegram TioGu usa um sistema multi-porta com Hub Qdrant como memória central.

### `c0b557be-f7d7-44c9-b4f0-10f06364b3fb`
- **Razão:** DUPLICATA semântica do fragmento mais antigo `e4af60ca-b56b-4bf7-bebb-2c6aeb36eb4b` (Jaccard ≥ 0.7). Manter 'O arquivo _estado-atual.md está desatualizado com relação aos últimos PRs....'
- **Texto:** O arquivo '_estado-atual.md' está desatualizado em relação ao projeto.

## Brain `gustavo` — severidade medio (18 candidatos)

### `06caf6bb-f1ed-43f4-a9ea-424409b55743`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo é anestesiologista e trabalha com o Dimagem (clínica/laboratório de imagem).
2. Gustavo recebe ordens de serviço do Dimagem e precisa acompanhar pacientes agendados.
3. Preferência: Gus dev

### `0ccf0b81-5233-4636-ba85-6ef997b02073`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo estabeleceu protocolo específico de análise de fotos que deve ser seguido nas próximas conversas
2. Gustavo está processando múltiplas imagens de Ordens de Serviço (OS) médicas com datas hi

### `0f7a70ea-3e6c-4735-8ff1-45d0e8c8ba84`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo trabalha com um projeto chamado **NeuroGus** — chegaram 3 demandas novas no dia 28/04 (briefing, arquitetura, código v1)
2. Existe um sistema de **múltiplos canais de comunicação** com o Gu

### `11b98c82-75de-4d09-b6c9-c0f1d49e6ba1`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Caminho completo da pasta de demandas do Gus: `Gustpbbr/Gus/dialogos/inbox-tiogu/`
2. PR #14 foi mergeado hoje (protocolo de portas e tools) — Gustavo pode querer revisar a documentação nova sobre 

### `2b68d542-c7c5-4ef9-b72e-492bbaddb7fe`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdrant (evolução positiva)
2. Problema identificado: Hub Qdrant mostra 0 fragmentos para user_id=gustavo — curador acessíve

### `3c58cbb8-63ee-4c99-a944-3a50dd512149`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo quer que o workflow de migração Mem0 → Qdrant rode e que o auto_diagnóstico seja executado após conclusão.

2. Hub Qdrant está operacional com 4+ fragmentos (subiu de 2), migração em progre

### `6855c44f-9d55-41ac-abd3-a9582985b505`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo está em fase de testes e quer que o Gus dispare workflows sempre que solicitado, sem justificar que foi feito recentemente.
2. Workflow de importação de demandas roda em ciclos de 15 minuto

### `6b589952-ef9c-4a2e-b278-dffb347130ca`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo quer que Gus dispare workflows sempre que solicitado, sem justificativas de execução recente — workflow de importação roda em ciclos de 15min.

2. Bug resolvido em `download_content`: `Unic

### `772f611d-ca24-4811-8ca0-0c8ba486785b`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Caminho correto no Drive para Claude Chat escrever demandas: `Gus-Sync/dialogos/inbox-tiogu/`
2. Workflow `import-from-drive.yml` executa a cada 15min, puxa arquivos do Drive pro GitHub e notifica 

### `7ef3b811-8dd7-40d8-85d6-5fe604461613`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo executa regularmente workflows de sincronização GitHub → Google Drive (sync-to-drive-full.yml para sync completo e sync-to-drive.yml para incremental)
2. Tem uma pasta `sensivel/` no reposi

### `809ba3f9-18d9-4aa8-b62e-590c02eedb7d`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo prefere corrigir o script para ser tolerante a encoding inválido em vez de deletar arquivos — usa fallback (UTF-8 → Latin-1)
2. Erro técnico identificado: arquivo `2026-04-28T14-30__frontma

### `9608b85a-488f-4cd1-93c5-e7cf8a382214`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Bug resolvido: função `download_content` (linha 150) falhava com `UnicodeDecodeError` ao ler arquivo `frontmatter-referencia.md` salvo com encoding não-UTF-8 (provavelmente Windows-1252), continha 

### `9aabe8eb-56d7-4eac-8473-d81af43716c3`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo quer apagar pendências que estão ultrapassadas — decisão tomada de limpar o backlog desatualizado.
2. Hub contém 204 memórias no total (auditoria de 7:51 BRT).
3. Migração Mem0 → Qdrant ain

### `bf6e32f3-d8b9-4953-be09-327f17521f2f`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo trabalha com agendamento/gestão de pacientes para exames de RM (ressonância magnética).
2. Padrão de resposta esperado do Gus: formato com detecção de imagem, lista de pacientes já no siste

### `c95ad8c6-1944-42f2-b5b7-acf147f9c67d`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo dispara regularmente workflow `import-from-drive.yml` para sincronizar arquivos do Drive com GitHub — tempo de execução esperado é até 15 minutos
2. Gustavo prefere confirmação clara quando

### `cb860bdb-c58e-4ba8-89c4-3b44435cb557`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Hub Qdrant agora funciona corretamente — 2+ fragmentos salvos, merge resolveu o problema crítico; Gustavo pode enviar PDFs quando quiser.

2. Sistema de curador híbrido (Haiku + Sonnet em paralelo)

### `e414b653-94c9-4a62-a8df-9cb30e2b9855`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Schema atual do Mem0 é `gus-18` com campos: `tipo`, `area`, `campa_temporal`, `confiança` — não possui campo `origem` (source de telegram/chat/code).
2. Gustavo quer melhorias no schema documentada

### `f6dc75c7-fe7f-4855-8190-8355ee6eaae8`
- **Razão:** UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente
- **Texto:** 1. Gustavo trabalha com gestão de pacientes organizados por planos de saúde (Assim Taquara vs. outros planos: Intermédica + Leve Saúde)
2. Preferência por separar dados de pacientes em arquivos markdo

