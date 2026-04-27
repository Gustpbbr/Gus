---
tipo: auditoria-fiscal
parte: 05-de-06
ordem_leitura: 6
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Design — Auto-merge condicional pra fechar gap Claude Code → main

Voltar: [[00-leia-primeiro]] · Anterior: [[04-plano-saneamento]] · Próximo: [[06-perguntas-abertas]]

---

## Problema

Hoje cada porta tem destino de escrita diferente:

| Porta | Onde escreve | Como chega no `main` |
|---|---|---|
| **Telegram (TioGu)** | direto em `main` via GitHub API (`save_to_github`) | já chega |
| **Custom GPT API** | direto em `main` (mesmo `_save_to_github`) | já chega |
| **Claude Chat** | no Drive `Gus-Sync/dialogos/` | `import-from-drive.yml` cron 15min commita em `main` |
| **Workflows automáticos** | direto em `main` | já estão lá |
| **Claude Code Web (esta porta)** | branch `claude/<nome>-<hash>` | ❌ **só por merge manual** |

→ **O problema é específico desta porta.** As outras 4 escrevem em main. Só Claude Code Web é forçado a operar em branch isolada (jeito do sandbox da Anthropic — não dá pra mudar daqui).

→ Resultado prático: quando Claude Code salva resultado em `dialogos/inbox-tiogu/`, registra em `_log/`, ou atualiza `_indices/`, fica trancado na branch até alguém mergear. As outras portas não veem.

→ Hoje **não existe nenhum workflow de auto-merge** no repo (verificado).

---

## Solução proposta — workflow `auto-merge-claude-branches.yml`

**Trigger:** push em qualquer branch `claude/**`

**Lógica em pseudo-código:**

```
1. Compara diff da branch contra main
2. Lista todos os paths modificados (git diff --name-only main...HEAD)
3. Pra cada path, classifica em ALLOW ou DENY (via globs)
4. Se TODOS estão em ALLOW e nenhum está em DENY:
     → tenta fast-forward merge pra main
     → se sucesso: push origin main, comentário no log
     → se conflito: posta erro, deixa pra resolver manualmente
5. Se algum path está em DENY:
     → não mergeia, posta comentário "exige PR pra revisão"
6. Se commit message começa com "wip:" ou "draft:":
     → skip auto-merge (trabalho parcial sinalizado)
```

---

## Allowlist proposta (auto-merge OK — são dados, não código)

Granularidade total — pode ser por pasta, subpasta ou arquivo:

```yaml
allow:
  # Comunicação entre portas
  - "dialogos/inbox-tiogu/**"
  - "dialogos/inbox-claude-code/**"
  - "dialogos/inbox-claude-chat/**"
  - "dialogos/inbox-custom-gpt/**"
  - "dialogos/archive/**"
  - "dialogos/historico/**"
  - "dialogos/processados-erro/**"
  - "dialogos/streams/**"

  # Logs auditáveis
  - "_log/**"

  # Dashboards regenerados
  - "_indices/saude.md"
  - "_indices/financeiro.md"
  - "_indices/projetos.md"
  - "_indices/dimagem.md"
  - "_indices/receitas.md"
  - "_indices/capturado.md"
  - "_indices/00-master.md"

  # Conteúdo do usuário
  - "pessoal/saude/**"
  - "pessoal/financeiro/**"
  - "pessoal/diario/**"
  - "dimagem/dia/**"      # só essa subpasta de dimagem
  - "capturado/**"
  - "receitas/**"
  - "agenda/**"
  - "acoes/**"

  # Reflexões automáticas
  - "projetos/gus/reflexoes/**"

  # Exports diários
  - "gus-memoria-export.md"
  - "gus-memoria-export.json"
```

---

## Lista bloqueada (precisa PR + revisão tua)

```yaml
deny:
  # Código + automação
  - "gus/**"
  - "api/**"
  - ".claude/**"
  - ".github/**"
  - "scripts/**"

  # Config e infra
  - "CLAUDE.md"
  - "requirements.txt"
  - "Dockerfile"
  - "railway.toml"
  - ".mcp.json"
  - ".env.example"
  - ".gitignore"

  # Doc canônica do projeto Gus (decisão arquitetural)
  - "projetos/gus/gus-*.md"
  - "projetos/gus/_estado-atual.md"
  - "projetos/gus/futuro/**"
  - "projetos/gus/auditorias/**"  # esta pasta também — auditoria nova é decisão tua mergear

  # Identidade — sensível
  - "gus/system_prompt.md"
  - "gus/meta-memoria.md"
  - "dialogos/_bootstrap/**"

  # Auditoria automática (gerada por workflow, não editar manualmente)
  - "_indices/_auditoria-mem0.md"

  # PII zone (já tem deny separada, redundância vale)
  - "sensivel/**"

  # Subpastas Dimagem que não são "dia"
  - "dimagem/casos/**"
  - "dimagem/protocolos/**"
  - "dimagem/admin/**"
  - "dimagem/convenios.json"

  # Obsidian config
  - ".obsidian/**"
```

⚠ **Importante:** `deny` tem precedência sobre `allow`. Se um commit toca em `dialogos/foo.md` (allow) E em `gus/bar.py` (deny), o auto-merge **não roda**.

---

## Riscos a mitigar

### Risco 1 — Conflito de merge

Duas branches `claude/*` mexem no mesmo arquivo (ex: dois Claude Codes paralelos atualizam `_log/auto-merge/AAAA-MM.md`).

**Solução:** workflow tenta fast-forward only. Se falhar, posta erro no commit/PR e deixa resolução manual.

### Risco 2 — Trabalho parcial vazando

Claude Code commita incompleto e auto-merge pega → main fica com WIP.

**Solução:** marcador no commit message:
- `wip:` ou `draft:` no início → workflow ignora
- Sem marcador → auto-merge se passar nas listas

### Risco 3 — Branch experimental indo pra main

Eu mexo em `dialogos/` pra testar e não quero mergear.

**Solução:** mesmo marcador `wip:` ou `draft:`. Convenção clara, fácil de seguir.

### Risco 4 — Race com workflows automáticos

Auditoria-mem0 commita em main às 06:30. Se uma branch claude tem mudança em `_indices/_auditoria-mem0.md`, conflita.

**Solução:** allowlist exclui `_indices/_auditoria-mem0.md` especificamente (esse arquivo é gerado, não editado por mim — listado em deny).

### Risco 5 — Múltiplas portas escrevendo na mesma pasta

Se Telegram commita em `dialogos/inbox-claude-chat/` ao mesmo tempo que Claude Code, race possível mas baixo (Telegram usa GitHub API que é serial; Claude Code via push depois do auto-merge).

**Solução:** workflow faz `git pull` antes do merge pra reduzir janela.

### Risco 6 — Workflow autorizando mais do que deveria

Bug na regex de allowlist pode liberar coisa que não deve.

**Solução:** começar com allowlist **bem curta** (só `dialogos/inbox-*/`, `_log/`, `dialogos/archive/`, `dialogos/historico/`) e expandir conforme observa. Logar cada execução em `_log/auto-merge/AAAA-MM.md`.

---

## Variações

### Variação A — Cherry-pick por path (mais conservadora)

Em vez de mergear branch inteira:

- Branch tem mudanças em `dialogos/foo.md` + `gus/bar.py`
- Workflow commita em main APENAS o `dialogos/foo.md`
- `gus/bar.py` continua só na branch, esperando PR

**Prós:** cirúrgico, não vaza WIP de código junto.
**Contras:** mais código de workflow, novos modos de falha (commits órfãos? referências cruzadas?).

### Variação B — Auto-merge integral com marcador `auto-merge-ok:`

Inverter a lógica: o auto-merge é **opt-in**, não opt-out. Só mergeia se commit message começa com tag específica.

**Prós:** zero risco de auto-merge não desejado.
**Contras:** preciso lembrar de marcar — se esquecer, info fica perdida igual hoje.

### Variação C — Não fazer nada — Claude Code escreve no Drive como Claude Chat

Reusa pipeline existente (`import-from-drive.yml`).

**Prós:** zero código novo, paridade com Claude Chat.
**Contras:** preciso de Drive auth aqui (não tenho hoje), latência de 15min do cron, perde commits diretos com história.

---

## Tradeoffs

| Opção | Prós | Contras |
|---|---|---|
| **Status quo (manual)** | Total controle, zero risco automático | Info perdida quando esqueço de pedir merge |
| **Auto-merge integral c/ allowlist + `wip:`** | Simples, comunicação flui, opt-out claro | Requer disciplina pra marcar wip; conflitos manuais quando paralelo |
| **Variação A (cherry-pick)** | Cirúrgico, não vaza WIP de código | Mais código de workflow, modos de falha novos |
| **Variação B (opt-in `auto-merge-ok:`)** | Zero risco de auto-merge não desejado | Esquecer = info perdida igual hoje |
| **Variação C (Drive)** | Reusa pipeline | Auth ausente, latência, perde commits diretos |

---

## Recomendação

**Auto-merge integral com allowlist conservadora + marcador `wip:`** na primeira versão.

Implementar:
1. **Allowlist curta inicial:** `dialogos/inbox-*/`, `dialogos/archive/`, `dialogos/historico/`, `dialogos/processados-erro/`, `_log/**`. Só isso.
2. **Skip se commit message tem `wip:`, `draft:`, `wip(`, `draft(` no início**
3. **Fast-forward only.** Falhou → erro, decide manual.
4. **Log de cada execução** em `_log/auto-merge/AAAA-MM.md` (auditável, mês a mês).
5. **Após 7 dias estável:** expandir allowlist com `_indices/<area>.md` (não o `_auditoria-mem0.md`), `pessoal/**`, `dimagem/dia/**`, `acoes/**`, `agenda/**`, `capturado/**`, `receitas/**`, `gus-memoria-export.{md,json}`, `projetos/gus/reflexoes/**`.
6. **Em paralelo:** mantém PR pra qualquer mudança em código.

---

## Próximos passos (quando você decidir implementar)

1. **Decidir granularidade inicial** (allowlist curta vs ampla)
2. **Decidir variação** (integral vs cherry-pick vs opt-in)
3. **Eu projeto o YAML do workflow + script Python** se quiser
4. **Você cria o secret se algum for necessário** (provavelmente nenhum — `GITHUB_TOKEN` automático basta)
5. **Ativar e observar 7 dias** com volume real

---

Próxima leitura: [[06-perguntas-abertas]] · Voltar: [[04-plano-saneamento]]
