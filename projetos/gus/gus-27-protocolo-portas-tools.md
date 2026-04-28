---
tipo: protocolo-arquitetural
area: gus
atualizado: 2026-04-28T09:55-03:00
status: vigente
proximos: aplicar retroativamente em portas/tools existentes
---

# gus-27 — Protocolo de análise de portas e ferramentas novas

Documento de **crivo arquitetural** pra novas portas (Custom GPT, Alexa,
SMS, carro, etc.) e novas ferramentas (`rotear_arquivo`, `criar_acao`,
ainda-a-criar). Hoje o checklist mental funciona porque cabe na cabeça;
mas conforme o sistema cresce, drift entre portas é certeza sem o crivo
escrito.

**Quando usar este doc:**

- Antes de implementar tool nova (preencha Seção 1 no PR description)
- Antes de habilitar porta nova (mesma Seção 1)
- Em revisão retroativa (toda tool/porta existente passa pelo crivo
  uma vez pra detectar gaps documentais)

**Não é burocracia** — é checklist de 5min que trava bug arquitetural
de 2 horas depois.

---

## Princípios não-negociáveis (validados em toda análise)

Estes pilares vêm de `CLAUDE.md`, `gus/system_prompt.md`, `gus-12-portas-futuras.md`.
Toda nova porta/tool tem que **respeitar** os 6:

1. **Identidade única**: Gus é uma entidade só, não 4. Porta é canal,
   não persona separada. (Exceção possível: Alexa pode ter persona
   ligeiramente adaptada à voz, mas valores e memória são compartilhados.)

2. **Memória compartilhada — Hub Qdrant é fonte única**: toda porta
   lê/escreve no `gus_hub`. Nenhuma porta tem brain próprio. `via` no
   payload identifica origem.

3. **GitHub é o vault de conhecimento**: arquivos `.md` estruturados.
   Toda porta lê do mesmo repo. Escrita passa por scan sensível
   (`gus.patterns_sensiveis`) exceto em `sensivel/`.

4. **LGPD em dimagem**: dados de paciente vão pra `dimagem/casos/`
   com pseudônimo. Ou pra `dimagem/dia/` (apenas nome+exame+convênio).
   **Nunca em outras pastas.** **Nunca no Drive sync.**

5. **Custo controlado**: orçamento atual ~US$30/mês Anthropic + ~$0
   Qdrant Cloud free + Tavily/OpenAI pontuais. Nova porta/tool não
   pode dobrar custo sem decisão explícita.

6. **Não-alucinação**: cada porta tem que ter mecanismo equivalente
   ao princípio 1 do system_prompt — verificar antes de afirmar
   ausência. Se a porta nova não permite isso (ex: Alexa sem ferramentas
   de busca real), tem que estar **explicitamente documentado**
   como limitação.

---

## Seção 1 — Checklist arquitetural (PRÉ-implementação)

Responda as 6 perguntas abaixo **antes de codar uma linha**. Se alguma
resposta for "não sei" ou "depende", **pause e discuta antes**. PR
description deve copiar essas respostas como bloco de aprovação.

### 1.1 Identidade e canal

- [ ] Esta é uma **porta nova** (canal de I/O com Gustavo) ou
      **ferramenta nova** (capacidade de uma porta existente)?
- [ ] Se porta: ela herda `gus-identity.md` integralmente, ou tem
      adaptação justificada? Qual?
- [ ] Se tool: em qual(is) porta(s) ela aparece? (Telegram TioGu,
      Claude Code, Claude Chat, Custom GPT, Alexa). Justifique se for
      em algumas e não outras.

### 1.2 Memória

- [ ] **Lê do Hub Qdrant**? Em qual brain (`gustavo`, `gus`, ambos)?
      Com qual filtro (tipo, area, camada_temporal)?
- [ ] **Escreve no Hub Qdrant**? Com qual `via` no payload?
      (`telegram-claude`, `claude-code`, `claude-chat`, `custom-gpt`,
      `alexa-skill`, `tiogu-roteador`, etc.) — escolher do enum
      canônico em `gus-13-tags-canonicas.md` ou propor adição
- [ ] Se a tool/porta cria fragmentos sem ir pelo curador (ou seja,
      escrita direta), eles têm `tipo` adequado? Não polui com
      conteúdo trivial?

### 1.3 Conhecimento (GitHub vault)

- [ ] **Lê GitHub**? Direto via API, ou via cópia espelhada (Drive),
      ou via API REST nossa?
- [ ] **Escreve GitHub**? Em quais pastas? Passa por
      `gus.patterns_sensiveis.escanear` antes? (Resposta correta:
      sim, exceto em `sensivel/`)
- [ ] Se cria arquivos novos, segue convenção de nome do CLAUDE.md
      (`<tipo>-<mes>-<ano>.md`, etc.)?
- [ ] Pode disparar workflow (sync-to-drive, archive-completed,
      notificar-inbox-tiogu)? Risco de loop infinito? Como mitiga?

### 1.4 Custo

- [ ] **Custo por chamada/evento**: estimativa em US$ (input tokens
      × preço modelo + output × preço + custo externo se houver)
- [ ] **Frequência esperada**: chamadas/dia. Cron? Trigger por evento?
      Manual?
- [ ] **Custo mensal estimado**: chamadas/dia × 30 × custo/chamada
- [ ] **Cabe no orçamento**? (Hoje ~US$30/mês Anthropic global). Se
      acrescentar mais que 20%, **discutir explicitamente** antes
- [ ] Tem rate-limit ou hard-limit no código pra não estourar?

### 1.5 LGPD e privacidade

- [ ] Pode tocar **dados de paciente Dimagem**? (Nome, CPF, exame,
      diagnóstico, etc.)
- [ ] Se sim, escreve em `dimagem/dia/` (mínimo: nome + exame +
      convênio) ou em `dimagem/casos/` (com pseudônimo)?
- [ ] Se sim, garantia de **não vazar pro Drive**? (`sensivel/` e
      `dimagem/casos/` são excluídos do sync; verificar `sync_to_drive.py`)
- [ ] Pode tocar **credenciais ou PII do Gustavo**? (Tokens, senhas,
      CPF dele, etc.) Se sim, scan ativo? Path em `sensivel/`?

### 1.6 Compatibilidade com fluxo entre portas

- [ ] Se a tool **modifica estado compartilhado** (Hub, GitHub, Drive),
      outras portas vão ver esse estado coerente?
- [ ] Se cria demanda em `dialogos/inbox-*/`, segue protocolo do
      `dialogos/README.md` (frontmatter completo, paths certos)?
- [ ] Se notifica Telegram, usa os mesmos secrets já configurados
      (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)? Não cria notificações
      duplicadas com workflows existentes?
- [ ] Se a porta nova é externa (Custom GPT, Alexa, carro) — como
      autentica? Token compartilhado? OAuth? Restrição por chat_id /
      device_id?

---

## Seção 2 — Checklist técnico (implementação + merge)

Lista mecânica do que tem que estar feito **antes do merge**. PR description
deve marcar cada item.

### 2.1 Código — tool nova

- [ ] Schema da tool em `gus/tools.py:TOOLS` (description clara dizendo
      QUANDO usar, não só O QUE faz)
- [ ] Handler em `executar_tool` delegando pra função de implementação
- [ ] Função de implementação em módulo dedicado (`gus/<dominio>.py`)
      se for não-trivial — não inflar `tools.py`
- [ ] Validações em camadas: input shape, path traversal, tipos, fonte
- [ ] Idempotência: chamadas repetidas com mesmo input não duplicam efeito
- [ ] Erro reporta mensagem amigável ao usuário (não stack trace cru)

### 2.2 Código — porta nova

- [ ] Entrypoint registrado (handler Telegram, route FastAPI, Lambda
      handler, etc.)
- [ ] Auth: token compartilhado, OAuth, ou allowlist por device/chat
- [ ] Rate limit: quantas mensagens/minuto/dia aceitas
- [ ] Logger registra chamadas (custo + latência) no padrão atual
      (JSONL em `gus/logger.py`)
- [ ] Error handling: porta não derruba bot principal se quebrar
- [ ] State persistente (se houver) em `/app/data` no Railway pra
      sobreviver redeploy

### 2.3 Documentação obrigatória

- [ ] **`gus/tools.py:TOOLS`** — schema com description
- [ ] **`gus/system_prompt.md`**:
  - [ ] Tool listada na enumeração "Suas capacidades"
  - [ ] Bloco "Quando usar `<tool>`" se não for trivial (>2 linhas
        de explicação justifica bloco)
- [ ] **`CLAUDE.md`**:
  - [ ] Lista geral de tools sincronizada (contagem + categoria)
  - [ ] Estrutura de código atualizada se houve módulo novo
- [ ] Onde a tool faz algo novo no protocolo (`dialogos/`, `_indices/`,
      `pessoal/`, etc.) → README dessa área atualizado
- [ ] Se afeta handoff entre sessões → `_estado-atual.md` atualizado
      ao final
- [ ] **Frontmatter / convenção nova** (ex: `acao_sugerida` que veio
      no Estágio 0): documentado no README da pasta relevante

### 2.4 Segurança

- [ ] **Scan sensível** ativo na escrita: usa `gus.patterns_sensiveis.
      escanear` ou passa por `_save_to_github` (que já scaneia)
- [ ] Path validation: bloqueia traversal (`..`), caracteres estranhos
      (regex SAFE_PATH)
- [ ] Restringe escopo: source/destino só onde faz sentido (ex:
      `rotear_arquivo` só aceita source em `dialogos/inbox-*/`)
- [ ] Hooks `PreToolUse:scan_sensivel` cobrem o caminho de escrita?
      Se for via API direta (não Write/Edit), o scan está duplicado
      no código?
- [ ] **Confirmação humana** pra ações irreversíveis (deletar,
      mover sem backup, ações em conta externa)

### 2.5 Testes

- [ ] Sintaxe Python OK (`python3 -c "import ast; ast.parse(...)"`)
- [ ] YAML válido em workflows novos
- [ ] **Smoke tests offline** em funções puras (parse, validações,
      formatação) — não exigir Qdrant/GitHub real
- [ ] Plano de teste em produção documentado no PR (passos
      reproduzíveis: como criar input de teste, o que esperar)
- [ ] Se a tool é chamada por `executar_tool` async, smoke test
      com `asyncio.run` se possível

### 2.6 PR e rollback

- [ ] PR description tem:
  - [ ] Resumo (1 parágrafo)
  - [ ] Lista de arquivos novos/modificados com 1 linha por mudança
  - [ ] Defesas listadas (idempotência, validações, scan)
  - [ ] Plano de teste pós-merge
  - [ ] Análise de risco
- [ ] Branch nomeada com prefixo `claude/<tema-curto>` ou
      `feat/<porta-tool>`
- [ ] Commits com mensagens descritivas (não "wip", não "fix")
- [ ] **Rollback documentado**: como reverter se der ruim em produção
      (revert PR, env var pra desligar feature, etc.)

---

## Seção 3 — Critério de calibração (PÓS-merge, antes de evoluir)

Quando considerar feature "estabilizada" e elegível pra evoluir
(ex: Estágio 1 → Estágio 2 do roteamento)?

### 3.1 Métricas mínimas pra "calibrado"

- **Volume**: pelo menos 5 usos reais por caminho/cenário
  (ex: 5 invocações de `criar_novo`, 5 de `append`, 5 de `mover`
  pra calibrar `rotear_arquivo`)
- **Custo real**: confirmado dentro da estimativa pré-merge (±20%).
  Acima disso, investigar antes de evoluir
- **Falha rate**: <5% das invocações falham por bug interno (não
  por input ruim, que é esperado)
- **Recusas explícitas do Gustavo**: registrar quando ele disse
  "não, faz diferente" — sinal de que defaults precisam ajuste

### 3.2 Janela mínima de observação

- Tool simples (utilitário): 1 semana de uso real
- Tool com efeito persistente (escreve repo, deleta memória): 2 semanas
- Porta nova: 4 semanas (volumes baixos no início, leva tempo pra
  ver edge cases)

### 3.3 Quem decide avançar

- **Gustavo decide** explicitamente baseado em:
  - "Funciona como esperado" (zero surpresas no período)
  - Custo dentro do orçamento
  - Não quebrou nada adjacente
- Auto-promoção (sem decisão dele) só pra mudanças cosméticas
  (ex: melhorar mensagem de erro), nunca pra mudança de comportamento

### 3.4 Sinais de que precisa rollback

Se algum dos 4 acontece, rollback imediato + post-mortem:

- Bug de produção que afeta outra feature (não é bug local)
- Custo 2x acima do estimado sem explicação clara
- Falha silenciosa (não loga erro, mas não faz o que deveria)
- Confusão do Gustavo sobre o que está acontecendo (UX ruim)

---

## Como integrar o protocolo

### Referência em outros docs

- **`CLAUDE.md`** ganha linha:
  > "Antes de adicionar tool/porta nova, ler `projetos/gus/gus-27-
  > protocolo-portas-tools.md` e preencher Seção 1 no PR description."

- **`dialogos/_bootstrap/gus-bootstrap.md`** (lido por Claude Chat)
  ganha linha similar pra que sugestões de feature dele já cheguem
  com Seção 1 preenchida.

### Template no PR

Sugestão de bloco no PR description (copy-paste):

```markdown
## Crivo gus-27

### Identidade
- **Tipo**: [porta nova | tool nova]
- **Onde aparece**: [Telegram | Claude Code | Chat | Custom GPT | Alexa]

### Memória
- **Lê Hub**: [sim/não — qual brain, qual filtro]
- **Escreve Hub**: [sim/não — qual via]

### Conhecimento
- **GitHub**: [só leitura | escrita em `<pasta>` | nenhuma]

### Custo
- **Por chamada**: ~$X
- **Frequência**: N/dia
- **Mensal estimado**: ~$Y
- **Cabe no orçamento**: [sim/não]

### LGPD
- **Dimagem**: [não toca | toca, escreve em `dimagem/dia` ou `casos`]
- **Sensível Gustavo**: [não toca | toca, escreve em `sensivel/`]

### Compatibilidade
- **Modifica estado compartilhado**: [sim/não]
- **Risco de loop**: [não | sim, mitigado por X]
```

### Aplicação retroativa (próxima sessão)

Tools/portas existentes passam pelo crivo uma vez. Não pra mudar
código, mas pra **detectar gaps documentais**:

- `search_memory`, `salvar_memoria_gus`, `buscar_memoria_gus`
- `save_to_github`, `read_from_github`, `list_github_directory`
- `auto_diagnostico`, `logs_railway`
- `pesquisar_pubmed`, `pesquisar_arxiv`, `search_web`
- `perguntar_gpt`
- `disparar_workflow`, `criar_acao`, `sugerir_wikilinks`
- `meta_memoria`, `auditoria_mem0`, `deletar_memoria`
- `rotear_arquivo` (recém-implementada, bom primeiro caso)

Cada uma deve ter um arquivo curto em
`projetos/gus/crivos/<tool>.md` (a criar) com Seção 1 preenchida.
Se algum gap aparecer (ex: tool sem hook scan ativo), abre PR de
correção.

---

## Histórico

| Data | Autor | Mudança |
|---|---|---|
| 2026-04-28 | Claude Code | Versão inicial — 3 seções, 6 princípios, template PR, plano retroativo |

Relacionado: [[gus-12-portas-futuras]], [[gus-13-tags-canonicas]],
[[gus-25-roadmap-ativacao]], [[CLAUDE]]
