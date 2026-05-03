---
tipo: estado-atual-vivo
gerado_em: 2026-05-03T07:18:29-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 03/05/2026 às 07:18 BRT

> Documento gerado automaticamente a cada 15 minutos lendo o Hub
> Qdrant. Substitui o snapshot estático das 03h pra Claude Chat ter
> contexto fresco do que o sistema sabe agora. NÃO editar manualmente —
> próxima execução do cron sobrescreve.

**Como o Claude Chat usa este arquivo:** lê no boot do modo Gus pra
complementar a identidade canônica em `gus-bootstrap.md` com o estado
dinâmico. Sem este arquivo, Claude Chat opera com lag de 21h.

## Decisões recentes

- [decisao/projetos] A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT. _(via claude-code)_
- [decisao/projetos] Foi decidido que a meta_reflexao do agente Gus deve ser capturada durante as conversas. _(via claude-code)_
- [decisao/projetos] A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat. _(via claude-code)_

## Meta-reflexões ativas

- [meta_reflexao/gus] Se um PR precisa ser lido pra entender o presente, é sinal de doc desatualizado — não de PR importante. _(via claude-code)_
- [meta_reflexao/projetos] O plano de saneamento da memória inclui 9 itens, sendo essa fase crítica para evitar poluição futura da base de dados. _(via claude-code)_
- [meta_reflexao/gus] O Hub atual já tem 70% de meta-lixo — não vale arriscar mais. _(via claude-code)_
- [meta_reflexao/gus] As pastas do Gustavo no Drive devem ser: Chat, Code e TioGu. _(via claude-code)_
- [meta_reflexao/projetos] O estado final dos PRs já está no código e nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente está. _(via claude-code)_

## Fragmentos das últimas 6h (20 de 50 no brain)

- [fato/gus] O status dos fragmentos que não são classificados polui o Hub com dados irrelevantes. _(via claude-code)_
- [fato/projetos] O curador Telegram apresenta erro 400 recorrente, resultando em apenas uma entrada por dia. Isso pode indicar que o ingesto do Chat também esteja falhando silenciosamente. _(via claude-code)_
- [fato/gus] Os '204 fragmentos históricos' estavam mesmo lá. Hipótese A8.1 confirmada: estavam no Mem0 SaaS (api.mem0.ai). _(via claude-code)_
- [fato/gus] O curador do Gus utiliza Haiku e GPT-4o-mini como modelos para processamento. _(via claude-code)_
- [fato/projetos] Há 3 demandas pendentes no `dialogos/inbox-claude-code/`. _(via claude-code)_
- [fato/gus] A captura de transcripts do Claude Code está quebrada desde 01/05. _(via claude-code)_
- [fato/gus] O MCP está público, permitindo que qualquer scanner leia todo o Hub. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` da pasta projetos/gus está desatualizado desde 27/04. _(via claude-code)_
- [fato/gus] A auditoria da memória é realizada diariamente, mas atualmente é cega para o brain 'gus' e ignora o campo 'area'. _(via claude-code)_
- [fato/gus] O Hub Qdrant atualmente contém 40 fragmentos, dos quais 70% são considerados lixo. _(via claude-code)_
- [identidade_operacional/gus] O Hub Qdrant é a fonte da verdade para o sistema. _(via claude-code)_
- [fato/projetos] Fragments recent itens têm um bug crítico do curador, com `format()` falhando 100% desde 30/04. _(via claude-code)_
- [fato/projetos] O estado final dos PRs já tá no código + nos docs gus-XX atualizados. _(via claude-code)_
- [fato/projetos] O bot do Telegram (TioGu) possui 21 ferramentas distintas integradas. _(via claude-code)_
- [fato/projetos] A stack de memória está em estado intermediário arriscado, com fallback ativo para a coleção legada 'gus'. _(via claude-code)_
- [fato/projetos] Os PRs mergeados post 02/05/2026 incluem melhorias no curador e correções de bugs críticos. _(via claude-code)_
- [fato/gus] O Gus é um sistema de agente pessoal multi-porta, operando em várias plataformas como Telegram, Claude Code e futuras integrações. _(via claude-code)_
- [projeto/gus] A proposta é criar a estrutura 'dialogos/Gustavo/' com subpastas para Chat, Code e TioGu. _(via claude-code)_
- [fato/projetos] Os itens da Fase 1 foram concluídos e incluem melhorias na auditoria, adição de tags e remoção de código obsoleto. _(via claude-code)_
- [procedural/-] Houve uma auditoria que revelou um estado intermediário arriscado da stack de memória, com problemas como 4 chamadas LLM por unidade de input sem mecanismo de deduplicação. _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 1633 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 36
- `decisao`: 4
- `identidade_operacional`: 2
- `projeto`: 2
- `procedural`: 2
- `rotina`: 1
- `lacuna`: 1
- `biografico`: 1
- `episodico`: 1

## Auto-observações do Gus (brain `gus` — 1577 fragmentos)

- [decisao/gus] Há necessidade de um script que pareie os resultados de Haiku e GPT para avaliação de desempenho antes da escolha final do modelo a ser adotado. _(via claude-code)_
- [decisao/gus] O Mem0 SaaS é um vetor de perda contínua se ainda escreve dados. _(via claude-code)_
- [cronologico/projetos] A coleta de modelos no curador (Haiku × GPT-4o-mini) está programada para terminar em 12/05/2026. _(via claude-code)_
- [fato/projetos] Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`. _(via claude-code)_
- [fato/gus] Hub Qdrant é a fonte da verdade. _(via claude-code)_
- [fato/gus] O conteúdo da coleção legada 'gus' está vazio, sem fragmentos a serem migrados. _(via claude-code)_
- [fato/gus] O passo 1 é necessário para proteger o MCP e liberar a escrita real-time do Chat. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta). _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
