---
tipo: pendencias-sessao
data: 2026-04-27
proxima_sessao: a definir
---

# Sessão 27/04/2026 — Pendências e próximos passos

O que **não** foi feito hoje, e por quê. Estruturado por prioridade.

## 🔴 Prioridade 1 — Decisão modelo curador (Fase 5 ADR-001)

**Quando:** após 12/05/2026 (14 dias de coleta dual a partir de 27/04)

**O que decidir:** qual curador fica em produção — Haiku 4.5, Sonnet 4.6,
ou ambos pra papéis diferentes?

**Como:** comparar par-a-par os fragmentos extraídos por cada modelo.

- Logs em `_log/resumos-mem0/AAAA-MM-DD.md`
- 1 entrada por curador, mesmo `hash_janela` permite parear no Obsidian
- Métricas a comparar: precisão (não captura lixo), recall (não perde fato),
  classificação correta (tipo / camada / area), custo por janela

**Implica também (Fase 5):**
- Aposentar Mem0 SaaS completamente
- Remover fallbacks Mem0 em `gus/memory.py:buscar_memorias` e `deletar_memoria`
- Remover `mem0ai==0.1.29` do `requirements.txt` principal e dos workflows
- Remover secret `MEM0_API_KEY` do GitHub e Railway
- Remover `from mem0 import Memory` de `gus/memory.py`
- Verificar se algum lugar ainda lê da coleção `gus` (Mem0 self-hosted)

## 🟡 Prioridade 2 — Custom GPT Action (DESKTOP obrigatório)

**Status:** Código `api/` em produção, GPT criado no mobile, **falta a Action**

**Por quê desktop:** GPT Builder mobile não mostra a aba Actions. Sem Action
configurada, o GPT alucina tool calls (testado em 25/04 — inventou `merge_branch`,
JSON simulado).

**Passos:**
1. Builder DESKTOP → editar GPT
2. Importar OpenAPI URL: `https://gus-production-58a7.up.railway.app/openapi.json`
3. Auth: API Key + Bearer + colar `CUSTOM_GPT_TOKEN`
4. Testar uma operation (ex: `read_from_github` com `path: "README.md"`)
5. Colar Instructions V2 anti-alucinação (texto pronto em `gus-14-custom-gpt-setup.md`)

**Doc completo:** `projetos/gus/gus-14-custom-gpt-setup.md`

## 🟡 Prioridade 3 — Suporte a vídeo no Telegram

**Status:** `filters.VIDEO` sem handler em `gus/main.py`. Mensagem do bot
pra formato não-suportado já está honesta ("Vídeo ainda não tem handler"
em vez de "Áudio e vídeo em breve").

**Implementação prevista:**
1. Handler `handle_video` em `gus/bot.py`
2. `processar_video` em `gus/media.py`:
   - Extrai áudio via `ffmpeg` (já no Dockerfile? confirmar)
   - Transcreve áudio via Whisper (reusa `transcrever_audio`)
   - Opcional: extrai N frames via Vision Sonnet pra contexto visual

**Custo estimado:** ~$0.05/vídeo (Whisper áudio + Vision frames)

**Nota:** Gustavo pediu pra pular nesta sessão.

## 🟢 Prioridade 4 — Itens menores

### Service Account Google Drive

Pendente desde sempre. Sem isso, sync GitHub → Drive não funciona em
arquivos novos. Provável caminho:
1. Console Google Cloud → criar service account
2. Compartilhar pasta Drive com service account email
3. Adicionar JSON da chave como secret `GDRIVE_SA_KEY` no GitHub

### Workflow YAML do `enrich_mem0_export.py`

Script existe mas não tem cron. Provavelmente deveria rodar logo após
`export_mem0.py` (3h BRT) — encadear no mesmo workflow ou criar novo
com `needs:` dependency.

### Limpar 4+ memórias poluídas no brain `gustavo`

Identificadas em 25/04 mas pendentes de deleção via MCP local.
Após a migração de hoje, as memórias estão na coleção `gus_hub` (se já
migradas) ou `gus` (se não). Caminho:
1. `mcp__mem0-gus__buscar_memorias("memória poluída")` — identifica IDs
2. Pra cada uma: `mcp__mem0-gus__deletar_memoria(memory_id=...)`

### Termux + wake word "Gus" no S8

Aprovada a Opção B. Pós-Alexa V1.

### Alexa Skill V1

Dot 3, Polly, voz pura (sem câmera, sem ações). Depois do Custom GPT
funcionando.

## ❓ Operacional — depende do Gustavo no painel

Ações que dependem de cliques em painéis externos. Algumas já feitas hoje
(✅), outras pendentes:

| Ação | Onde | Status |
|---|---|---|
| Configurar `Railway_diagnostic` | Railway → Variables | ✅ Feito hoje |
| Conferir secrets `QDRANT_URL`/`QDRANT_API_KEY` | GitHub → Settings → Secrets | ✅ Feito hoje |
| Disparar workflow `Migrar gus → gus_hub` | GitHub Actions → workflow_dispatch | ✅ Feito hoje |
| Mergear PR #10 | GitHub | ✅ Feito hoje |
| Configurar Custom GPT Action | OpenAI Builder DESKTOP | ❌ Pendente |
| Service Account Google Drive | Google Cloud Console | ❌ Pendente |

## 🐛 Bugs em aberto (não bloqueantes)

- DDG fallback ativa quando Tavily esgota cota (intermitente, conhecido)
- 4+ memórias poluídas no brain `gustavo` aguardando limpeza manual via MCP
- Hub: latência de embedding na primeira call do processo (~1-2s, sentence-transformers carrega modelo). Após primeira call, normaliza.

## ✅ Resolvidos hoje (registrados pra histórico)

- ~~OCR Dimagem com nome trocado em prontuário~~ — gate de confiança implementado (PR #8)
- ~~TioGu reportando "Mem0 silêncio 25h" no auto_diagnostico~~ — `_check_hub` lê do Hub (PR #8 + rename PR #10)
- ~~Curador erro 400 'temperature and top_p'~~ — sistema_prompt em vez de messages[0] (PR #9)
- ~~Hub Qdrant vazio mesmo após migração~~ — consequência do bug do curador, resolvido junto
- ~~5 demandas no inbox-claude-code~~ — todas processadas, inbox vazio
- ~~CLAUDE.md, system_prompt, gus-15/23 desatualizados~~ — R5 endereçado (PR #10)
- ~~`Railway_diagnostic` não configurado~~ — Gustavo configurou hoje
- ~~Coleção `gus` antiga sem migração~~ — workflow `Migrar gus → gus_hub` rodou

## Recomendação pra próxima sessão

1. **Começar lendo** `projetos/gus/_estado-atual.md` (foi reescrito hoje, está atualizado)
2. **Conferir** se decisão modelo curador chegou no fim do ciclo de coleta dual (depende da data — após 12/05)
3. **Se Custom GPT Action ainda não foi feita**, é provavelmente o item de maior alavanca pra avançar (destrava porta mobile via Custom GPT)
4. **Se vídeo for desejado**, é PR pequeno (~1h de trabalho)

## Ver também

- `01-resumo-executivo.md` — visão geral
- `02-detalhes-tecnicos.md` — bugs e fixes em profundidade
- `projetos/gus/_estado-atual.md` — handoff entre sessões
- `projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md` — decisão raiz da migração

Relacionado: [[_estado-atual]], [[gus-14-custom-gpt-setup]], [[gus-15-decisao-migracao]]
