---
tipo: documentacao-tecnica
atualizado: 2026-04-24
---

# Drive Inbox → GitHub — Setup

Sistema que permite ao Claude Projetos (e qualquer ferramenta com acesso ao Drive) salvar arquivos `.md` no GitHub automaticamente.

## Como funciona

```
Claude Projetos gera .md
    → você salva em Gus-Sync/Inbox/ no Drive (1 clique)
    → Apps Script detecta o arquivo (~5 min)
    → cria/atualiza o .md no GitHub via API
    → GitHub Action sincroniza de volta pro Drive na pasta correta
```

## Pré-requisitos

- Pasta `Gus-Sync/Inbox/` criada no Drive (criar manualmente)
- GitHub Personal Access Token (PAT) com permissão de escrita no repo Gus
- Conta Google (já tem — é a mesma do Drive)

## Passo 1 — GitHub PAT

1. `github.com` → clica no avatar (canto superior direito) → **Settings**
2. Scroll até o final → **Developer settings**
3. **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
4. Configurações:
   - Nome: `Gus Apps Script`
   - Expiração: 1 year (ou No expiration)
   - Repository access: **Only select repositories** → seleciona `Gus`
   - Permissions → Repository permissions → **Contents: Read and write**
5. **Generate token** → copia o token (aparece só uma vez)

## Passo 2 — Pasta Inbox no Drive

1. Abre o Google Drive
2. Navega até `Gus-Sync/`
3. Cria nova pasta: **+ Novo → Pasta** → nome `Inbox`
4. Abre a pasta `Inbox` → olha a URL do navegador
5. Copia o ID da URL: `drive.google.com/drive/folders/**ID_AQUI**`

## Passo 3 — Criar o Apps Script

1. Abre `script.google.com`
2. **Novo projeto**
3. Nome do projeto: `Gus Inbox Sync`
4. Apaga o código padrão (`function myFunction() {}`)
5. Cola o conteúdo completo de `.github/scripts/drive_inbox_to_github.gs`
6. Salva (Ctrl+S)

## Passo 4 — Configurar propriedades

1. No menu lateral esquerdo: **Configurações do projeto** (ícone de engrenagem)
2. **Propriedades do script** → **Adicionar propriedade**
3. Adiciona as duas:
   - `GITHUB_TOKEN` = o token do Passo 1
   - `INBOX_FOLDER_ID` = o ID do Drive do Passo 2
4. Salva

## Passo 5 — Autorizar e testar

1. No editor, seleciona a função `processInbox` no dropdown
2. Clica **Executar**
3. Aparece janela de autorização → **Revisar permissões** → escolhe a conta Google → **Permitir**
4. Verifica o log (menu **Execuções** ou View → Logs): deve mostrar `Concluído: 0 arquivo(s) processados`

## Passo 6 — Trigger automático

1. Menu lateral esquerdo: **Gatilhos** (ícone de relógio)
2. **+ Adicionar gatilho** (canto inferior direito)
3. Configurações:
   - Função: `processInbox`
   - Fonte de eventos: **Baseado em tempo**
   - Tipo: **Temporizador de minutos**
   - Intervalo: **A cada 5 minutos**
4. Salva

## Passo 7 — Testar o fluxo completo

1. Cria um arquivo `.md` com este frontmatter:
   ```
   ---
   github_path: capturado/misc/teste-inbox.md
   via: claude-projetos
   ---

   Conteúdo de teste.
   ```
2. Salva na pasta `Gus-Sync/Inbox/` no Drive
3. Aguarda até 5 minutos
4. Verifica no GitHub se `capturado/misc/teste-inbox.md` foi criado
5. O arquivo também aparece na pasta `Processado/` dentro de `Inbox/`

## Como o Claude Projetos deve formatar os arquivos

Nas instruções do projeto no Claude.ai, adiciona:

> Quando eu pedir pra salvar algo, gere o documento em markdown com este frontmatter:
> ```
> ---
> github_path: <pasta/nome-do-arquivo.md>
> via: claude-projetos
> atualizado: <data>
> ---
> ```
> Use os mesmos caminhos de pasta do repositório Gus:
> - Reflexões pessoais: `pessoal/diario/`
> - Saúde: `pessoal/saude/`
> - Projetos: `projetos/<nome>/`
> - Capturado/ideias: `capturado/ideias/`
> - Padrão se não souber: `capturado/misc/`

## Manutenção

- O PAT expira em 1 ano — renovar em `github.com → Settings → Developer settings`
- Arquivos processados ficam em `Inbox/Processado/` — pode limpar periodicamente
- Erros aparecem no log do Apps Script em `script.google.com → Execuções`
- Se o script parar de rodar: verificar em **Gatilhos** se o trigger ainda está ativo
