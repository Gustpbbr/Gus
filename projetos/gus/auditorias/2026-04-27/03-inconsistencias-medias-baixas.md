---
tipo: auditoria-fiscal
parte: 03-de-06
ordem_leitura: 4
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Inconsistências médias e baixas (R9–R16)

Voltar: [[00-leia-primeiro]] · Anterior: [[02-inconsistencias-criticas-altas]] · Próximo: [[04-plano-saneamento]]

---

## 🟡 MÉDIO

### R9. Pasta com nome irregular

`dialogos/Demandas Gustavo /` (espaço final, capitalizada). Foge do padrão lowercase-sem-espaço. Não é um inbox válido pelo protocolo. Tem só `_teste_para_todas_portas.md` dentro.

**Provável causa:** criação acidental pelo Apps Script ou manualmente no Drive (Drive aceita espaço em nome de pasta, mas em paths URL/Git fica esquisito).

**Ação simples:** renomear pra `dialogos/_demandas-gustavo/` (com underscore inicial pra ficar fora do fluxo de inbox) ou mover o arquivo pra `dialogos/archive/` e deletar a pasta.

---

### R10. inbox-tiogu acumula respostas, não demandas

5 arquivos hoje, todos parecem ser **respostas** criadas por outras portas pra notificar o Gustavo via Telegram:

- `2026-04-26T01-00__site-arquitetura-pronto.md`
- `2026-04-26T12-45__resposta-secrets-google-drive.md`
- `2026-04-26T18-55__resposta-status-migracao-qdrant.md`
- `2026-04-27T00-30__fix-qdrant-search-bug-concluido.md`
- `2026-04-26T00-15__teste-canal.md`

Mas o protocolo `dialogos/README.md` diz que `archive-completed-demandas.yml` só age sobre arquivos com `tipo: demanda` E `status: concluido`. Se essas notas têm outro `tipo` (ex: `tipo: resposta`) ou nenhum frontmatter padrão, **nunca são archivadas** → pasta cresce indefinidamente.

**Verificação:** li o `2026-04-27T00-30__fix-qdrant-search-bug-concluido.md` — frontmatter usa `tipo: resposta`, não `tipo: demanda`. Confirmado o problema.

**Ações possíveis:**
- Estender `archive_completed.py` pra aceitar também `tipo: resposta` com `status: concluido`
- Ou criar pasta `dialogos/respostas/` separada e ajustar fluxo
- Ou archive manual periódico

---

### R11. Branch local fora de sync (na hora desta auditoria)

No início desta sessão:
- `main` local: 10 commits atrás de `origin/main`
- `claude/greeting-checkin-NAcVz` (branch atual): aparentava 115 commits à frente de `origin/main`

**Realidade descoberta após push:** só **1 commit** real na frente (o meu, `98e8125`). A discrepância dos 115 vinha de fetch antigo. Não é problema real — só ruído.

→ Vale lembrar que `git fetch` deve rodar antes de qualquer comparação confiável de branches.

---

### R12. Workflows one-shot ainda no repo

`migrate-mem0-to-qdrant.yml` e `fix-qdrant-dims.yml` foram rotinas de migração que rodaram uma vez (commits `2907704`, `48c92b9`, `9ff9c96`).

Continuam aparecendo na lista do `disparar_workflow` (8 oficiais documentados em `gus/system_prompt.md`, mas `.github/workflows/` tem 14). O bot pode listar workflows que não fazem mais sentido rodar — risco baixo de Gustavo pedir pra rodar de novo por engano.

**Ação simples:** mover pra `.github/workflows/_legado/` ou deletar (etapa D.4 do plano).

---

### R13. `session-start.sh` instala deps em runtime no Web

```bash
pip install -q --user "mem0ai==0.1.29" "mcp>=1.0.0"
```

Frágil:
- Se o pip falhar (rede instável, PyPI fora), MCPs não sobem nesta porta
- O hook retorna `continue: true` mesmo assim, sem alertar
- Falha silenciosa: Claude Code parte sem MCPs, sem mensagem clara

**Ações:**
- Logar status do pip pro stderr (pode aparecer no log da sessão)
- Considerar pre-instalar via Dockerfile do sandbox (não sei se Anthropic permite)
- Ou aceitar a fragilidade — é Claude Code Web, sandbox não-controlado

---

## 🔵 BAIXO / cosmético

### R14. Estrutura aspiracional vs realidade

Pastas com pouquíssimo conteúdo real:

| Pasta | Realidade | Esperado |
|---|---|---|
| `pessoal/saude/` | 0 arquivos | "histórico-saude.md mestre + exames" |
| `pessoal/financeiro/` | 1 arquivo (`overview.md`) | mestre + extratos |
| `pessoal/diario/` | 1 arquivo (`semana-2026-W17.md`) | reflexões pessoais |
| `dimagem/dia/` | 2 arquivos | OS dia a dia |
| `dimagem/casos/`, `dimagem/protocolos/`, `dimagem/admin/` | 0 arquivos cada | conteúdo clínico |
| `receitas/` | 2 receitas (1 doce + 1 salgada) | doces + salgadas com subpastas |
| `agenda/` | 8 stubs mensais provavelmente vazios | compromissos |
| `acoes/{pendentes,concluidas}/` | só `.gitkeep` | fila de ações (executor não existe) |
| `capturado/visual/` | 1 placeholder `_ultimo.md` | capturas câmera S8 (futuro) |

**Não é problema** — é normal pra sistema com 12 dias. Mas reflete que o sistema é **mais infraestrutura de captura do que captura efetiva**. Conforme o uso real começar, essas pastas vão ganhar peso.

**Ação:** nenhuma direta. Observar evolução nas próximas auditorias.

---

### R15. Arquivos na raiz que parecem fora de lugar

- `get_token.py` — script utilitário (provavelmente OAuth Google Drive setup)
- `gus-memoria-export.json` e `gus-memoria-export.md` — exports diários, poderiam ir pra `_log/exports/` ou `_indices/`
- `resumo-financeiro.md` na raiz, quando o doc canônico (gus-01, system_prompt) diz que vive em `pessoal/financeiro/resumo-financeiro.md`

**Ações possíveis:**
- Mover `get_token.py` pra `scripts/` (já tem essa pasta)
- Mover exports pra `_log/exports/` ou criar pasta dedicada
- Mover `resumo-financeiro.md` pra `pessoal/financeiro/`

---

### R16. Reflexão SELF-1 rodou só 1 vez

`projetos/gus/reflexoes/2026-W17-reflexao.md` gerada 24/04. O cron é `sábado 10h BRT em semanas pares`, então:
- W17 (24/04) = sábado da semana ímpar 17 (passou em 19/04 — sábado 19/04 era W16 sábado? confuso)
- Próxima execução depende da regra de "semana par/ímpar" implementada no script

→ Só vou conseguir confirmar quando ler `reflexao_quinzenal.py` com calma. Por ora: o sistema só viu sua própria reflexão **uma vez**, então o brain `gus` (auto-observação) ainda tem ~4 memórias e o componente "Gus que pensa sobre si" ainda é praticamente inativo.

**Não é defeito** — é estado natural de sistema novo. Mas vale acompanhar se a próxima reflexão (sábado 02/05?) realmente roda.

---

## Síntese desta seção

R9-R13 são fricções operacionais que valem fix em algum momento, mas não bloqueiam nada hoje. R14-R16 são observações sobre maturidade do sistema — sintomas de juventude, não doenças.

**Nenhum item desta seção entra na ordem de prioridade do [[04-plano-saneamento]].** Todos podem ser endereçados depois que os críticos+altos estiverem resolvidos.

---

Próxima leitura: [[04-plano-saneamento]] · Voltar: [[02-inconsistencias-criticas-altas]]
