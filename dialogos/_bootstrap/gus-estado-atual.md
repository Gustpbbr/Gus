---
tipo: estado-atual-vivo
gerado_em: 2026-05-03T04:24:19-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 03/05/2026 às 04:24 BRT

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

- [meta_reflexao/gus] As pastas do Gustavo no Drive devem ser: Chat, Code e TioGu. _(via claude-code)_
- [meta_reflexao/projetos] Avanços futuros no projeto incluem a reescrita do system_prompt.md e a revisão de ferramentas e métodos utilizados na integração do bot. _(via claude-code)_
- [meta_reflexao/projetos] 4 memórias poluídas precisam ser deletadas manualmente. _(via claude-code)_
- [meta_reflexao/gus] O Hub Qdrant deve receber fragmentos úteis e consolidar as informações do Gus. _(via claude-code)_
- [meta_reflexao/gus] Curadores de memória devem ser mantidos atualizados para evitar a poluição de dados. _(via claude-code)_

## Fragmentos das últimas 6h (20 de 50 no brain)

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
- [fato/gus] O `auditoria_hub.py` é cego para o brain gus e as classificações são feitas somente por keywords. _(via claude-code)_
- [decisao/projetos] Foi decidido que a meta_reflexao do agente Gus deve ser capturada durante as conversas. _(via claude-code)_
- [decisao/projetos] A opção A para o conteúdo do Mem0 SaaS é mantê-lo em `historico/`, enquanto a opção C planeja filtrá-lo e traduzi-lo para importação futura. _(via claude-code)_
- [fato/gus] Gus é um sistema de agente pessoal multi-porta, integrando Telegram, Claude Code, Claude Chat e futuras plataformas como Custom GPT mobile e Alexa. A memória central fica no Hub Qdrant. _(via claude-code)_
- [fato/gus] O conteúdo no Mem0 SaaS inclui 204 fragmentos, com dados biográficos e preferências sobre o trabalho. _(via claude-code)_
- [decisao/gus] A memória anterior (Mem0 SaaS) está sendo aposentada e o Hub Qdrant é a nova fonte da verdade. _(via claude-code)_
- [biografico/gus] Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus. _(via claude-code)_
- [fato/projetos] O estado atual do projeto inclui o TioGu com 163 testes verdes, o Claude Chat com 12 fixes de 31 achados e pendências em várias áreas, incluindo a definição de `MCP_URL_SECRET` no Railway. _(via claude-code)_
- [rotina/projetos] Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`. _(via claude-code)_
- [decisao/projetos] A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat. _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 1118 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 30
- `decisao`: 8
- `procedural`: 3
- `identidade_operacional`: 2
- `projeto`: 2
- `rotina`: 1
- `lacuna`: 1
- `biografico`: 1
- `episodico`: 1
- `cronologico`: 1

## Auto-observações do Gus (brain `gus` — 1062 fragmentos)

- [fato/projetos] Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`. _(via claude-code)_
- [fato/gus] Hub Qdrant é a fonte da verdade. _(via claude-code)_
- [fato/gus] O conteúdo da coleção legada 'gus' está vazio, sem fragmentos a serem migrados. _(via claude-code)_
- [fato/gus] O passo 1 é necessário para proteger o MCP e liberar a escrita real-time do Chat. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta). _(via claude-code)_
- [fato/projetos] A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat. _(via claude-code)_
- [fato/projetos] As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus. _(via claude-code)_
- [fato/gus] As diretrizes de segurança para o MCP incluem a proteção com um URL secreto. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
