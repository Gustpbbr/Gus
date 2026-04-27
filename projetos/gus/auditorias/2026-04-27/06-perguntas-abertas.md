---
tipo: auditoria-fiscal
parte: 06-de-06
ordem_leitura: 7
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Perguntas abertas pra Gustavo decidir

Voltar: [[00-leia-primeiro]] · Anterior: [[05-design-auto-merge]]

> Decisões que dependem de você antes que eu execute. Cada item aqui aponta pra qual arquivo da auditoria ele afeta. Quando você responder, ataco.

---

## P1. Mergear o `98e8125` agora?

A demanda `fix-qdrant-search-bug` foi marcada como concluído na branch `claude/greeting-checkin-NAcVz` (etapa A do [[04-plano-saneamento]]). Pra `archive-completed-demandas.yml` mover o arquivo, o commit precisa estar em `main`.

**Opções:**
- **P1.a** Mergear agora — abre PR e mergeia, archive workflow move em ≤15min
- **P1.b** Acumular B/C/D na mesma branch e mergear tudo de uma vez no fim
- **P1.c** Cherry-pick só esse commit pra main (menos provável)

**Minha leitura:** P1.b é mais limpo se você confia no plano todo. P1.a é mais didático se quer ver o archive funcionando hoje.

---

## P2. Auto-merge — implementar? Como?

Discussão completa em [[05-design-auto-merge]].

**Opções:**
- **P2.a** Não implementar — fica no manual
- **P2.b** Implementar versão integral com allowlist conservadora + marcador `wip:` (recomendação minha)
- **P2.c** Implementar variação cherry-pick (mais cirúrgico, mais código)
- **P2.d** Implementar opt-in com `auto-merge-ok:` (zero risco mas exige disciplina)

Se for P2.b/c/d: que pastas entram na allowlist inicial?

---

## P3. Ordem de saneamento: começo por onde?

Plano detalhado em [[04-plano-saneamento]].

**Recomendação minha:**
1. **B (curadoria híbrida)** primeiro — bug ativo perdendo dados agora
2. **D (migração Qdrant)** segundo — destrava MCP daqui, alinha auditoria
3. **E + F (LGPD)** terceiro — depende de D ideal pra rodar nas duas fontes
4. **G (patterns sensíveis)** em paralelo — fácil
5. **H (Drive→GitHub)** quando você decidir
6. **I (docs)** último — só após +48h estável

**Você concorda? Quer trocar a ordem?**

---

## P4. H — Drive→GitHub: qual caminho?

Verificação que depende de você (não vejo Apps Script):

> O Apps Script `drive_inbox_to_github.gs` está deployado e ativo no Google?

Se sim:
- **H1.** Desativar Apps Script (você desliga no script.google.com)
- **H2.** Manter ambos com escopos disjuntos (Apps Script pra `Gus-Sync/Inbox/` capturado/misc, Action pra `Gus-Sync/dialogos/`)
- **H3.** Migrar Apps Script pra Action (unificar em GitHub Actions, refator de `import_from_drive.py`)

Se não está deployado: deletar o `.gs` do repo (limpeza cosmética).

---

## P5. Custom GPT — quando configurar Builder?

Bloqueio único hoje:
- API FastAPI ✅ em produção
- GPT criado no Builder ✅ (mobile)
- ⏳ Configurar Action (precisa **desktop**, mobile não tem essa seção)
- ⏳ Colar Instructions V2 (texto pronto em `gus-14-custom-gpt-setup.md`)

Estimativa: ~30min seu, zero código meu. Mas exige você no PC.

**Quer agendar pra próximo turno PC ou ainda não?**

---

## P6. Hub pre-AGI — ativar etapas 2-5 ou estabilizar primeiro?

Toda a série gus-15..gus-26 descreve etapas:
1. ✅ Mem0 self-hosted (executada 26/04, com bugs ativos R1-R6)
2. ⏳ Hub Qdrant (estendido — não vi se tem código novo)
3. ⏳ Curador Haiku integrado — exatamente o que tá quebrado em R1
4. ⏳ Ego Cache dinâmico
5. ⏳ Auto-relato narrativo

A demanda `2026-04-27T06-16__schema-hub-qdrant-salvar-memoria.md` (pendente) refere ao schema do Hub gus-18 — implícito que ainda não foi implementado no código.

**Recomendação minha (provisional, sem ter lido gus-15..25 a fundo):** estabilizar Etapa 1 (corrigir R1-R8) antes de implementar 2-5. Etapas 2-5 dependem de fundação estável — implementar em cima de fundação quebrada multiplica problemas.

**Você concorda?** Ou prefere implementar Etapas 2-5 em paralelo com saneamento porque elas próprias resolvem alguns dos R?

---

## P7. Quer que eu leia gus-15..25 com calma?

Pra dar opinião informada sobre arquitetura "Hub pre-AGI", SELF-1, Ego Cache, Auto-relato — preciso ler esses 11 docs com atenção (não só headers como nesta auditoria).

Estimativa: 30-60min de leitura aprofundada nesta porta + atualização desta auditoria com seção nova "Análise da arquitetura Hub pre-AGI" se relevante.

**Quando? Antes de B ou depois?**

---

## P8. Outras portas — prioridades

`gus-12-portas-futuras.md` lista: Custom GPT (em config), Alexa, S8 wake-word, carro.

**Pergunta de visão (não tem resposta certa):** vale abrir Custom GPT mobile + Alexa antes de o sistema acumular 30 dias de uso real, ou esperar?

Meu palpite (provisional): cada porta nova é mais 1 lugar pra divergir. Se você ainda tá calibrando o Telegram (usado há ~12 dias), abrir 2 portas ao mesmo tempo dificulta isolar problemas. Mas é tua chamada.

---

## P9. Estrutura final do projeto

Você mencionou: *"ainda temos que formalizar uma estrutura final do projeto, mas para isso vc tem q ler todos os outros mds"*.

Pra propor estrutura final, preciso ler:
- gus-02..25 (24 docs canônicos)
- `gus-08-plano-proximos-passos.md` (plano A-H)
- `gus-09-guia-uso-diario.md`
- `projetos/gus/reflexoes/2026-W17-reflexao.md`
- `projetos/gus/futuro/*` (2 docs)
- Implementação completa de `gus/tools.py`, `gus/integrations/*`, `gus/dimagem.py`, `gus/media.py`
- `api/dashboard.py`, `api/camera.py`

Estimativa: 2-3h de leitura nesta porta.

**Quando você quer? Antes ou depois do saneamento?**

---

## P10. Periodicidade desta auditoria

Esta auditoria é a **primeira** desta natureza no repo. Se útil, faz sentido recorrer:

**Opções:**
- **P10.a** Auditoria pontual sob demanda (você pede quando achar útil)
- **P10.b** Auditoria mensal automática (workflow `auditoria-fiscal-mensal.yml`?)
- **P10.c** Auditoria trimestral (tipo "reflexão arquitetural" do SELF-1)
- **P10.d** Não recorrer — esta foi suficiente

---

## Ordem sugerida pra você responder

Se quiser otimizar: **P3 → P1 → P2 → P7 → P9 → P6 → P4 → P5 → P8 → P10**.

P3 destrava o resto (ordem do saneamento). P1+P2 são decisões de processo. P7+P9 são leituras minhas. P6 é decisão estratégica grande. P4+P5+P8+P10 podem esperar.

Mas você é quem dirige.

---

Voltar: [[00-leia-primeiro]]
