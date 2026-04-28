---
tipo: blueprint-spec
componente: pre-requisitos
ordem: 2
---

# Pré-requisitos

Antes de começar a implementar, garantir que tem:

## 1. Contas externas

Stack default opinionada deste blueprint. Substituições são possíveis
mas exigem adaptação dos templates.

| Serviço | Pra que serve | Custo esperado | Nível de obrigatoriedade |
|---|---|---|---|
| **Anthropic** (console.anthropic.com) | LLM principal (Claude) — bot Telegram, curador de memória, todas as portas internas | ~US$3–25/mês conforme uso | Obrigatório |
| **Qdrant Cloud** (cloud.qdrant.io) | Vector store da memória persistente | US$0 (free tier 4GiB sem expirar) | Obrigatório |
| **GitHub** (github.com) | Vault de conhecimento + Actions (automação) + sync com Drive | US$0 (plano Free é suficiente) | Obrigatório |
| **Railway** (railway.app) | Deploy 24/7 do bot Telegram | US$5 inicial + free tier de execução | Obrigatório se Telegram |
| **Telegram Bot** (@BotFather) | Bot novo com token | US$0 | Obrigatório se Telegram |
| **Google Cloud OAuth** | Auth pro sync GitHub ↔ Drive | US$0 | Opcional (se quer sync Drive) |
| **Tavily** (tavily.com) | Busca web pela tool do agente | US$0 (free tier 1000 buscas/mês) | Opcional |
| **OpenAI** (platform.openai.com) | Tool "second opinion" (GPT) + Whisper pra transcrição de áudio | US$1–5/mês conforme uso | Opcional |
| **ChatGPT Builder** (chatgpt.com) | Pra criar Custom GPT (porta voz mobile) | Plus US$20/mês | Opcional |

## 2. Custo mensal esperado (estimativa)

Cenário típico: 50 mensagens/dia no Telegram + curador automático +
crons diários.

| Item | Custo/mês |
|---|---|
| Anthropic Claude (Sonnet + Haiku) | ~US$10–25 |
| Railway runtime | US$5 (cobre uso baixo) |
| Qdrant Cloud | US$0 (free tier) |
| Tavily, GitHub, Drive, Telegram | US$0 |
| OpenAI (se usar) | ~US$1–5 |
| **Total** | **~US$15–35/mês** |

Pra reduzir: usar só Haiku (mais barato), limitar mensagens/dia, evitar
processamento de imagem em alto volume.

## 3. Conhecimento mínimo do dono

Você **não precisa programar**. Mas precisa:

- Saber o que é GitHub (repositório, commit, branch)
- Conseguir editar arquivos `.md` em editor de texto
- Topar interagir com IA (Claude Code ou similar) pra implementação
- Confortável em painéis administrativos web (Railway, GitHub Settings,
  Google Cloud Console)
- Topar ler instruções em inglês quando aparecem em telas (a maioria das
  contas externas é em inglês)

## 4. Conhecimento mínimo da IA implementadora

A IA que vai executar o blueprint precisa:

- Acesso a este repositório de blueprint
- Capacidade de criar arquivos, fazer commits, abrir PRs (Claude Code,
  GitHub Copilot Workspace, ou similar)
- Tools de leitura web (pra consultar docs Anthropic, Qdrant, etc.
  quando precisar)
- Modelo de **alta capacidade** pra entender arquitetura — Claude
  Sonnet / Opus, GPT-4 / GPT-5, ou equivalentes. Modelos pequenos
  (Haiku, GPT-3.5) podem ser usados pra subtarefas mas não pra
  decisões arquiteturais

## 5. Hardware

- Computador com navegador (qualquer SO) — só pra acessar painéis
  web e revisar código
- Smartphone com Telegram instalado — pra interagir com o agente em
  produção

Não precisa máquina local rodando código. Tudo cloud.

## 6. Tempo

- Setup inicial: ~10-12h ao longo de 2-4 dias
- Operação contínua: ~5-15min/dia pra revisar saves de memória,
  responder demandas em fila, etc.
- Manutenção semanal: ~30min pra ler retrospectiva, ajustar pendências
- Manutenção mensal: ~1h pra rever decisões arquiteturais, custos

## 7. Decisões a tomar antes de começar

Marque com X o que tá decidido:

- [ ] Nome do agente: ____________ (sugestões: nome curto, único,
      sem ambiguidade com produtos existentes)
- [ ] Propósito: assistente geral? especializado em X? (uma frase)
- [ ] Tom: formal? informal? português br informal? bilíngue?
- [ ] 3-5 princípios não-negociáveis (ex: "não alucinar", "crítica
      direta", "verificar antes de afirmar ausência")
- [ ] Domínios de conteúdo: pessoal, profissional, ambos?
- [ ] Portas iniciais: Telegram só? + outras?
- [ ] Orçamento mensal aceito: ____________ US$/mês

Não precisa todas decididas pra começar — mas as 3 primeiras (nome,
propósito, tom) são bloqueantes pra escrever a identidade canônica.

## Próximo passo

Depois de garantir os pré-requisitos: ler `passo-a-passo-resumido.md`.
