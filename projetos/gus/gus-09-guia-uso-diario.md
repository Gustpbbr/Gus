---
tipo: documentacao-projeto
projeto: gus
parte: 9-guia-uso-diario
atualizado: 2026-04-24
---

# Gus — Guia prático de uso diário

Lista de comandos e fluxos que funcionam na prática no bot do Telegram (`@Tiogubot`). Organizado por intenção.

## Captura rápida

### Salvar um exame
```
"Recebi exame de sangue hoje. Segue os valores: TSH 0.8, T4L 1.3, T3 120. Salva pra mim."
```
Bot extrai os dados, cria `pessoal/saude/exame-sangue-<mes>-<ano>.md` com tabela de valores, e atualiza `pessoal/saude/historico-saude.md` se já existir.

### Registrar um treino
```
"Fiz 45min de corrida hoje, pace médio 5:30. Saí cedo."
```
Cria `esportes/treinos/treino-<data>.md` com frontmatter e contexto. Atualiza `esportes/evolucao.md` se existir.

### Capturar uma ideia
```
"Ideia pro Phronesis: benchmark de hypercompilation com tasks de refatoração multi-arquivo."
```
Bot decide onde salvar. Se o tema já tem pasta, vai pra lá. Se for novo mas importante, cria pasta nova. Se for solto, vai em `capturado/ideias/`.

### Salvar um link/artigo
```
"Guarda esse link com um resumo em 5 bullets: [URL]"
```
Busca o conteúdo, gera resumo, salva em `capturado/links/<titulo>.md` com `fonte:` no frontmatter.

### Transcrever PDF
Manda o PDF direto no Telegram (arrastando). Bot processa:
- Com texto: extrai e salva como MD
- Escaneado/visual: renderiza como imagens e analisa com Vision

## Consultas

### Memória ativa
```
"O que tu lembra sobre o Phronesis?"
"Quais memórias recentes tu tem sobre minha saúde?"
"O que sabe sobre a casa em Paty do Alferes?"
```
Bot usa `search_memory` pra buscar ativamente no Mem0 por tema.

### Leitura de arquivo específico
```
"Abre o histórico de saúde"
"Lê o índice de projetos"
"Me mostra o gus-08-plano-proximos-passos"
```
Bot chama `read_from_github` com o path certo.

### Explorar pasta
```
"O que tem em _indices?"
"Lista os arquivos em pessoal/saude"
"Quais projetos têm pasta no repo?"
```
Bot chama `list_github_directory`.

### Busca na web
```
"Busca: últimas diretrizes brasileiras pra hipertireoidismo"
"Preço atual de bitcoin"
"Qual o horário do pôr do sol hoje no Rio?"
```
Bot chama `search_web` (Tavily primeiro, DDG fallback).

## Histórico

### O que mudou
```
"O que mudou essa semana?"
"Últimos 5 commits no repo"
"Qual foi a última edição em historico-saude.md?"
```
Bot chama `list_commits` com filtros.

### Evolução de tema
```
"Como o Phronesis evoluiu nos últimos 30 dias?"
```
Bot combina `list_commits(path="projetos/phronesis-bench", since_days=30)` + `read_from_github` dos principais arquivos.

## Dados sensíveis

### Fluxo normal
```
"Salva um arquivo com meu CPF 123.456.789-00"
```
Bot **detecta** o CPF e **NÃO salva**. Responde com 3 opções:
- **(a)** salvar em `sensivel/identidade/`
- **(b)** forçar no path original
- **(c)** cancelar

Tu responde (a), (b) ou (c). Bot só salva depois de confirmação explícita.

### O que o scan detecta
- CPF (formatos com ou sem pontuação)
- CNPJ
- Cartão de crédito (13-19 dígitos)
- API keys (Anthropic `sk-ant-`, OpenAI `sk-`, GitHub `ghp_`/`github_pat_`, Mem0 `m0-`, Tavily `tvly-`)

### Pasta `sensivel/`
- Excluída do sync pra Google Drive (quando ativado).
- Subestrutura sugerida: `identidade/`, `financeiro/`, `contatos/`, `credenciais/`, `documentos/`.
- Bot só salva aí com confirmação explícita tua.

## Comandos do bot

| Comando | Efeito |
|---------|--------|
| `/start` | Boas-vindas. Se `TELEGRAM_CHAT_ID` vazio, mostra teu chat_id. |
| `/reset` | Limpa histórico da conversa em memória. Dispara save de resumo do trecho pendente antes de zerar. |

## Troubleshooting

### "Tive um problema interno. Tenta de novo em instantes."
Erro genérico. Causa possível:
- **Anthropic 529 overload:** a mensagem nova é *"A API tá sobrecarregada..."*. Se aparecer a genérica, é outro bug.
- **Erro 4xx na API:** deploy antigo no ar, ou tools com schema errado. Verificar logs Railway.
- **Exceção não prevista:** logs Railway `ERROR - Erro ao processar mensagem: ...` mostra a causa real.

### "API da IA tá sobrecarregada agora (status X)"
Mensagem amigável. Claude ou Haiku tentou 4 vezes e falhou. Espera 1-2 min e manda de novo.

### Bot ignora mensagem ("Bot privado")
`TELEGRAM_CHAT_ID` no Railway não bate com teu chat real. Checar se não tem espaço ou caractere extra na variável.

### Bot não acha um arquivo que tu sabe que existe
Tu pode pedir explicitamente:
```
"Usa list_github_directory em [pasta] pra confirmar"
```
Se o arquivo aparecer na listagem mas o bot não lê, talvez seja case-sensitive (`README.md` ≠ `readme.md`).

### Memória não atualiza
- **Mem0 tem latência de indexação** (minutos). Uma memória salva agora pode não aparecer na busca imediata.
- Pra validar que foi salva: `search_memory` com query bem específica do conteúdo recente.
- Ou checa `app.mem0.ai` → Dashboard → Memories direto.

### Rate limit disparou
Mandou mais de 20 msgs em 60s. Espera uns segundos. `RATE_LIMIT_MSG_PER_MINUTE` no Railway ajusta o teto.

### Custo mensal estourando
`HARD_LIMIT_USD_MONTH` corta chamadas até o próximo mês. Pra monitorar: (futuro) `/custo` comando, ou ver `logs/gus_metrics.jsonl` no Railway. Cuidado: logs não persistem sem volume.

## Padrões recomendados

### Fluxo saúde
1. Recebeu exame → manda foto ou PDF pro bot
2. Bot transcreve em tabela, salva em `pessoal/saude/`
3. Pergunta ao bot: *"compara com exame anterior de janeiro"*
4. Periodicamente: *"me dá estado atual da minha saúde"* → bot lê índice + histórico + últimos exames

### Fluxo projeto
1. Mexeu em algo importante no Phronesis? Manda decisão ou contexto pro bot
2. Bot salva em `projetos/phronesis-bench/...` ou atualiza estado existente
3. Fim da semana: retrospectiva automática (quando ativada) consolida em `pessoal/diario/semana-AAAA-WW.md`

### Fluxo captura em movimento
1. Pensou em algo no carro, no sítio, em qualquer lugar → manda áudio? texto? foto?
2. Por enquanto **só texto, foto, PDF** funciona (áudio via Whisper é fase 3).
3. Bot decide onde salvar. Se errar a categoria, tu redireciona: *"move pra outra pasta"*

## Limites conhecidos

- **Só branch main:** não lê/escreve em outras branches.
- **Sem diff de commits:** vê o commit mas não o que mudou linha-a-linha. Se precisar, acessa GitHub web.
- **Sem áudio** (ainda).
- **Sem Drive** (ainda — bloqueado por política Google).
- **Sem Calendar** (Fase 3).

Relacionado: [[gus-02-implementado]], [[gus-04-seguranca-protecao]], [[gus-05-portas-capacidades]], [[gus-08-plano-proximos-passos]]
