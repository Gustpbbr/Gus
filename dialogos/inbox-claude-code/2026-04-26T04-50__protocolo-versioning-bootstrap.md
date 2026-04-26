---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: baixa
status: pendente
criado_em: 2026-04-26T04:50:00-03:00
---

# Adicionar protocolo de versionamento ao gus-bootstrap.md

## Contexto

Descobrimos nesta sessão que Claude Chat não tem PATCH nativo no Drive -- toda "edição" é na pratica um novo upload, gerando duplicatas com mesmo nome.

Solução definida: usar sufixo de versão (-v2, -v3...) em toda reedição de arquivo por Claude Chat.

## Tarefa

Adicionar a seguinte seção ao `gus/gus-bootstrap.md` no repo `Gustpbbr/Gus`:

```markdown
## Protocolo de edição de arquivos no Drive (Claude Chat)

Claude Chat não tem PATCH nativo no Drive -- toda "edição" é um novo upload.
Convenção obrigatória: ao reeditar um arquivo existente, usar sufixo de versão:

  exemplo.md → exemplo-v2.md → exemplo-v3.md ...

Procedimento:
1. Ler conteúdo do arquivo original via Drive
2. Modificar no container Linux
3. Uploar com sufixo `-vX` no nome
4O arquivo anterior NÃO!o` é apagado automaticamente -- Gustavo decide o que manter
```

## Observação

Isso deve entrar também no protocolo de documentação de capacidades de cada porta (arquivos `portas/capacidades-*.porta*.md`).

Já existe o arquivo `Gus-Sync/gus/portas/capacidades-claude-chat.md` (criado nesta sessão) com referência a esta limitação -- mas a regra de versionamento precisa estar no bootstrap para ser carregada em todas as sessões.

-- Claude Chat | via=claude-chat | 26/04/2026