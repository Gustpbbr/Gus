# BRIEFING — Instruções para Opus executar o Gus completo

**Tipo:** prompts-templates + manual  
**Data:** 2026-04-09  
**Destino:** colar numa aba Opus com acesso ao projeto memória-viva  
**Conexão:** gus-conceito-produto.md, gus-modelo-negocio.md, gus-telegram-config.md

---

## Contexto para o Opus

Você é o Claude Code com acesso ao projeto do Gustavo. Sua missão é implementar o **Gus** — um AGI pessoal baseado em Telegram que integra MemPalace + Mem0 + API Anthropic.

O Gustavo não programa diretamente. Ele confirma ações, fornece credenciais quando pedido, e valida resultados. Você executa tudo.

---

## Regras de execução

1. **Sempre verificar antes de instalar** — checar se já está instalado antes de rodar pip install
2. **Um passo de cada vez** — não fazer tudo de uma vez, confirmar cada etapa antes de avançar
3. **Paths do Windows** — usar sempre barras invertidas `\` ou raw strings `r"caminho"`
4. **Nunca hardcodar credenciais** — sempre usar arquivo de configuração separado
5. **Criar backups** — antes de editar qualquer arquivo existente, fazer cópia com sufixo `.bak`
6. **Testar cada componente isolado** — antes de integrar, confirmar que cada peça funciona sozinha
7. **Logging em tudo** — cada script deve gerar log em arquivo, não só no terminal
8. **Tratamento de erro** — nunca deixar script quebrar silenciosamente, sempre capturar e logar erros

---

## Ordem de execução recomendada

### FASE 1 — Verificar fundação (já feito, só confirmar)
- [ ] MemPalace instalado: `mempalace status`
- [ ] MCP configurado no `.claude.json`
- [ ] Mem0 configurado com API key
- [ ] Testar busca: `mempalace search "phronesis"`

### FASE 2 — CLAUDE.md orquestrador
Criar arquivo `CLAUDE.md` na raiz do projeto com:
- Instrução para usar MemPalace antes de responder sobre projetos
- Instrução para carregar perfil do Mem0 no início de cada sessão
- Estilo de comunicação do Gus (direto, sem enrolação, com contexto)
- Roteamento de modelos por tipo de tarefa

### FASE 3 — Script principal do Gus
Arquivo: `gus/gus_core.py`

Usar **python-telegram-bot v20+** (assíncrono — mais estável)
Usar **mem0ai** para memória de identidade
Usar **anthropic** SDK oficial

Estrutura do script:
```
gus/
├── gus_core.py          ← bot principal
├── gus_scheduler.py     ← mensagens proativas
├── gus_memory.py        ← interface com MemPalace + Mem0
├── gus_router.py        ← roteamento de modelos
├── gus_config.json      ← credenciais e configurações
└── logs/
    └── gus.log          ← log de tudo
```

### FASE 4 — Roteamento de modelos
Lógica no `gus_router.py`:

```python
# Critérios de roteamento
HAIKU = ["lembra", "salva", "categoriza", "lista", "ok", "sim", "não"]
OPUS = ["decide", "arquitetura", "estratégia", "análise", "phronesis", "ter"]
# Todo o resto → Sonnet
```

Adicionar contagem de tokens estimada no log para monitoramento de custo.

### FASE 5 — Scheduler proativo
Arquivo: `gus/gus_scheduler.py`

3 horários padrão: 07:00, 13:00, 21:00
Configurar via **Windows Task Scheduler** — não via loop infinito (consome recursos)
Cada execução:
1. Consulta MemPalace por pendências recentes
2. Consulta Mem0 por contexto pessoal
3. Gera mensagem curta (máx 3 linhas)
4. Envia no Telegram
5. Loga resultado

### FASE 6 — Testes
- Testar bot respondendo "oi"
- Testar busca no MemPalace via Telegram
- Testar mensagem proativa manualmente
- Testar roteamento de modelos
- Verificar logs

---

## Decisões técnicas já tomadas

| Componente | Escolha | Motivo |
|---|---|---|
| Interface | Telegram | Menor fricção, já instalado |
| Memória projetos | MemPalace local | Privado, gratuito, 1494 arquivos já minerados |
| Memória identidade | Mem0 OSS | Open source, sem dependência cloud |
| Scheduler | Windows Task Scheduler | Nativo, sem processo em background |
| Logs | Arquivo local | Simples, auditável |
| Config | JSON único | Fácil de editar, separado do código |

---

## Decisões técnicas a evitar

- ❌ **Não usar** Mem0 cloud — usar versão OSS local
- ❌ **Não usar** polling loop infinito para o bot — usar webhooks ou long polling com timeout
- ❌ **Não usar** threading complexo — python-telegram-bot v20 já é assíncrono
- ❌ **Não hardcodar** horários do scheduler no código — manter no JSON
- ❌ **Não usar** SQLite próprio — MemPalace e Mem0 já têm seus bancos

---

## Credenciais necessárias (Gustavo fornece quando pedido)

1. **Telegram Bot Token** — obtido no BotFather
2. **Telegram Chat ID** — obtido após mandar /start pro bot
3. **Anthropic API Key** — já tem (plano Max)
4. **Mem0 API Key** — já obtida
5. **Google OAuth** — para Drive (fase posterior)

Pedir uma de cada vez, nunca todas de uma vez.

---

## Como lidar com erros comuns no Windows

**Problema: path com espaços**
```python
# Errado
path = "C:\Users\Gustavo\Desktop\CLAUDE\Projetos Antigos"
# Certo
path = r"C:\Users\Gustavo\Desktop\CLAUDE\Projetos Antigos"
```

**Problema: encoding de caracteres brasileiros**
```python
# Sempre abrir arquivos com encoding explícito
open(file, 'r', encoding='utf-8')
```

**Problema: PowerShell vs CMD**
- Gustavo usa PowerShell
- Comandos Unix-style não funcionam
- Usar sempre sintaxe PowerShell

**Problema: pip install falha**
```
# Tentar primeiro
pip install pacote
# Se falhar
python -m pip install pacote
# Se ainda falhar
python -m pip install pacote --user
```

---

## Definição de sucesso da sessão

A sessão está completa quando:
- [ ] Gustavo manda "oi" no Telegram e o Gus responde com contexto dos projetos
- [ ] Gus menciona pelo menos um projeto ativo corretamente
- [ ] Log mostra qual modelo foi usado na resposta
- [ ] Scheduler configurado para rodar amanhã às 7h

---

## Prompt de abertura sugerido para o Opus

```
Leia os seguintes documentos nesta ordem:
1. gus-conceito-produto.md
2. gus-modelo-negocio.md  
3. gus-telegram-config.md
4. Este briefing

Depois verifique o estado atual do ambiente:
- mempalace status
- Verificar se .claude.json tem MCP configurado
- Verificar se Mem0 está configurado

Me diga o que já está pronto e o que falta fazer.
Aguarde minha confirmação antes de começar a executar.
```

---

---

## FASE V2.0 — Gus executa tarefas autônomas via GitHub

### O que muda
O Gus passa de respondente para executor. Não só gera código — commita, publica e avisa.

### Fluxo completo
```
Você no Telegram: "Gus, faz um site sobre leões"
        ↓
Script Python recebe
        ↓
API Anthropic gera o código
        ↓
API GitHub faz o commit no repositório
        ↓
Netlify detecta commit e publica automaticamente
        ↓
Gus manda o link no Telegram
```

### O que o Claude Code NÃO é nesse fluxo
O Claude Code é uma interface para conversa. O Gus usa a API Anthropic diretamente — mesmo motor, sem interface visual. O GitHub é acionado via API, não via Claude Code.

### O que precisa configurar
Adicionar ao `gus_config.json`:
```json
{
  "github_token": "SEU_TOKEN_GITHUB",
  "github_repo": "usuario/repositorio",
  "github_branch": "main",
  "netlify_auto_deploy": true
}
```

O token do GitHub é gerado em:
`GitHub → Settings → Developer Settings → Personal Access Tokens`

O Claude Code provavelmente já usa um — pode aproveitar o mesmo.

### Capacidades V2.0
- Gerar e commitar código no GitHub via Telegram
- Publicar sites no Netlify automaticamente
- Criar e atualizar arquivos nos repositórios
- Reportar resultado com link no Telegram

---

## FASE V1.5 — Demo de vendas via Telegram

### O conceito
O Telegram vira canal de vendas. Você adiciona um prospect num grupo, o Gus já sabe quem é a pessoa e demonstra ao vivo.

### Como preparar uma demo
1. Criar um "wing" temporário no MemPalace com contexto do prospect
2. Nome, profissão, dor específica, contexto relevante
3. Adicionar prospect no grupo do Telegram
4. Gus já sabe quem é — demo personalizada na hora

### Exemplo de fluxo
```
Você: "João, te adiciono num grupo pra você ver"
        ↓
Gus: "Oi João, vi que você trabalha com consultoria jurídica.
      Posso te mostrar como funcionaria pra você?"
        ↓
João experimenta ao vivo
        ↓
Venda acontece na experiência, não no pitch
```

### Por que funciona
Ninguém compra o que não entende. Todo mundo compra o que experimenta e funciona. O Telegram elimina a barreira entre explicar e demonstrar.

---

---

## FASE V3.0 — Gus como orquestrador do ecossistema completo

### O conceito
O Gus não só responde e executa tarefas simples — ele orquestra todo o ecossistema MGX que o Gustavo já construiu. É o Thalamus do Gustavo-AGI: ponto central de controle de tudo.

### Ferramentas que o Gus poderia acionar

| Comando no Telegram | O que acontece |
|---|---|
| "Gus, roda MGE no Olho Vivo" | Executa fluxo de geração de ideias no projeto |
| "Gus, CEX sobre [decisão]" | Aciona deliberação multi-perspectiva |
| "Gus, MEX no Phronesis-Bench" | Materializa próximos artefatos |
| "Gus, avalia esse texto no Bench" | Roda avaliação Phronesis-Bench |
| "Gus, qual o estado do Olho Vivo?" | Consulta MemPalace + resume estado atual |

### Fluxo exemplo
```
Você no Telegram: "Gus, roda o MGE no Olho Vivo"
        ↓
Gus acessa arquivos do projeto via MemPalace
        ↓
Executa fluxo MGE (geração de ideias)
        ↓
Gera artefatos estruturados
        ↓
Commita no GitHub
        ↓
"Pronto. MGE concluído. Aqui os resultados: [resumo]"
```

### Como implementar
Cada ferramenta vira um "comando registrado" no `gus_config.json`:

```json
{
  "comandos": {
    "mge": "executar fluxo MGE com contexto do projeto",
    "cex": "executar deliberação CEX sobre a questão",
    "mex": "materializar próximos artefatos do projeto",
    "bench": "avaliar texto no Phronesis-Bench"
  }
}
```

O Gus reconhece o comando, carrega o contexto do projeto via MemPalace, e executa via API Anthropic com o prompt correto para cada ferramenta.

### Conexão com o Segundo Cérebro
O Gus é o **Portal/Thalamus** que o Segundo Cérebro já prevê — o agente que roteia entre os outros agentes (Hippocampus, Amygdala, Prefrontal etc). A arquitetura já estava desenhada. O Telegram é a interface de acionamento.

---

## Nota

Este briefing foi construído para minimizar erros numa sessão de implementação com usuário não-programador. Cada decisão técnica foi tomada priorizando simplicidade e menor chance de falha — não a solução mais elegante, mas a mais robusta para o contexto.
