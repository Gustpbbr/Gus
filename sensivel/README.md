---
tipo: pasta-regras
privacidade: alta
sync_drive: excluida
atualizado: 2026-04-24
---

# sensivel/ — dados que não espelham pro Google Drive

Esta pasta existe para isolar conteúdo que **não deve** ser espelhado no Google Drive, mas ainda precisa ser versionado no GitHub e acessível pelo Gus.

## O que vai aqui

- CPF, CNPJ, RG em qualquer contexto
- Número de cartão de crédito ou débito (mesmo se só últimos 4 dígitos)
- Senhas, API keys, tokens de acesso
- Contatos com telefone ou email de terceiros (não é pra compartilhar)
- Qualquer dado bancário (conta, agência, chave Pix, boleto)
- Documentos de identidade digitalizados

## Como funciona a proteção

O workflow `sync-to-drive.yml` exclui o prefixo `sensivel/` — nada aqui entra no Drive. Só fica no GitHub privado do Gustavo.

O bot do Telegram faz **scan automático** antes de salvar qualquer `.md`. Se detectar CPF, cartão, API key, etc., ele **sugere salvar aqui em vez da pasta original**. O Gustavo confirma ou redireciona.

## Regras de sub-estrutura

Dentro de `sensivel/`, organiza por categoria:

- `sensivel/identidade/` — CPF, RG, passaporte
- `sensivel/financeiro/` — contas, cartões, chave Pix
- `sensivel/contatos/` — pessoas com dados privados (telefone de mãe, email de cliente, etc.)
- `sensivel/credenciais/` — senhas, API keys que o Gus precisa lembrar
- `sensivel/documentos/` — fotos de RG, CNH, comprovantes

Um MD por item (não um MD gigante com tudo). Nomenclatura normal (sem acentos, hífen, extensão `.md`).
