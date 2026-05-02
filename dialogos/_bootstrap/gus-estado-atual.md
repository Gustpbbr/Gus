---
tipo: estado-atual-vivo
gerado_em: 2026-05-02T19:58:37-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 02/05/2026 às 19:58 BRT

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
- [decisao/projetos] O primeiro passo para resolver o problema identificado é mergear o PR #72 e aguardar o CI passar. _(via claude-code)_

## Meta-reflexões ativas

- [meta_reflexao/projetos] Avanços futuros no projeto incluem a reescrita do system_prompt.md e a revisão de ferramentas e métodos utilizados na integração do bot. _(via claude-code)_
- [meta_reflexao/projetos] Os 60 PRs são considerados ruído gigante no contexto para ganho zero quando se busca entender o estado atual do projeto. _(via claude-code)_
- [meta_reflexao/projetos] A regressão do test para o bug do `_render_prompt()` foi sugerida para prevenir que o erro de KeyError volte a ocorrer. _(via claude-code)_
- [meta_reflexao/projetos] A meta é estabilizar o caminho crítico com testes e reconciliar as documentações com o código devido ao drift. _(via claude-code)_

## Fragmentos das últimas 6h (20 de 50 no brain)

- [procedural/gus] As buscas realizadas no Hub Qdrant devem retornar respostas relevantes para questões sobre exames anteriores. _(via telegram-claude)_
- [fato/projetos] O workflow de sincronização entre o Google Drive e o GitHub ainda não está ativo. _(via telegram-claude)_
- [fato/projetos] Houve um merge de um pull request relacionado a testes de regressão do curador. _(via telegram-claude)_
- [fato/projetos] O PR #72 corrigiu um bug em produção que impedia o curador de funcionar. _(via claude-code)_
- [fato/projetos] Há uma demanda parada chamada `2026-05-01-captura-multiporta-curador.md`. _(via claude-code)_
- [fato/projetos] A arquitetura do sistema é baseada no processamento paralelo entre vários modelos de linguagem, utilizando fallback em caso de falhas. _(via claude-code)_
- [fato/projetos] Hub é a memória central conectada a vários serviços, como Telegram, Claude Code e Claude Chat. _(via claude-code)_
- [fato/projetos] O manual operacional do Gus, regras de comportamento e como cada porta usa o Hub estão no arquivo `dialogos/_bootstrap/gus-bootstrap.md`. _(via claude-code)_
- [fato/projetos] O curador está rodando em loop com 100% de erro há mais de 3 dias. _(via claude-code)_
- [decisao/-] O connector do Gus Hub precisa ser recadastrado no claude.ai devido ao ponto de falha na URL. _(via claude-code)_
- [fato/projetos] O PR #72 foi aberto no repositório Gus para abordar as questões identificadas na auditoria do Chat. _(via claude-code)_
- [fato/projetos] As frentes mais ativas nos últimos dias são relacionadas ao PR #60 (MCP URL secret) e PR #64 (cron captura transcripts Claude Code). _(via claude-code)_
- [fato/projetos] No projeto, as demandas pendentes se referem a quatro tarefas: captura multiporta curador, drive sync oauth fix, pendências da Claude Chat consolidadas, e um template. _(via claude-code)_
- [decisao/projetos] O primeiro passo para resolver o problema identificado é mergear o PR #72 e aguardar o CI passar. _(via claude-code)_
- [fato/projetos] Os canais de controle e armazenamento de dados (hub/store) são utilizados para gerenciar a memória do Gus. _(via claude-code)_
- [fato/projetos] A demanda `2026-05-01-captura-multiporta-curador.md` é parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat. _(via claude-code)_
- [fato/projetos] O `_estado-atual.md` (27/04) está desatualizado e não reflete muitas atualizações posteriores documentadas no git, como PRs #57, #60, #63, #64 e #67. _(via claude-code)_
- [fato/gus] O projeto Gus envolve um sistema multi-porta que conecta vários canais, como Telegram, Claude Code e Claude Chat, usando um Hub Qdrant como memória central. _(via claude-code)_
- [fato/projetos] O cache de mídia não tem limite de bytes, o que pode levar a problemas de memória no container do Railway. _(via claude-code)_
- [fato/projetos] O projeto NeuroGus está com planejamento 100% pronto e falta a implementação. _(via claude-code)_

## Resumo numérico

- **Total no brain `gustavo`**: 551 fragmentos
- **Amostra carregada**: 50 mais recentes (limite do listar)

### Distribuição por tipo (na amostra)

- `fato`: 36
- `decisao`: 5
- `episodico`: 4
- `lacuna`: 3
- `projeto`: 1
- `procedural`: 1

## Auto-observações do Gus (brain `gus` — 525 fragmentos)

- [fato/projetos] O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta). _(via claude-code)_
- [fato/projetos] A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat. _(via claude-code)_
- [fato/gus] As diretrizes de segurança para o MCP incluem a proteção com um URL secreto. _(via claude-code)_
- [fato/projetos] Os documentos principais que fornecem contexto para novas abas são: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md`, e `proj... _(via claude-code)_
- [fato/projetos] Existem 3 demandas paradas em `dialogos/inbox-claude-code/`. _(via claude-code)_
- [fato/projetos] PRs descrevem o caminho, não onde a equipe está atualmente em seu trabalho. _(via claude-code)_
- [procedural/projetos] Decisões arquiteturais devem ser documentadas nos docs, não nos PRs. _(via claude-code)_
- [fato/gus] Hoje, o MCP Hub está público sem `MCP_URL_SECRET`. _(via claude-code)_

---

_Última atualização automática. Próxima em ≤15min._
