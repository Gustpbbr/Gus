---
tipo: estado-atual-vivo
gerado_em: 2026-05-02T22:23:53-0300
fonte: hub-qdrant (gus_hub, user_id=gustavo)
janela_recentes_horas: 6
atualizacao: cron 15min
---

# Estado atual do Gus — 02/05/2026 às 22:23 BRT

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

## Fragmentos das últimas 6h (2 de 50 no brain)

- [procedural/gus] As buscas realizadas no Hub Qdrant devem retornar respostas relevantes para questões sobre exames anteriores. _(via telegram-claude)_
- [fato/projetos] O workflow de sincronização entre o Google Drive e o GitHub ainda não está ativo. _(via telegram-claude)_

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
