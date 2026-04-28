---
tipo: detalhes-tecnicos-sessao
data: 2026-04-27
prs: [7, 8, 9, 10]
arquivos_modificados: ~40
linhas_alteradas: ~2200 (insertions+deletions)
---

# Sessão 27/04/2026 — Detalhes técnicos

Documentação cirúrgica das mudanças de código. Para visão geral ver
`01-resumo-executivo.md`.

## Bug 1 — OCR Dimagem com nome trocado em prontuário (#4 inbox)

**Sintoma:** Gustavo enviou foto de OS deitada (rotação 90°), Haiku Vision
extraiu nome **errado** sem aviso de incerteza, bot registrou paciente
trocado em `dimagem/dia/2026-04-27.md`.

**Risco:** Identidade trocada em contexto médico corrompe prontuário/cobrança.
Falso positivo é mais perigoso que falso negativo.

**Causa:** `PROMPT_EXTRACAO` em `gus/dimagem.py` não pedia auto-avaliação de
confiança. Haiku retornava JSON com nome (mesmo errado) sem flag de incerteza.

**Fix em 3 camadas:**

1. **`gus/dimagem.py:PROMPT_EXTRACAO`** — schema do JSON ganhou 2 campos:
   - `confianca`: "alta" | "media" | "baixa"
   - `motivo_incerteza`: string curta (null se alta)

   Critérios explícitos no prompt:
   - **alta**: imagem nítida, NOME lido com 100% de certeza letra por letra
   - **media**: borrão leve, ambiguidade resolvida por contexto
   - **baixa**: rotação >15°, NOME ambíguo, qualquer dúvida sobre quem é o paciente

2. **`gus/dimagem.py:analisar_os_dimagem` (linhas 541-563)** — gate antes
   de criar pending:
   - Confiança "baixa" → retorna `{"pedir_reenvio": True, "preview_text": ...}` sem criar state
   - Confiança "media" → preview com `⚠️ Confiança média na leitura` + motivo
   - Confiança "alta" / ausente / inválida → fluxo normal

3. **`gus/bot.py:handle_photo` (linhas 469-475)** — verifica
   `_preview.get("pedir_reenvio")` ANTES de criar `dimagem_pending[chat_id]`.
   Sem pending = sem caminho pro save subsequente.

**Limitações documentadas:**

- Auto-avaliação do Haiku (sem ground truth). Se classificar "alta" foto difícil, gate não bloqueia.
- Não detecta nome trocado entre 2 pacientes legítimos (Wilson vs Gilson, ambos parecem nomes). Defesa adicional: aviso ⚠️ em "media" empurra Gustavo a checar visualmente.

## Bug 2 — Tools do TioGu reportando Mem0 silêncio (3 funções não migradas)

**Sintoma:** Após `auto_diagnostico`, TioGu reportava:
- `Mem0 ⚠️ 20 mems, última há 25.6h (26/04 18:46 BRT) — possível silêncio`
- `Não tenho acesso direto ao Qdrant — ele é serviço separado`
- `Sem hub/Qdrant no repo principal`

**Causa:** Apenas a função principal `buscar_memorias` tinha sido migrada
pra Hub (Fase 3 / PR #7). Outras 3 funções continuavam apontando pro Mem0
antigo morto:

- `buscar_memorias_detalhada` (gus/memory.py:135) — usada por `search_memory` tool
- `buscar_memorias_gus` (gus/memory.py:185) — delega pra detalhada
- `_check_mem0` (gus/integrations/diagnostico.py:91) — chamado por `auto_diagnostico`

**Fix (commit `b541d85`):**

1. **`gus/memory.py:buscar_memorias_detalhada`** — Hub-first com fallback
   Mem0. Retorno agora inclui `[tipo/area]` no formato:
   ```
   Encontradas N memória(s) em `gustavo` (Hub) pra `query`:
   1. [uuid] [biografico/pessoal] Gustavo mora em ...
   ```

2. **`gus/memory.py:buscar_memorias_gus`** — sem mudança direta, delega
   pra `detalhada`. Pega Hub-first de graça.

3. **`gus/integrations/diagnostico.py:_check_mem0`** → reescrita usando
   `hub.store.listar(user_id="gustavo", limit=50)`. Reporta name="Hub Qdrant"
   no `auto_diagnostico` (antes era "Mem0", o que confundia: TioGu via 20
   mems da coleção MORTA e disparava warn de silêncio falso).

**Cleanup posterior (PR #10):** função renomeada de `_check_mem0` →
`_check_hub` pra zerar a confusão de quem ler o código.

## Bug 3 — Curador erro 400 'temperature and top_p' (Hub vazio o dia inteiro)

**Sintoma:** Após PR #8 mergeado, `auto_diagnostico` mostrou:
```
| Hub Qdrant | ⚠️ | 0 fragmentos no user_id=gustavo |
```

Mesmo com fix do `_check_hub`, Hub estava vazio. Olhando logs em
`_log/resumos-mem0/2026-04-27.md`, o curador estava errando 100% das
chamadas com:

```
Error code: 400 - {'type': 'invalid_request_error',
'message': '`temperature` and `top_p` cannot both be specified...'}
```

8+ tentativas durante o dia, todas com 400. Por isso fallback Mem0 também
não pegava (Mem0 morto = silêncio total).

**Causa:** O helper `_chamar_claude_com_retry` em `gus/llm.py` sempre
incluía `system` no kwargs do `client.messages.create`, mesmo quando
`system_prompt=""`. O curador chamava com `system_prompt=""` porque o
prompt template ia em `messages[0].content`. Em **modelo Sonnet 4.6 + sem
tools + system=""**, o SDK Anthropic 0.40 ativava algum default que fazia
`top_p` chegar junto com `temperature` → 400.

**Por que o bot principal não falhava:**
- Bot sempre passa `tools=TOOLS` → ativa `extra_headers` token-efficient
- Bot sempre passa `system_prompt` com conteúdo (system_prompt do TioGu)
- Curador era o único caminho com `system=""` E `tools=None` simultâneos

**Fix em 2 camadas (commit `8eff275`, cherry-pick do `84afb3e`):**

1. **`hub/curador.py:_extrair_via_modelo`** — prompt template agora vai
   como `system_prompt` (canônico). `messages` recebe trigger curto:
   ```python
   response = await _chamar_claude_com_retry(
       model=modelo,
       max_tokens=2048,
       system_prompt=prompt,  # ← antes era ""
       messages=[{"role": "user", "content": "Extraia agora os fragmentos..."}],
   )
   ```

2. **`gus/llm.py:_chamar_claude_com_retry`** — só inclui `system` no
   kwargs se truthy:
   ```python
   if system_prompt:
       kwargs["system"] = system_prompt
   ```
   Defesa contra outros callsites que possam passar `system=""` no futuro.

**Validação pós-deploy:**
```
| Hub Qdrant | ✅ | 2+ frags, mais recente há 0.0h (27/04 21:13 BRT) |
```

## Migrações de código (R2, R6, R7)

### R2 — 5 scripts cron migrados pra Hub

Scripts em `.github/scripts/` que liam direto do Mem0 SaaS via
`from mem0 import MemoryClient`:

- `auditoria_mem0.py`
- `briefing_matinal.py`
- `export_mem0.py`
- `retrospectiva_semanal.py`
- `reflexao_quinzenal.py`

**Estratégia:** criado `_hub_compat.py` (compat layer) que expõe
`get_all_memorias()` e `search_memorias()` retornando no formato esperado
pelos scripts (campos `memory`/`created_at`/`metadata` que era o formato
Mem0). Cada script muda só 3-5 linhas em vez de ser reescrito.

**Workflows YAML correspondentes** atualizados pra:
- Trocar `MEM0_API_KEY` por `QDRANT_URL`/`QDRANT_API_KEY`
- Usar `pip install -r .github/scripts/requirements.txt` (novo arquivo)

**Cleanup posterior (PR #10):** `check-saude.yml` também migrado (não
era um dos 5 originais mas usa o mesmo padrão).

### R6 — MCP Claude Code lendo Hub

`.claude/mcp/mem0_server.py` (nome legado mantido por retrocompat) reescrito
pra usar `hub.store.*` internamente:
- `buscar_memorias` / `buscar_memorias_gus` → `hub.store.lembrar`
- `salvar_memoria` / `salvar_memoria_gus` → `hub.store.ingestar(metadata={"via":"claude-code"})`
- `listar_memorias` / `listar_memorias_gus` → `hub.store.listar`
- `deletar_memoria` → `hub.store.deletar`

`hub/store.py` ganhou métodos novos pra suportar o MCP:
- `listar(user_id, limit)` — scroll Qdrant filtrado
- `deletar(memory_id)` — delete idempotente por UUID

### R7 — Patterns sensíveis em fonte única + 5 novos

Antes os patterns estavam duplicados em 2 lugares (`gus/tools.py:_PATTERNS_SENSIVEIS`
e `.claude/hooks/scan_sensivel.py:PATTERNS`) com risco de drift.

**Centralização:** criado `gus/patterns_sensiveis.py` com `PATTERNS_SENSIVEIS`
(13 patterns) + helper `escanear(content)`. Ambos os callsites importam
deste módulo único.

**Patterns novos (5):**
- Qdrant API key (JWT-like)
- Telegram bot token (`\d{8,10}:[A-Za-z0-9_-]{35}`)
- Google service account key (PEM)
- Google OAuth client secret (`GOCSPX-...`)
- Railway token (env line `RAILWAY_*_TOKEN=`)

**Hook:** `scan_sensivel.py` adiciona `sys.path.insert(0, repo_root)` pra
importar do pacote `gus.patterns_sensiveis`. Fallback defensivo: se import
falhar, hook degrada gracioso (não trava Claude Code).

## R5 — Documentação pós-migração (PR #10)

Atualizado pra refletir Hub Qdrant como fonte da verdade:

| Arquivo | Mudança |
|---|---|
| `CLAUDE.md` | Reescrita parcial — bloco "Estado da migração", arquitetura, estrutura de código, lista de tools, hooks, pastas |
| `gus/system_prompt.md` | ~20 menções a Mem0 limpas (search_memory, deletar_memoria, automações, recovery, etc.) |
| `gus/tools.py` | 7 descrições de tools atualizadas |
| `projetos/gus/gus-15-decisao-migracao.md` | Nota de evolução: superada pelo ADR-001 |
| `projetos/gus/gus-23-logica-qdrant-mem0.md` | Status `superado-pelo-ADR-001`, custos atualizados |
| `projetos/gus/_estado-atual.md` | Reescrita completa pra 27/04 (era 25/04) |

## Cleanup R2 leftovers (PR #10)

- `gus/integrations/diagnostico.py:_check_mem0` → `_check_hub` (rename + docstring CHECKS ATIVOS)
- `.github/workflows/check-saude.yml` — `MEM0_API_KEY` → `QDRANT_URL`/`QDRANT_API_KEY`
- `.github/scripts/check_saude.py` — docstring atualizado
- `gus/bot.py` — mensagem fallback de mídia "Áudio e vídeo em breve" → "Vídeo ainda não tem handler" (áudio JÁ funciona desde sempre)

## Verificações que NÃO precisaram migrar

Encontrados em grep mas já estavam corretos:

- `.github/scripts/ingest_mem0_from_chat.py` — já usa `hub.curador.curar_arquivo`
- `.github/scripts/enrich_mem0_export.py` — só usa `anthropic`, não Mem0
- `.github/scripts/migrate_mem0.py` — script de migração ATIVA, intencional manter
- `.github/scripts/migrar_gus_para_hub.py` — migração `gus → gus_hub`, intencional manter

## Estatísticas da sessão

- **4 PRs sequenciais** mergeados (#7, #8, #9, #10)
- **~40 arquivos modificados** ao longo do dia
- **~2200 linhas alteradas** (insertions + deletions)
- **Sintaxe Python validada** em todos os arquivos modificados
- **YAML validado** em todos os workflows alterados
- **Smoke tests** rodaram onde possível (alguns dependem de Qdrant Cloud real, só rodam pós-deploy)

## Limitações honestas

Algumas coisas que **não** foram totalmente endereçadas, propositalmente:

- **`gus/memory.py` ainda importa `from mem0 import Memory`** — usado pelo
  `_get_client()` que é fallback de leitura em `buscar_memorias`. Necessário
  enquanto a Fase 5 do ADR-001 não removeu fallbacks.
- **Workflows `fix-qdrant-dims.yml` e `migrate-mem0-to-qdrant.yml`** ainda
  passam `MEM0_API_KEY` — são parte da migração ativa, manter intencional.
- **System_prompt.md tem ~5 menções restantes a Mem0** — todas intencionais
  (bloco-âncora, fallback documentado, pattern sensível "Mem0 key" no scan,
  nomes de arquivo/workflow legados como `auditoria-mem0.yml`).

## Ver também

- `01-resumo-executivo.md` — visão geral
- `03-pendencias-e-proximos-passos.md` — o que ficou aberto

Relacionado: [[_estado-atual]], [[gus-15-decisao-migracao]], [[gus-23-logica-qdrant-mem0]]
