---
tipo: demanda
origem: gustavo
destino: claude-chat
prioridade: media
status: pendente
criado_em: 2026-05-03T14:15:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: editar
destino_path: capturado/shakira-copa-2026/index.html
contexto: "HTML estrutural do show da Shakira em Copacabana criado por Claude Code (commit em main, 03/05/2026). Estética e conteúdo precisam ser finalizados — você tem web search nativo, use pra trazer info real."
---

# Finalizar HTML — Shakira em Copacabana

Claude Code criou a **estrutura V1** do site em `capturado/shakira-copa-2026/index.html`.
Ela tem layout, CSS, seções e placeholders marcados claramente. Sua tarefa:
**preencher conteúdo real e melhorar estética**.

## O que já está pronto (não precisa refazer)

- Layout responsivo mobile-first sem framework (HTML + CSS inline)
- 6 seções estruturadas: hero / info prática / sobre / setlist / FAQ / footer
- Cards de info com gradient placeholder (rosa+roxo, paleta Shakira-friendly)
- Accordion FAQ via `<details>/<summary>` nativo
- Comentários HTML em cada seção dizendo o que fazer

## O que falta (sua parte)

### 1. Pesquisa real via web search

**Confirme primeiro se o show existe.** Pode ser que ainda seja só rumor.
Se for rumor: ajusta tom de toda a página pra "aguardando confirmação"
e marca como tal no header.

Se confirmado, traz info real pra:

- **Data exata e horário**
- **Tour atual** (nome oficial, ex: "Las Mujeres Ya No Lloran World Tour")
- **Setlist** (pega de shows recentes via setlist.fm ou similar — 8-12 músicas)
- **Bio curta** com foco em momento atual da carreira (último álbum,
  conquistas 2025-2026, NÃO genérico tipo "uma das maiores artistas")
- **Ingressos** (gratuito como Madonna 2024? Pago? Plataforma?)
- **Capacidade estimada** (Madonna 2024 = 1.6 milhão na praia)
- **Horário ideal de chegada** (lições do Réveillon e Madonna)
- **Acesso de transporte público** (metrô: Cardeal Arcoverde, Siqueira Campos, Cantagalo)
- **Segurança e dicas práticas**

### 2. Estética — melhorar visual

Estrutura atual é funcional mas neutra. Você pode:

- **Trocar gradient placeholder** do hero por imagem real da Shakira
  (atribuição correta — usa Wikimedia Commons ou Shutterstock free se possível)
- **Adicionar fontes** customizadas (ex: Google Fonts com personalidade
  latino-pop — Bebas Neue pra títulos, Inter pra body)
- **Ajustar paleta** — atualmente rosa hot + roxo. Pode buscar paleta
  oficial do tour atual da Shakira (se houver branding)
- **Adicionar microanimações** (CSS only, nada de JS pesado): hover
  nos cards, fade-in das seções, etc.
- **Imagens em outras seções** — bio com foto, setlist com capa do álbum

### 3. Conteúdo extra (se inspiração)

- **Linha do tempo** rápida da Shakira (estreia, hits marcantes,
  Copacabana — se já tocou aqui antes, comparativo)
- **"O que esperar"** — vídeo de show recente embedado
- **Mapa interativo** com pontos de encontro / banheiros / postos médicos
  (depois que a Riotur publicar)

### 4. Validações finais

- HTML válido (https://validator.w3.org/)
- Acessibilidade: alt em imagens, contraste WCAG AA, navegação por teclado
- Open Graph + Twitter Card pra compartilhamento
- Favicon

## Como entregar

Como você (Claude Chat) **não tem PATCH no Drive**, segue protocolo `-vX`:

1. Lê `capturado/shakira-copa-2026/index.html` via MCP `read_repo_file` (preferível)
   ou Drive
2. Trabalha numa versão completa
3. Faz upload em **Drive** com nome `index-v2.html` na mesma pasta
4. Em até 15min cron `import-from-drive.yml` mirrora pro GitHub
5. Quando ficar bom, abre demanda pro `claude-code` renomear `index-v2.html` → `index.html`
   substituindo o original (workflow `delete-drive-file.yml` + commit no GitHub)

**Ou alternativa simples:** retorna o HTML completo aqui no chat e Gustavo cola pro Code substituir.

## Critério de pronto

- [ ] Confirmação se show existe (web search)
- [ ] Todos `[PLACEHOLDER]` removidos ou substituídos por info real
- [ ] Hero com imagem real (com atribuição) ou gradient mais elaborado
- [ ] Setlist real ou marcado claramente como "estimativa"
- [ ] FAQ com 5+ respostas reais
- [ ] Validado em mobile (DevTools responsive)

## Refs

- Demanda original: `dialogos/archive/2026-05-03-shakira-copa-html.md` (a ser arquivada)
- Arquivo a editar: `capturado/shakira-copa-2026/index.html`
- Versão estrutural V1 em `commit` de Code 03/05/2026 ~14:15 BRT

## Observação

Esse é o tipo de tarefa onde Caminho 2 (upload .md) faz menos sentido — você
tá editando HTML, não escrevendo memória. Se durante a pesquisa achar fato
relevante sobre Gustavo (ex: ele decidiu ir? gosta da Shakira?), aí sim usa
Caminho 1 (`ingestar_fragmento`) pra brain `gustavo`.
