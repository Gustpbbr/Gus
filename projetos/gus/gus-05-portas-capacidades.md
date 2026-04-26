---
tipo: documentacao-projeto
projeto: gus
parte: 5-de-7
atualizado: 2026-04-23
---

# Gus — Novas portas e capacidades (Fases 3 e 5)

Aqui entra o que **ainda não existe** mas está mapeado. A ordem é Fase 3 → Fase 4 ([[gus-06-autonomia-acoes]]) → Fase 5. Cada item é opcional — pode implementar um sem os outros.

## Fase 3 — capacidades novas

### Custom GPT no ChatGPT (porta de voz e criatividade)

**Por quê:** o ChatGPT mobile tem modo de voz decente em pt-BR e suporte a Actions (chamadas HTTP para APIs externas). Vira uma porta do Gus sem precisar manter infra própria.

**Como:**
1. ChatGPT → Create GPT → importar `dialogos/_bootstrap/gus-identity.md` como instruções.
2. **Actions** apontando para dois endpoints próprios (HTTP simples, deploy no Railway ao lado do bot):
   - `POST /mem0/search` — proxy autenticado do Mem0 `search()`
   - `POST /github/save` — proxy que chama a mesma lógica de `_save_to_github`
3. OAuth ou API key fixa no header — só tu usa.

Limitação: ChatGPT não expõe identidade do chamador, então o endpoint precisa ter autenticação própria. Simples de resolver.

### Whisper — transcrição de áudio no Telegram

**Por quê:** gravar áudio é o jeito mais rápido de capturar pensamento em movimento. Hoje o bot só aceita texto, foto e PDF.

**Como:** adicionar handler de `filters.VOICE` em `bot.py`, baixar o `.ogg`, enviar para Whisper API (`whisper-1`, pt-BR), injetar o texto transcrito como se tivesse vindo por escrito. Custo marginal, latência baixa.

### Google Calendar como tool

**Por quê:** "Gus, qual meu próximo plantão?" e "Gus, agenda reunião com o Fulano quarta às 14h" viram naturais. Hoje o Gus não tem acesso à agenda.

**Como:** service account com escopo `calendar.events`, duas tools novas em `tools.py`:
- `list_events(range, max)` — próximos N eventos num intervalo
- `create_event(title, start, end, notes)` — cria evento

A mesma service account do Drive sync pode ser reaproveitada com escopo adicional.

### Briefing matinal proativo

**Por quê:** Gus só reage hoje. Um bom assistente antecipa.

**Como:** GitHub Action cron `0 10 * * *` UTC (7h Brasília) que:
1. Lê memórias do Mem0 (pendências, projetos ativos)
2. Lê próximos eventos do Calendar
3. Consulta `esportes/evolucao.md`, `pessoal/saude/historico-saude.md`
4. Gera briefing curto (3-5 linhas) via Claude
5. Envia no Telegram via Bot API direta (sem depender do bot rodando polling)

Regras: só manda em dias úteis, pula se Gustavo mandou /reset nas últimas 2h, máximo 3 linhas.

### Retrospectiva semanal automática

**Por quê:** capturar o que rolou na semana sem depender da disciplina do Gustavo.

**Como:** cron sexta-feira 20h BRT. Lê logs do Mem0 da semana, memórias novas adicionadas, `.md` criados no GitHub nos últimos 7 dias. Gera `pessoal/diario/semana-[YYYY-WW].md` com resumo por tema (saúde, projetos, capturado). Sync Drive espelha automático.

### Obsidian Bases — dashboards queryáveis

**Por quê:** o plugin Bases (do kepano/obsidian-skills) permite criar views dinâmicas a partir de frontmatter. Hoje a organização é só por pasta.

**Como:** padronizar frontmatter nos `.md` criados pelo Gus:
- Exames: `tipo`, `data`, `valores_alterados`
- Treinos: `tipo`, `duracao`, `intensidade`
- Projetos: `status`, `prioridade`, `ultima_atualizacao`

Depois criar bases no Obsidian: "exames com valor fora do range", "treinos da última semana", "projetos parados há >14 dias". Zero código adicional — só convenção.

## Fase 5 — Alexa (voz mãos livres em casa)

**Por quê:** o ChatGPT no celular resolve voz quando tu tá em movimento. Em casa, Alexa é mais natural — sem tirar o celular do bolso.

**Fricções reais (não romantizar):**

- **Timeout de Skill custom:** ~8s pra resposta final, ~24s com progressive response. Tool use do Claude pode estourar.
- **STT pt-BR** tem qualidade pior pra termos técnicos (nomes de medicamento, Phronesis, hipóxia). Melhor pra perguntas curtas e frases comuns.
- **Invocação:** "Alexa, fala com o Claude" não funciona — nome de invocação custom precisa ser registrado ("Alexa, abrir Gus").

**Arquitetura proposta:**

```
Alexa Echo  →  Alexa Skill  →  AWS Lambda (Python)
                                    ↓
                          Mem0 + GitHub + Claude API
                                    ↓
                              Resposta (voz + card)
```

A Lambda reutiliza **80% do código que já existe**:
- `gus/memory.py` → idêntico
- `gus/tools.py` → idêntico
- `gus/llm.py` → idêntico
- Handler novo no lugar de `bot.py`

Não é reescrita — é uma porta nova na casa que já existe.

**Padrão async para contornar o timeout:**

Para pergunta que exige tool use (ler Drive, buscar web), a Alexa responde "tô olhando, já te aviso" e a Lambda processa em background, terminando com uma notification no app Alexa ou num card no Echo Show.

Para pergunta que cabe em memória pura (<3s), responde síncrono mesmo.

**Pré-requisito:** Custom GPT funcionando primeiro. Ele valida a mesma arquitetura (API externa consumindo Mem0 + GitHub) num ambiente com tolerância de tempo maior.

## O que fica de fora mesmo com tudo pronto

Nenhuma porta de voz vai suportar:
- Criação de artefatos interativos (HTML, React, Canvas)
- Documentos complexos (.docx, .xlsx) editáveis ao vivo
- Busca em conversas antigas do claude.ai (não são expostas via API)

Essas coisas vão continuar morando no Claude Code e no Claude Chat.

Relacionado: [[gus-02-implementado]], [[gus-06-autonomia-acoes]], [[gus-07-decisoes-descartadas]]
