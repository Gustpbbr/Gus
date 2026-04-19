---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: pendente
fase: 3
---

# Gus — Novas Portas e Capacidades (Fase 3)

Expansões planejadas após deploy e segurança estarem estáveis.

## Custom GPT (ChatGPT como porta do Gus)

### Conceito
O ChatGPT vira mais uma porta de acesso ao Gus, não um sistema paralelo. O "Kai" (como Gustavo chama o ChatGPT) acessaria os mesmos dados: Mem0 para memória, GitHub para arquivos.

### Como implementar
1. Criar Custom GPT no ChatGPT Plus
2. Configurar Actions (API endpoints que o GPT pode chamar):
   - **Mem0 API** direta: buscar e salvar memórias
   - **GitHub API** direta: ler e criar .md
3. Nas instruções do GPT, colar conteúdo de gus-identity.md
4. O GPT teria personalidade diferente (mais criativo, "Kai"), mas mesma base de dados

### Schema das Actions
```yaml
# Mem0 - buscar memórias
GET https://api.mem0.ai/v1/memories/search
Headers: Authorization: Bearer {MEM0_API_KEY}
Body: { "query": "...", "user_id": "gustavo" }

# Mem0 - salvar memória
POST https://api.mem0.ai/v1/memories/
Headers: Authorization: Bearer {MEM0_API_KEY}
Body: { "messages": [...], "user_id": "gustavo" }

# GitHub - ler arquivo
GET https://api.github.com/repos/Gustpbbr/Gus/contents/{path}
Headers: Authorization: Bearer {GITHUB_TOKEN}

# GitHub - criar/atualizar arquivo
PUT https://api.github.com/repos/Gustpbbr/Gus/contents/{path}
Headers: Authorization: Bearer {GITHUB_TOKEN}
Body: { "message": "...", "content": "base64...", "sha": "..." }
```

### Notas
- Não precisa de API Anthropic (o GPT usa modelo próprio)
- As chaves ficam configuradas nas Actions do Custom GPT (seguras)
- O ponto chave: mesmo Mem0 + mesmo GitHub = mesmo Gus, porta diferente

## Whisper (transcrição de áudio)

### Conceito
Receber áudio no Telegram e transcrever para texto antes de processar.

### Como implementar
- Usar OpenAI Whisper API (paga, melhor qualidade pt-BR) ou whisper.cpp local
- No bot.py, adicionar handler de voice message
- Transcrever → usar texto como input normal do LLM
- Salvar transcrição no Mem0 como contexto

### Trade-off
- Whisper API: simples, custo por minuto, boa qualidade pt-BR
- whisper.cpp local: grátis, mas precisa de mais recursos no Railway
- Recomendação: começar com API, migrar se custo justificar

## Google Calendar

### Conceito
Gus consegue ler e criar eventos no Google Calendar.

### Como implementar
- Nova tool: `manage_calendar` (read/create/update)
- Google Calendar API com Service Account
- Adicionar ao tools.py com mesma estrutura das tools existentes

### Casos de uso
- "Gus, que compromissos tenho amanhã?"
- "Marca consulta com endocrinologista dia 25 às 14h"
- Integração com action queue (Fase 4)

## Briefing matinal automático

### Conceito
Todo dia de manhã, Gus manda mensagem proativa no Telegram com resumo do dia.

### Como implementar
- GitHub Action com cron (7h BRT)
- Script que: lê Calendar, lê pendências, lê Mem0 para contexto
- Monta mensagem e envia via Telegram Bot API
- Ou: implementar no próprio bot com APScheduler

### Conteúdo do briefing
- Compromissos do dia
- Pendências abertas (se action queue existir)
- Lembretes baseados em memórias recentes

## Retrospectiva semanal

### Conceito
Toda sexta, Gus gera resumo da semana: o que foi feito, o que ficou pendente, padrões observados.

### Como implementar
- GitHub Action semanal (sexta 18h BRT)
- Script que: analisa commits da semana, lê Mem0, gera relatório
- Salva em `pessoal/diario/retrospectiva-semana-XX.md`

## Obsidian Skills (kepano/obsidian-skills)

### Conceito
Skills oficiais do criador do Obsidian que dão ao Claude Code superpoderes sobre o vault. Quando o repo Gus é o vault do Obsidian, essas skills permitem que o Claude Code opere diretamente sobre os MDs com sintaxe correta e ferramentas avançadas.

### Skills disponíveis

| Skill | Função | Uso no Gus |
|-------|--------|------------|
| obsidian-cli | Controla Obsidian rodando (ler, criar, buscar notas, screenshots) | Navegar vault, buscar notas por conteúdo |
| obsidian-markdown | Garante sintaxe Obsidian (wikilinks, embeds, callouts, frontmatter) | Criar MDs com formatação rica |
| obsidian-bases | Views tipo banco de dados (tabelas, cards, filtros sobre MDs) | Dashboard de saúde, projetos, finanças |
| json-canvas | Mapas visuais (.canvas) com nós e conexões | Visualizar arquitetura, fluxos |
| defuddle | Limpa páginas web → markdown legível | Salvar links em capturado/links/ com conteúdo limpo |

### Impacto
- **defuddle** melhora a tool search_web — conteúdo mais limpo, menos tokens
- **obsidian-bases** permite criar dashboards queryáveis (ex: "todos os exames de 2026", "treinos do mês")
- **obsidian-markdown** garante que wikilinks e frontmatter sigam o padrão
- **obsidian-cli** exige Obsidian rodando no PC — funciona quando Gustavo está no computador

### Instalação
```bash
npx skills add git@github.com:kepano/obsidian-skills.git
```

Relacionado: [[gus-01-visao-geral]], [[gus-04-seguranca-protecao]], [[gus-06-autonomia-acoes]]
