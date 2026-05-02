---
tipo: estado-atual-vivo
gerado_em: 2026-05-02T13:51:38-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 02/05/2026 às 13:51 BRT

> Documento gerado automaticamente a cada 15 minutos lendo o Hub
> Qdrant. Substitui o snapshot estático das 03h pra Claude Chat ter
> contexto fresco do que o sistema sabe agora. NÃO editar manualmente —
> próxima execução do cron sobrescreve.

**Como o Claude Chat usa este arquivo:** lê no boot do modo Gus pra
complementar a identidade canônica em `gus-bootstrap.md` com o estado
dinâmico. Sem este arquivo, Claude Chat opera com lag de 21h.

## Decisões recentes

- [decisao/projetos] A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT. _(via claude-code)_
- [decisao/projetos] Aba nova só precisa olhar PRs se houve uma quebra específica que depende do PR mais recente. _(via claude-code)_
- [decisao/gus] Gustavo pediu um panorama geral do projeto antes de focar em um assunto específico. _(via claude-code)_

## Meta-reflexões ativas

- [meta_reflexao/projetos] A meta é estabilizar o caminho crítico com testes e reconciliar as documentações com o código devido ao drift. _(via claude-code)_

## Fragmentos das últimas 6h (20 de 50 no brain)

- [fato/gus] O PR #67 introduziu um curador bidirecional no Chat, utilizando Sonnet 4.6 e GPT-4o. _(via claude-code)_
- [fato/projetos] O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template. _(via claude-code)_
- [fato/projetos] O modelo do Chat pode salvar fragmentos sobre Gustavo no brain `gus` sem validação. _(via claude-code)_
- [fato/projetos] A estrutura atual do sistema de escrita do projeto `claude-code` consiste em três canais distintos: escrita em tempo real através de MCP, upload de arquivos .md e demandas inbox. _(via claude-code)_
- [decisao/gus] Gustavo pediu um panorama geral do projeto antes de focar em um assunto específico. _(via claude-code)_
- [decisao/projetos] A captura em tempo real durante a conversa pode ser ativada para aumentar a interação e responsividade do Chat. _(via claude-code)_
- [fato/projetos] Houve um erro na sincronia entre o Heap e o Drive do Gus. _(via claude-code)_
- [decisao/projetos] O Hub deve utilizar URL secrets para aumentar a segurança. _(via claude-code)_
- [fato/projetos] O sistema de captura de fragmentos do Chat estava quebrado devido ao bug. _(via claude-code)_
- [preferencia/projetos] A atualização dos documentos de estado atual e de projetos deve ser feita sempre que houver mudanças significativas. _(via claude-code)_
- [decisao/projetos] A mudança de `drop_pending_updates` de True para False pode causar storm de mensagens em caso de downtime. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` é gerado pela automática a cada 15 minutos, oferecendo um snapshot do Hub. _(via claude-code)_
- [fato/projetos] A captura Claude Code via cron salva transcripts redatados a cada 30 minutos. _(via claude-code)_
- [fato/projetos] As capturas estão funcionando de forma assíncrona no cron GitHub Actions, processadas pelo curador, que já está rodando. _(via claude-code)_
- [decisao/projetos] A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT. _(via claude-code)_
- [decisao/projetos] A demanda de Drive sync (`2026-05-01-drive-sync-oauth-fix.md`) está ativa. Hipótese: refresh token OAuth expirou. Três opções: reset OAuth (paliativo) / Service Account (definitivo) / aposentar Dri... _(via claude-code)_
- [fato/projetos] O foco do projeto é desenvolver um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa). _(via claude-code)_
- [decisao/projetos] O `dimagem.py` é uma integração de domínio e deve ser movido para o diretório `integrations/` para refletir sua natureza. _(via claude-code)_
- [fato/projetos] Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`. _(via claude-code)_
- [fato/projetos] O sistema multi-porta com Hub Qdrant como memória central opera com GitHub como conhecimento e Drive como espelho. _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 257 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 31
- `decisao`: 9
- `episodico`: 5
- `lacuna`: 3
- `projeto`: 1
- `preferencia`: 1

## Auto-observações do Gus (brain `gus` — 258 fragmentos)

- [fato/projetos] O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta). _(via claude-code)_
- [fato/projetos] Existem 3 demandas paradas em `dialogos/inbox-claude-code/`. _(via claude-code)_
- [fato/projetos] PRs descrevem o caminho, não onde a equipe está atualmente em seu trabalho. _(via claude-code)_
- [episodico/-] As informações foram registradas como memórias pessoais de Gustavo sobre filmes, gostos e experiências de vida. _(via telegram-claude)_
- [fato/projetos] Os 4 arquivos obrigatórios para o contexto em toda aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_es... _(via claude-code)_
- [procedural/projetos] Para uma nova aba, o core obrigatório dá 80% do contexto: manual operacional, identidade do Gustavo, estado atual do Hub, e o estado atual do projeto. _(via claude-code)_
- [fato/projetos] A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat. _(via claude-code)_
- [fato/gus] Gus está na porta Code, branch `claude/initial-setup-iWTfL`. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
