---
tipo: estado-atual-vivo
gerado_em: 2026-05-03T11:36:46-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 03/05/2026 às 11:36 BRT

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
- [meta_reflexao/projetos] O plano de saneamento da memória inclui 9 itens, sendo essa fase crítica para evitar poluição futura da base de dados. _(via claude-code)_
- [meta_reflexao/gus] A futura auditoria (no fluxo do projeto) deve rastrear `motivo` do delete com mais evidência e relatar mudanças relevantes no hub Qdrant. _(via claude-code)_
- [meta_reflexao/gus] O Hub atual já tem 70% de meta-lixo — não vale arriscar mais. _(via claude-code)_
- [meta_reflexao/gus] As pastas do Gustavo no Drive devem ser: Chat, Code e TioGu. _(via claude-code)_

## Fragmentos das últimas 6h (20 de 50 no brain)

- [fato/gus] O sistema de agente pessoal multi-porta usa memória central no Hub Qdrant. _(via claude-code)_
- [identidade_operacional/gus] O Hub Qdrant é a memória central do sistema. _(via claude-code)_
- [fato/projetos] Apenas análise de estado final dos PRs ligado ao código e as documentações atualizadas. _(via claude-code)_
- [fato/projetos] Drive sync (WIF/PR #76) precisa estar verde para que o bootstrap atualizado chegue no Drive. _(via claude-code)_
- [fato/gus] Um total de 208 fragmentos foi exportado da Mem0 SaaS para o diretório de histórico. _(via claude-code)_
- [fato/gus] Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync). _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` da pasta projetos/gus está desatualizado de 27/04. _(via claude-code)_
- [fato/gus] O conteúdo no Mem0 SaaS possui maior qualidade em comparação aos fragmentos atuais no Hub. _(via claude-code)_
- [fato/projetos] O workflow de migração para o Hub revelou que não há fragmentos a migrar da coleção `gus`. _(via claude-code)_
- [fato/projetos] O workflow de migração `migrar_gus_para_hub.py` indica que não há fragmentos na coleção 'gus'. _(via claude-code)_
- [fato/projetos] O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas. _(via claude-code)_
- [decisao/projetos] A fase 4 do projeto envolve a promoção automática de fragmentos da memória de ativo para estável após 30 dias. _(via claude-code)_
- [identidade_operacional/gus] O Gus é um sistema de agente pessoal multi-porta que se comunica através de diferentes plataformas como Telegram, Claude Code e Claude Chat. _(via claude-code)_
- [identidade_operacional/gus] O Hub Qdrant é a fonte da verdade para o Gus. _(via claude-code)_
- [episodico/projetos] Os arquivos de estado do projeto sempre devem ser lidos, preferindo a consulta no Hub sobre o arquivo `gus-estado-atual.md`. _(via claude-code)_
- [decisao/gus] A comunicação com a API do Mem0 SaaS deve ser verificada para confirmar a existência de conteúdos históricos e decidir sobre a eliminação do secret. _(via claude-code)_
- [fato/gus] A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026. _(via claude-code)_
- [fato/projetos] O bot do Telegram, TioGu, possui cerca de 21 ferramentas. _(via claude-code)_
- [fato/gus] O status dos fragmentos que não são classificados polui o Hub com dados irrelevantes. _(via claude-code)_
- [fato/gus] Os '204 fragmentos históricos' estavam mesmo lá. Hipótese A8.1 confirmada: estavam no Mem0 SaaS (api.mem0.ai). _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 2697 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 36
- `identidade_operacional`: 5
- `decisao`: 3
- `projeto`: 2
- `rotina`: 1
- `episodico`: 1
- `lacuna`: 1
- `biografico`: 1

## Auto-observações do Gus (brain `gus` — 2634 fragmentos)

- [decisao/gus] Há necessidade de um script que pareie os resultados de Haiku e GPT para avaliação de desempenho antes da escolha final do modelo a ser adotado. _(via claude-code)_
- [decisao/gus] O Mem0 SaaS é um vetor de perda contínua se ainda escreve dados. _(via claude-code)_
- [cronologico/projetos] A coleta de modelos no curador (Haiku × GPT-4o-mini) está programada para terminar em 12/05/2026. _(via claude-code)_
- [fato/projetos] Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`. _(via claude-code)_
- [fato/gus] A stack de memória está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados. _(via claude-code)_
- [fato/gus] Hub Qdrant é a fonte da verdade. _(via claude-code)_
- [fato/projetos] O estado final dos PRs já está no código + nos docs gus-XX atualizados. _(via claude-code)_
- [fato/gus] Está com 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
