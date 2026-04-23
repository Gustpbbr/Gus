---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: pendente
fase: 3-5
---

# Gus — Novas Portas e Capacidades (Fases 3 e 5)

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

## Alexa como porta de voz (Fase 5)

### Conceito
Alexa funciona como microfone e alto-falante — só captura e reproduz. A inteligência é Claude API com o mesmo Mem0 e GitHub do Gus. Uso principal: mãos livres em casa (cozinhando, acordando, etc.) para pedidos pontuais e conversa contextual.

### Arquitetura

```
Voz do Gustavo
    ↓
Alexa (transcreve voz → texto)
    ↓
AWS Lambda (orquestrador)
    ↓
Claude API + Mem0 + GitHub (mesmos do Gus)
    ↓
Lambda formata resposta
    ↓
Alexa fala a resposta
```

### Como implementar
1. Criar Alexa Skill custom (console Amazon Developer)
2. Lambda em Python como backend — basicamente `llm.py` + `tools.py` adaptados
3. Conectar ao mesmo Mem0 (user_id "gustavo") e GitHub (Gustpbbr/Gus)
4. System prompt: carregar gus-identity.md
5. Histórico de sessão: DynamoDB ou Mem0 (evitar duplicar memória)

### Componentes AWS
- **Alexa Skill** — configuração JSON, define intents e slots
- **Lambda** — código Python, recebe texto da Alexa, chama Claude, retorna resposta
- **DynamoDB** (opcional) — histórico de sessão de voz (se Mem0 não cobrir)
- **IAM** — permissões entre serviços

### Latência esperada
- Alexa transcreve: ~1s
- Lambda → Claude API: 2-5s
- Tool use (se houver): +2-3s por tool
- Alexa fala resposta: ~1-2s
- **Total: 5-10s** — aceitável pra pedidos pontuais, não pra diálogo rápido

### Casos de uso
- "Alexa, pergunta pro Gus como tá o Phronesis-Bench"
- "Alexa, pede pro Gus marcar consulta com endocrinologista dia 25"
- "Alexa, fala pro Gus salvar que mudei o tapazol pra 10mg"
- Conversa mais longa tipo ChatGPT voice — possível mas com pausas maiores

### Pré-requisitos
- [ ] Custom GPT funcionando (valida que Mem0 + GitHub via API externa funciona)
- [ ] Conta AWS + conta Amazon Developer
- [ ] Whisper já implementado no Telegram (valida transcrição pt-BR)

### Por que Fase 5 (última)
- Maior complexidade de infra (AWS Lambda, IAM, Alexa console, certificação)
- Custom GPT por voz no celular resolve 80% do caso de uso com 10% do esforço
- Telegram + Whisper resolve áudio sem infra nova
- Alexa é o "luxo" — mãos livres em casa, pra quando todo o resto já funciona

Relacionado: [[gus-01-visao-geral]], [[gus-04-seguranca-protecao]], [[gus-06-autonomia-acoes]]
