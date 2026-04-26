---
tipo: contrato-canonico
area: gus
atualizado: 2026-04-25T16:05-03:00
status: ativo — qualquer salvamento novo no Mem0 deve respeitar
---

# Tags canônicas do Mem0 — quem é quem, o que é arquitetura

Documento de **contrato**: define os user_ids e tags `via` aceitos no
sistema. Qualquer porta nova ou script que salve memória **deve usar uma
tag desta tabela** — nada de inventar variações.

Por que isso importa: sem padrão, "telegram-claude" / "tg-claude" /
"bot-tg" se misturariam e qualquer filtro semântico vira inútil.

---

## 1. Os DOIS brains (user_id)

| user_id | O que guarda | Quem escreve |
|---|---|---|
| **`gustavo`** | Fatos sobre o Gustavo: saúde, projetos, preferências, decisões pessoais, contexto de vida, memória semântica resumida pelas portas | Qualquer porta — automaticamente via resumo de turnos OU explicitamente via `salvar_memoria` |
| **`gus`** | Auto-observações do agente sobre si mesmo: padrões operacionais sobre o Gustavo, aprendizados táticos, princípios emergidos, caveats de tools | Qualquer porta — explicitamente via `salvar_memoria_gus` (não tem fluxo automático) |

**Regra de roteamento:**
- Pergunta sobre o Gustavo → `salvar_memoria` → brain `gustavo`
- Auto-reflexão do agente → `salvar_memoria_gus` → brain `gus`
- Confusão? Padrão é `gustavo`. Brain `gus` é exceção, usar com moderação.

---

## 2. Tags `via` canônicas

Toda memória nova carrega `metadata.via = <tag>`. Search default não filtra
(visibilidade cruzada total). Filtro só pra debug ou comparação intencional.

### 2.1 Portas humanas (interação direta com Gustavo)

| Tag canônica | Origem | Cérebro | Status |
|---|---|---|---|
| `telegram-claude` | Bot @Tiogubot — interação principal de hoje | Sonnet 4.6 | **ativa** (default no `gus/memory.py`) |
| `telegram-gpt` | Bot @GptGusBot — futuro, segundo bot Telegram | GPT-5 | reservada |
| `claude-code` | Sessões Claude Code (web ou local), via MCP | Opus/Sonnet | **ativa** (default no `mem0_server.py`) |
| `claude-chat` | Claude.ai web (chat manual com Gustavo) | Sonnet/Opus | **ativa** via canal `dialogos/inbox-mem0-from-chat/` (workflow `ingest-mem0-from-chat.yml` salva, ver §2.2) |
| `custom-gpt` | Custom GPT no ChatGPT mobile (voz) | GPT | reservada (Sprint F do roadmap) |
| `alexa` | Skill Alexa em casa | Sonnet (provável) | reservada (Sprint G) |
| `carro-audio` | Plugin de áudio no carro | TBD | reservada |

### 2.2 Automações (escrevem programaticamente, sem interação humana direta)

| Tag canônica | Origem | Frequência | Status |
|---|---|---|---|
| `workflow-briefing` | `briefing-matinal.py` | diário 7h BRT | **planejada** (script ainda não salva no Mem0 hoje) |
| `workflow-retrospectiva` | `retrospectiva-semanal.py` | sexta 20h BRT | planejada |
| `workflow-reflexao` | `reflexao-quinzenal.py` | sábado 10h BRT (semanas pares) | planejada |
| `workflow-self1` | reflexão SELF-1 (Nosis/Thymos/Síntese) | quinzenal | planejada |
| `workflow-export-mem0` | NUNCA salva, só exporta | — | não usa |
| `workflow-auditoria-mem0` | NUNCA salva, só lê + gera MD | — | não usa |
| `ingest-mem0-from-chat.yml` | salva memórias do Claude Chat (tag `via=claude-chat`) | a cada 30min | **ativa** desde 26/04/2026 |

**Importante:** o `ingest-mem0-from-chat.yml` é o **primeiro workflow que salva
no Mem0**. Ele não cria uma tag própria — usa `via=claude-chat` porque o
conteúdo veio do Chat (ele só executa o save). Se outros workflows começarem
a salvar conteúdo gerado por eles mesmos (ex: briefing matinal salvando "fato
do dia"), aí sim criar tag canônica `workflow-X` + atualizar este doc.

### 2.3 Importações externas (futuro)

| Tag canônica | Origem |
|---|---|
| `import-obsidian` | Importação manual de notas pré-Gus |
| `import-notion` | Se um dia importar do Notion |
| `import-mempalace` | Sistema antigo, se tiver memórias salvas |

---

## 3. O que NÃO é memória Mem0

Pra evitar confusão entre conceitos:

| Coisa | Onde mora | Função | NÃO confundir com |
|---|---|---|---|
| `gus/meta-memoria.md` | arquivo .md no repo | Biografia narrativa do Gus (auto-conhecimento longo) | Brain `gus` no Mem0 (memórias atômicas) |
| `gus/system_prompt.md` | arquivo .md no repo | Identidade + regras + descrição de tools | Memórias sobre identidade |
| `_indices/_auditoria-mem0.md` | arquivo gerado | Relatório auto-gerado das memórias | Memória |
| `_log/resumos-mem0/AAAA-MM-DD.md` | arquivo gerado | Log auditável dos resumos extrativos do dia | Memória |
| `gus-memoria-export.md` + `.json` | arquivos gerados | Snapshot diário do brain `gustavo` | Fonte de verdade — Mem0 cloud é a fonte |
| `_indices/<area>.md` | arquivo MD curado | Dashboard estático por área | Memória semântica |

Regra: **memória só é o que está no Mem0 cloud** (acessível via SDK MemoryClient). O resto é **derivado** ou **identidade**, não memória.

---

## 4. Onde cada tag é setada hoje

### 4.1 `telegram-claude` (default do bot)

`gus/memory.py:VIA_DEFAULT` lê `MEM0_VIA_TAG` do env. No deploy do Railway,
`MEM0_VIA_TAG` não está setado explicitamente, então usa default da linha:

```python
VIA_DEFAULT = os.getenv("MEM0_VIA_TAG", "telegram-claude")
```

Se quisesse mudar (ex: deploy paralelo do bot com cérebro GPT), bastaria
adicionar `MEM0_VIA_TAG=telegram-gpt` no env do segundo deploy.

### 4.2 `claude-code` (default do MCP)

`.claude/mcp/mem0_server.py:VIA_TAG`:

```python
VIA_TAG = os.environ.get("MEM0_VIA_TAG", "claude-code")
```

Setado por `~/.claude/gus.env` quando configurado:

```bash
MEM0_VIA_TAG=claude-code
```

Se for distinguir Web vs Local, dá pra usar `claude-code-web` / `claude-code-local`.
Mas pra V1, `claude-code` basta.

### 4.3 Outras (planejadas)

Cada nova porta seta `MEM0_VIA_TAG=<tag>` no seu próprio deploy. Sem mudança no código.

---

## 5. Como filtrar por origem

### Search filtrado (Python SDK Mem0):

```python
# Tudo (default — visibilidade cruzada)
client.search("query", user_id="gustavo")

# Só do Telegram com cérebro Claude
client.search(
    "query",
    user_id="gustavo",
    filters={"metadata": {"via": "telegram-claude"}}
)

# Só do Claude Code
client.search(
    "query",
    user_id="gustavo",
    filters={"metadata": {"via": "claude-code"}}
)

# Comparar 2 portas — duas chamadas separadas
```

### Via MCP daqui (quando ativar):

Hoje as tools MCP não expõem `filters`. Se virar caso de uso real,
adicionar param `filtro_via` em `buscar_memorias` (1 linha de código).

---

## 6. Limitação retroativa

**Memórias salvas ANTES de 2026-04-25 15:20 BRT NÃO TÊM TAG.** São indistinguíveis quanto à origem.

Pra estimar origem das 128 atuais:
- Claude Code (esta porta): praticamente zero (MCP não tinha key configurada)
- Bot Telegram: ~100% das memórias automáticas (resumo a cada 3 turnos)
- Workflows GH: nenhuma (nenhum salva hoje)

Daqui pra frente, distinção é confiável.

---

## 7. Decisões pendentes

| Decisão | Estado |
|---|---|
| Tagar workflows GH quando começarem a salvar | A fazer no momento que algum começar |
| Distinguir `claude-code-web` vs `claude-code-local`? | Não — V1 usa só `claude-code` |
| Distinguir cérebro do bot (claude vs haiku fallback) na tag? | Não — `via` é canal, não modelo |
| Adicionar filtro `via` nas tools MCP de busca? | Só se virar dor real |

---

## 8. Como atualizar este doc

Quando aparecer porta nova ou tag nova:
1. Adicionar linha na tabela 2.1 ou 2.2
2. Atualizar `atualizado:` no frontmatter
3. Se mudou comportamento default de algum salvador, atualizar também `projetos/gus/gus-12-portas-futuras.md`

Relacionado: [[gus-12-portas-futuras]], [[gus-11-tools-roadmap]], [[gus-01-visao-geral]]
