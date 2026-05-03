---
tipo: estado-atual-vivo
gerado_em: 2026-05-03T18:12:48-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 03/05/2026 às 18:12 BRT

> Documento gerado automaticamente a cada 15 minutos lendo o Hub
> Qdrant. Substitui o snapshot estático das 03h pra Claude Chat ter
> contexto fresco do que o sistema sabe agora. NÃO editar manualmente —
> próxima execução do cron sobrescreve.

**Como o Claude Chat usa este arquivo:** lê no boot do modo Gus pra
complementar a identidade canônica em `gus-bootstrap.md` com o estado
dinâmico. Sem este arquivo, Claude Chat opera com lag de 21h.

## Decisões recentes

- [decisao/gus] A comunicação com a API do Mem0 SaaS deve ser verificada para confirmar a existência de conteúdos históricos e decidir sobre a eliminação do secret. _(via claude-code)_
- [decisao/projetos] A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT. _(via claude-code)_
- [decisao/projetos] A fase 4 do projeto envolve a promoção automática de fragmentos da memória de ativo para estável após 30 dias. _(via claude-code)_

## Meta-reflexões ativas

- [meta_reflexao/gus] Se um PR precisa ser lido pra entender o presente, é sinal de doc desatualizado — não de PR importante. _(via claude-code)_
- [meta_reflexao/projetos] O filtro e a tradução dos 204 fragmentos estão planejados para a Fase 5. _(via claude-code)_
- [meta_reflexao/projetos] O plano de saneamento da memória inclui 9 itens, sendo essa fase crítica para evitar poluição futura da base de dados. _(via claude-code)_
- [meta_reflexao/gus] A futura auditoria (no fluxo do projeto) deve rastrear `motivo` do delete com mais evidência e relatar mudanças relevantes no hub Qdrant. _(via claude-code)_
- [meta_reflexao/gus] O Hub atual já tem 70% de meta-lixo — não vale arriscar mais. _(via claude-code)_

## Fragmentos das últimas 6h (4 de 50 no brain)

- [decisao/projetos] A demanda `sync-to-drive.yml` deve ser validada após a instalação do WIF e o saldo do Anthropic. _(via claude-code)_
- [fato/projetos] Haiku do curador não roda sem créditos. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` na pasta projetos/gus foi atualizado em 27/04 e está desatualizado para o processo atual. _(via claude-code)_
- [procedural/gus] O script `limpeza_hub_dryrun.py` gera relatório de IDs candidatos a delete sem afetar a base atual. _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 3214 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 37
- `identidade_operacional`: 4
- `decisao`: 4
- `rotina`: 1
- `projeto`: 1
- `episodico`: 1
- `lacuna`: 1
- `procedural`: 1

## Auto-observações do Gus (brain `gus` — 3153 fragmentos)

- [decisao/gus] Há necessidade de um script que pareie os resultados de Haiku e GPT para avaliação de desempenho antes da escolha final do modelo a ser adotado. _(via claude-code)_
- [decisao/gus] O Mem0 SaaS é um vetor de perda contínua se ainda escreve dados. _(via claude-code)_
- [cronologico/projetos] A coleta de modelos no curador (Haiku × GPT-4o-mini) está programada para terminar em 12/05/2026. _(via claude-code)_
- [fato/projetos] Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`. _(via claude-code)_
- [fato/gus] A stack de memória está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados. _(via claude-code)_
- [fato/gus] Hub Qdrant é a fonte da verdade. _(via claude-code)_
- [fato/gus] A URL /mcp deve retornar 404 Not Found ou JSON com erro após a adição do MCP_URL_SECRET. _(via claude-code)_
- [fato/projetos] O estado final dos PRs já está no código + nos docs gus-XX atualizados. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
