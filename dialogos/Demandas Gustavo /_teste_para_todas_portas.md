# Inbox — Claude Chat

Marcadores ou demandas pra **próxima sessão Claude Chat** (claude.ai) ler.

## Caso de uso típico

Como Claude Chat **não tem memória entre sessões** (cada aba é nova),
demandas aqui servem como "mensagens pra mim mesmo no futuro":

- Continuação de análise iniciada antes
- Lembrete de contexto que precisa ser carregado
- Decisão pendente que precisa retomar

## Quem escreve

- **Claude Chat** mesmo (auto-mensagem cross-sessão)
- **TioGu/Claude Code/Gustavo** quando quer que próxima sessão Claude Chat
  já comece com contexto específico

## Quem lê

- **Claude Chat** quando Gustavo apontar no bootstrap ou pedir explicitamente
  ("lê inbox-claude-chat antes de continuar")

## Frontmatter

Ver `dialogos/README.md`. Pode ter `prioridade: media` ou `baixa` — alta não
faz tanto sentido aqui (Claude Chat não monitora ativamente).

## Após processar

1. `status: concluido`, `processado_em`, `processado_por: claude-chat`
2. Mover pra `archive/`
