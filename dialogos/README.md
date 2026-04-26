# `dialogos/` — canal unificado entre as portas do Gus

Pasta única pra comunicação assíncrona entre as portas do Gus
(TioGu/Telegram, Claude Code, Claude Chat, Custom GPT, e o próprio Gustavo).

> Antes do 25/04/2026 noite essa pasta se chamava `dialogos-tiogu-claude/` e
> só atendia o par Telegram↔Claude Code. Agora atende todos os pares.

## Estrutura

```
dialogos/
├── README.md                 ← este arquivo (protocolo)
├── inbox-tiogu/              ← demandas pra TioGu (Telegram bot) processar
├── inbox-claude-code/        ← demandas pra Claude Code processar
├── inbox-claude-chat/        ← marcadores pra Claude Chat ler na próxima sessão
├── inbox-custom-gpt/         ← demandas pra Custom GPT processar
├── archive/                  ← demandas concluídas (move pra cá quando done)
├── processados-erro/         ← demandas com frontmatter inválido (pra debug)
└── streams/                  ← cronológico semanal (legado pré-25/04 noite)
    ├── semana-2026-04-21.md
    └── README-legado.md
```

## Fluxo de uma demanda

```
1. Origem (qualquer porta) cria arquivo .md em inbox-<destino>/
   Ex: Claude Chat cria em Gus-Sync/dialogos/inbox-tiogu/2026-04-25T23-50__teste.md no Drive

2. Workflow `import-from-drive.yml` (cron 15min) puxa do Drive pro GitHub
   - Se frontmatter válido: importa, move arquivo no Drive pra processados/
   - Se inválido: skip, deixa no Drive, loga erro
   - (opcional) Notifica Telegram quando demanda chega em inbox-tiogu/

3. Destino lê seu próprio inbox quando ativar
   Ex: TioGu lê dialogos/inbox-tiogu/ no início de conversa

4. Destino processa a demanda. Após terminar:
   a. Atualiza frontmatter: status: concluido, processado_em, processado_por
   b. Adiciona seção `## Resultado` no corpo descrevendo o que foi feito
      (commit hash, memory_id, link, decisão tomada — qualquer coisa rastreável)
   c. NÃO precisa mover o arquivo — o workflow archive-completed-demandas.yml
      faz isso automaticamente em até 15min

5. Workflow `archive-completed-demandas.yml` (cron 15min) pega arquivos
   com status: concluido (ou cancelado) e:
   - Move pra dialogos/archive/<filename>
   - Trash arquivo no Drive em Gus-Sync/dialogos/inbox-<X>/<filename>
     (impede reimport pelo import-from-drive)
   - Append linha em dialogos/historico/<AAAA-MM>.md (mensal)
```

## Frontmatter padrão (obrigatório)

```yaml
---
tipo: demanda
origem: claude-chat | tiogu | claude-code | custom-gpt | gustavo
destino: tiogu | claude-code | claude-chat | custom-gpt
prioridade: alta | media | baixa
status: pendente | processando | concluido
criado_em: 2026-04-25T23:50:00-03:00
processado_em: ""
processado_por: ""
---

# Título curto da demanda

Corpo descritivo: o que precisa ser feito, contexto, critério de sucesso.

## Resultado (preenche depois de processar)
[O destino preenche aqui o que fez + memory_id, commit hash, etc. pra rastreabilidade]
```

## Regras de validação (workflow rejeita se quebrar)

- Frontmatter precisa ser YAML válido entre `---`
- Campos obrigatórios: `tipo`, `origem`, `destino`, `prioridade`, `status`, `criado_em`
- `tipo` precisa ser `demanda`
- `origem` precisa ser uma das portas conhecidas
- `destino` precisa ser uma das portas conhecidas (não pode ser igual à origem)
- `status` no momento do create deve ser `pendente`

Se qualquer regra quebrar:
- Workflow loga erro
- Arquivo NÃO é importado pro GitHub
- Arquivo permanece no Drive (pra Gustavo ver e corrigir)
- Próxima execução tenta de novo (idempotente)

## Convenção de nome de arquivo

```
<timestamp>__<descricao-curta>.md
```

Ex: `2026-04-25T23-50__salvar-mem0-cleir.md`

Timestamp formato `AAAA-MM-DDTHH-MM` (BRT) facilita ordenação cronológica e evita
colisão entre demandas geradas em sessões paralelas.

## Quem pode escrever onde

| Origem (escreve em) | inbox-tiogu | inbox-claude-code | inbox-claude-chat | inbox-custom-gpt |
|---|:---:|:---:|:---:|:---:|
| Claude Chat (Drive) | ✅ | ✅ | ✅ | ✅ |
| Claude Code (commit direto) | ✅ | (auto) | ✅ | ✅ |
| TioGu Telegram (save_to_github) | (auto) | ✅ | ✅ | ✅ |
| Custom GPT (API REST) | ✅ | ✅ | ✅ | (auto) |
| Gustavo (manual no Obsidian/repo) | ✅ | ✅ | ✅ | ✅ |

`(auto)` = a porta destino é a mesma da origem, faz mais sentido executar direto que enfileirar pra si mesma.

## Quem lê o quê (e quando)

- **TioGu Telegram:** cron 5min varre `inbox-tiogu/` pegando `prioridade: alta` pra notificar (não-implementado V1, manual por enquanto)
- **Claude Code (sessão Web):** SessionStart hook lê `inbox-claude-code/` no início de cada sessão (a implementar)
- **Claude Chat:** lê `inbox-claude-chat/` quando bootstrap pede; ou Gustavo aponta na conversa
- **Custom GPT:** lê `inbox-custom-gpt/` quando Gustavo pedir explicitamente (não tem cron)

Hoje (V1, 25/04): leitura é **manual** — cada porta confere o seu inbox quando o Gustavo lembrar de pedir. Auto-leitura é Nível 3 (futuro).

## Notificação Telegram

Quando workflow `import-from-drive.yml` importar uma demanda em `inbox-tiogu/`,
manda mensagem no Telegram chat do Gustavo:

```
📥 Demanda nova em inbox-tiogu
Origem: claude-chat | Prioridade: alta
"<título>"
```

Implementado se `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` estiverem como secrets do
GitHub (precisa o Gustavo adicionar). Sem isso, import funciona mas sem notificação.

## Histórico (legado)

A pasta `streams/` mantém o formato antigo (arquivo único cronológico por semana,
nomeado pela segunda-feira). Foi o protocolo entre 24/04 e 25/04 noite. Continua
sendo onde Claude Code registra fim de sessão por convenção, mas pode evoluir
pra subpasta de `archive/` no futuro.

## Documentos relacionados

- `dialogos/_bootstrap/gus-bootstrap.md` — ativador de identidade Gus pro Claude Chat (read-only por convenção, não editar via Drive)
- `dialogos/_bootstrap/gus-identity.md` — identidade compartilhada entre todas as portas
- `projetos/gus/gus-13-tags-canonicas.md` — tags `via` no Mem0 (mesma taxonomia de portas)
- `projetos/gus/gus-12-portas-futuras.md` — diretriz arquitetural de portas
- `projetos/gus/gus-16-canal-unificado.md` — design rationale desta arquitetura (a criar)
