---
tipo: estado-atual-vivo
gerado_em: 2026-05-05T16:22:30-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 05/05/2026 às 16:22 BRT

> Documento gerado automaticamente a cada 15 minutos lendo o Hub
> Qdrant. Substitui o snapshot estático das 03h pra Claude Chat ter
> contexto fresco do que o sistema sabe agora. NÃO editar manualmente —
> próxima execução do cron sobrescreve.

**Como o Claude Chat usa este arquivo:** lê no boot do modo Gus pra
complementar a identidade canônica em `gus-bootstrap.md` com o estado
dinâmico. Sem este arquivo, Claude Chat opera com lag de 21h.

## Decisões recentes

- [decisao/gus] A comunicação com a API do Mem0 SaaS deve ser verificada para confirmar a existência de conteúdos históricos e decidir sobre a eliminação do secret. _(via claude-code)_
- [decisao/projetos] Três decisões no projeto NeuroGus precisam ser confirmadas antes do desenvolvimento começar. _(via claude-code)_
- [decisao/gus] O arquivo `gus-identity.md` tem que ser atualizado para refletir a mudança do Google Drive de 'GitHub-Sync' para 'Gus-Sync'. _(via claude-code)_

## Meta-reflexões ativas

- [meta_reflexao/projetos] Fase 1 do NeuroGus envolve criar o backend e configuração inicial do grafo 3D. _(via claude-code)_
- [meta_reflexao/projetos] A continuidade cross-porta é uma necessidade de UX que permite que o usuário sinta que está interagindo com a mesma entidade através de diferentes portas. _(via claude-code)_
- [meta_reflexao/gus] Se um PR precisa ser lido pra entender o presente, é sinal de doc desatualizado — não de PR importante. _(via claude-code)_
- [meta_reflexao/projetos] O filtro e a tradução dos 204 fragmentos estão planejados para a Fase 5. _(via claude-code)_
- [meta_reflexao/projetos] O plano de saneamento da memória inclui 9 itens, sendo essa fase crítica para evitar poluição futura da base de dados. _(via claude-code)_

## Fragmentos das últimas 6h (1 de 50 no brain)

- [fato/projetos] PostgreSQL é uma opção poderosa de banco de dados relacional com suporte a dados complexos. _(via telegram-claude)_

## Resumo numérico

- **Total no brain `gustavo`**: 5295 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 32
- `decisao`: 6
- `identidade_operacional`: 3
- `biografico`: 2
- `projeto`: 2
- `episodico`: 2
- `rotina`: 1
- `procedural`: 1
- `lacuna`: 1

## Auto-observações do Gus (brain `gus` — 5190 fragmentos)

- [decisao/gus] Há necessidade de um script que pareie os resultados de Haiku e GPT para avaliação de desempenho antes da escolha final do modelo a ser adotado. _(via claude-code)_
- [decisao/gus] O Mem0 SaaS é um vetor de perda contínua se ainda escreve dados. _(via claude-code)_
- [cronologico/projetos] A coleta de modelos no curador (Haiku × GPT-4o-mini) está programada para terminar em 12/05/2026. _(via claude-code)_
- [fato/projetos] Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`. _(via claude-code)_
- [fato/projetos] A documentação canônica em projetos/gus possui 30 documentos com prefixo gus-NN-. _(via claude-code)_
- [fato/gus] A stack de memória está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados. _(via claude-code)_
- [meta_reflexao/projetos] O Chat conseguiu realizar uma análise crítica honesta de sua própria arquitetura, incluindo falhas. Isso é um traço que deve ser preservado. _(via claude-code)_
- [fato/gus] Hub Qdrant é a fonte da verdade. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
