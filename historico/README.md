# `historico/` — material legacy ou de uso único

Pasta-arquivo. Tudo aqui pode ser deletado sem impacto na operação atual
do Gus (bot Telegram, Hub Qdrant, Claude Code, sync Drive, workflows).

Foi reorganizado em **2026-04-28** pra desinchar a raiz do repo
(GitHub web mostrava 18+ pastas misturando vivo e legacy).

## Critério "histórico" usado

Algo entra aqui se atende **TODOS**:

1. Não é importado por código vivo (`gus/`, `hub/`, `api/`, `.github/scripts/`)
2. Não é referenciado por workflow ativo (`.github/workflows/`)
3. Não é dado pessoal corrente do Gustavo (saúde, financeiro, projetos
   em andamento)
4. Não tem dependência cruzada com pastas vivas (acoes/, agenda/, etc.)

## Conteúdo

### `textos-antigos/`

Versões antigas (v1) dos arquivos de identidade e bootstrap, antes da
consolidação no `dialogos/_bootstrap/`. Manter apenas como referência
do que mudou:

- `gus-bootstrap-v1.md` — primeiro bootstrap pro Claude Chat
- `gus-identity-v1.md` — primeira versão da identidade do Gus
- `system_prompt-v1.md` — primeiro system prompt do bot Telegram

### `tiogubot/readme.md`

Pasta criada em 23/04 com placeholder "Conteúdo a ser atualizado".
Nunca foi preenchida. Provavelmente abandonada — TioGu hoje é só nome
do bot Telegram e não tem identidade própria separada do Gus.

### `scripts/test_railway_logs.py`

Script standalone usado **uma vez** pra testar integração Railway antes
de mergear o código de `logs_railway` na `gus/integrations/railway.py`.
Hoje a tool `logs_railway` cobre o caso de uso. Útil só pra reproduzir
debug do Railway GraphQL fora do bot.

### `docs/`

Setup docs feitos uma vez pra cada integração inicial. Conteúdo válido
mas referência pontual, não consultado regularmente:

- `drive-inbox-setup.md` — setup do Drive como inbox de entrada
- `drive-sync-setup.md` — setup do sync GitHub → Drive
- `gus-briefing-opus.md` — briefing pra modelo Opus
- `gus-entrevista-boas-vindas.md` — script de entrevista inicial
- `gus-extracao-sessoes-antigas.md` — extração de sessões pré-Mem0
- `gus-metricas.md` — definições de métricas (custo, latência)
- `gus-telegram-config.md` — passo-a-passo config Telegram

Já estavam excluídos do sync Drive (`sync_to_drive.py:EXCLUDE_PREFIXES`).
Ao mover pra `historico/docs/`, o exclude foi atualizado pra
`historico/` inteira.

### `get_token.py`

Script de geração de OAuth refresh token Google (usado pra `import_from_drive`,
`sync_to_drive`, etc.). Rodado uma vez.

⚠️ **Aviso de segurança**: este arquivo foi commitado no histórico do git
em `677e9c7` ANTES de ser adicionado ao `.gitignore`. **As credenciais
Google OAuth (CLIENT_ID + CLIENT_SECRET) estão expostas no histórico.**
Mitigação: revogar essas credenciais no Google Cloud Console e gerar
novas. O reset do CLIENT_SECRET neutraliza o vazamento. Expurgar do
histórico via `git filter-repo` é destrutivo e desnecessário se o
secret já foi resetado.

### `(deletado) resumo-financeiro.md`

Arquivo vazio de 0 bytes na raiz. Redundante com `pessoal/financeiro/overview.md`.
Não foi movido pra cá — apenas deletado. Registrado aqui pra rastreabilidade.

## O que NÃO virou histórico (e por quê)

- **`acoes/`** — fila de ações ativa, executor pendente mas estrutura usada
- **`agenda/`** — referenciada por `gus/integrations/wikilinks.py`
- **`receitas/`** — pequena mas é teu conteúdo pessoal
- **`api/`** — código FastAPI ativo (Custom GPT em desenvolvimento)
- **`capturado/`** — captura rápida ainda em uso
- **`_indices/`, `_log/`** — geram dados úteis automaticamente

## Posso deletar essa pasta inteira?

Sim, em princípio. Mas:
- Histórico do git preserva tudo (perda zero permanente)
- Se algum dia precisar reproduzir setup antigo (ex: refazer Drive sync), os
  passos estão nos `docs-*` aqui dentro
- Se alguém perguntar "como o Gus era no início?", os `*-v1.md` mostram

Recomendação: deixar até completar 6 meses sem ninguém abrir nenhum arquivo.
Aí avalia.
