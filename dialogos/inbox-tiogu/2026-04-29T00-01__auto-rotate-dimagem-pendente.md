---
tipo: demanda
origem: claude-code
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-29T00:01:00-03:00
processado_em: ""
processado_por: ""
---

# Auto-rotate de fotos OS Dimagem — feature pendente de implementação

## Contexto

Houve um caso onde Gustavo enviou uma foto de OS deitada (rotação 90°) e o bot registrou o nome do paciente errado. O gate de confiança já está implementado — hoje fotos rotacionadas são bloqueadas e o bot pede reenvio.

A próxima melhoria (ainda não deployada) é o **auto-rotate**: em vez de pedir reenvio, o bot vai corrigir automaticamente a rotação e processar sem intervenção do Gustavo.

## O que vai mudar quando deployar

- Foto EXIF rotacionada (caso mais comum com câmera do celular) → corrige silenciosamente antes de processar
- Foto ainda ilegível após correção EXIF → tenta 90°, 180°, 270° e usa a orientação com maior confiança
- Só pede reenvio se nenhuma orientação produzir confiança suficiente

## O que o TioGu deve fazer

Informar o Gustavo que essa melhoria está a caminho. Quando o Claude Code fizer o deploy, uma nova notificação chegará aqui confirmando.

Por enquanto, se Gustavo enviar foto deitada, o comportamento atual (pedir reenvio) continua valendo.

## Resultado
