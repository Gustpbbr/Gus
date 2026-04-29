---
tipo: demanda
origem: claude-code
destino: claude-chat
prioridade: media
status: concluido
criado_em: 2026-04-26T01:00:00-03:00
processado_em: 2026-04-29T12:15:00-03:00
processado_por: claude-code
---

# Renderizar site da arquitetura do Gus pro Gustavo visualizar

## Contexto

TioGu pediu (via `dialogos/inbox-claude-code/2026-04-26T00-43__site-arquitetura-projeto.md`, agora arquivado) que Claude Code criasse um site HTML resumindo a arquitetura do projeto Gus.

Como Gustavo está em ambiente sem como abrir HTML local, o handoff é contigo: tu rendereiza o HTML abaixo como **Artifact** dentro do chat com ele, ele vê direto no claude.ai.

## Ação

1. Cria um Artifact `text/html` no chat com Gustavo usando exatamente o HTML da seção abaixo.
2. Confirma com ele que a renderização ficou ok.
3. Se ele pedir, salva uma cópia em `Gus-Sync/site-arquitetura/index.html` no Drive.

## Critério de sucesso

- Artifact aberto no claude.ai mostrando o site
- Gustavo conseguiu visualizar
- Atualizar frontmatter desta demanda pra `status: concluido`, preencher `processado_em`/`processado_por: claude-chat` e mover pra `dialogos/archive/`

## HTML a renderizar

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gus — arquitetura</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
      max-width: 760px;
      margin: 0 auto;
      padding: 48px 24px;
      color: #1a1a1a;
      background: #fafafa;
    }
    h1 { font-size: 28px; margin: 0 0 4px; font-weight: 600; letter-spacing: -0.01em; }
    h2 { font-size: 18px; margin: 36px 0 12px; font-weight: 600; color: #2c3e50; border-bottom: 1px solid #e1e4e8; padding-bottom: 6px; }
    p { margin: 12px 0; }
    .lead { color: #555; font-size: 15px; margin: 0 0 24px; }
    code, pre { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 13px; }
    pre { background: #f1f3f5; padding: 12px 16px; border-radius: 4px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 12px 0; }
    th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid #e1e4e8; vertical-align: top; }
    th { font-weight: 600; color: #555; font-size: 13px; }
    .tag { display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 3px; font-family: ui-monospace, monospace; }
    .tag-on { background: #d1f5e0; color: #1d6b3a; }
    .tag-wip { background: #fff3cd; color: #7c5b00; }
    .tag-future { background: #e9ecef; color: #555; }
    ul { margin: 12px 0; padding-left: 24px; }
    li { margin: 4px 0; }
    .meta { color: #888; font-size: 12px; margin-top: 48px; border-top: 1px solid #e1e4e8; padding-top: 12px; }
    svg { display: block; margin: 16px auto; max-width: 100%; }
  </style>
</head>
<body>

  <h1>Gus — arquitetura</h1>
  <p class="lead">Resumo visual do agente pessoal multi-porta do Gustavo Pratti.</p>

  <h2>O que é</h2>
  <p>
    Gus é um sistema com identidade única acessada por múltiplas portas que compartilham a mesma memória, o mesmo arquivo e os mesmos princípios. O dono não programa: toda implementação acontece via conversa com LLMs e é commitada no GitHub.
  </p>

  <h2>Diagrama</h2>
  <svg viewBox="0 0 720 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagrama de arquitetura do Gus">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="#6c757d" />
      </marker>
    </defs>
    <style>
      .box { fill: white; stroke: #2c3e50; stroke-width: 1.4; }
      .box-shared { fill: #f1f3f5; stroke: #495057; stroke-width: 1.4; }
      .label { font: 12px ui-monospace, monospace; fill: #1a1a1a; }
      .label-small { font: 10px system-ui, sans-serif; fill: #6c757d; }
      .arrow { stroke: #6c757d; stroke-width: 1; fill: none; marker-end: url(#arrow); }
    </style>

    <rect class="box" x="20"  y="20" width="120" height="40" rx="3" />
    <text class="label" x="80"  y="44" text-anchor="middle">Telegram (TioGu)</text>
    <rect class="box" x="160" y="20" width="120" height="40" rx="3" />
    <text class="label" x="220" y="44" text-anchor="middle">Claude Code</text>
    <rect class="box" x="300" y="20" width="120" height="40" rx="3" />
    <text class="label" x="360" y="44" text-anchor="middle">Claude Chat</text>
    <rect class="box" x="440" y="20" width="120" height="40" rx="3" />
    <text class="label" x="500" y="44" text-anchor="middle">Custom GPT</text>
    <rect class="box" x="580" y="20" width="120" height="40" rx="3" />
    <text class="label" x="640" y="44" text-anchor="middle">Alexa (futuro)</text>

    <rect class="box-shared" x="40"  y="170" width="180" height="60" rx="4" />
    <text class="label" x="130" y="195" text-anchor="middle">Mem0 (brain)</text>
    <text class="label-small" x="130" y="212" text-anchor="middle">user_id="gustavo" / "gus"</text>

    <rect class="box-shared" x="270" y="170" width="180" height="60" rx="4" />
    <text class="label" x="360" y="195" text-anchor="middle">GitHub vault</text>
    <text class="label-small" x="360" y="212" text-anchor="middle">Gustpbbr/Gus (.md)</text>

    <rect class="box-shared" x="500" y="170" width="180" height="60" rx="4" />
    <text class="label" x="590" y="195" text-anchor="middle">Google Drive (mirror)</text>
    <text class="label-small" x="590" y="212" text-anchor="middle">sync via Actions</text>

    <rect class="box-shared" x="160" y="275" width="400" height="36" rx="4" />
    <text class="label" x="360" y="298" text-anchor="middle">dialogos/inbox-X/  — canal assíncrono entre portas</text>

    <path class="arrow" d="M 80 60 Q 80 110 130 170" />
    <path class="arrow" d="M 220 60 Q 220 110 360 170" />
    <path class="arrow" d="M 360 60 Q 360 110 590 170" />
    <path class="arrow" d="M 500 60 Q 500 110 360 170" />
    <path class="arrow" d="M 640 60 Q 640 110 590 170" />

    <path class="arrow" d="M 130 230 L 220 275" />
    <path class="arrow" d="M 360 230 L 360 275" />
    <path class="arrow" d="M 590 230 L 500 275" />
  </svg>

  <h2>Portas</h2>
  <table>
    <tr><th>Porta</th><th>Cérebro</th><th>Função</th><th>Status</th></tr>
    <tr><td>Telegram (TioGu)</td><td>Sonnet 4.6</td><td>Captura diária, foto, áudio, PDF</td><td><span class="tag tag-on">ativa</span></td></tr>
    <tr><td>Claude Code</td><td>Opus / Sonnet</td><td>Engenharia: edita, commita, mergeia</td><td><span class="tag tag-on">ativa</span></td></tr>
    <tr><td>Claude Chat</td><td>Claude (web)</td><td>Reflexão longa, leitura do Drive, Artifacts</td><td><span class="tag tag-on">ativa</span></td></tr>
    <tr><td>Custom GPT</td><td>GPT-5</td><td>Voz fluida no celular</td><td><span class="tag tag-wip">API pronta, falta Action</span></td></tr>
    <tr><td>Alexa</td><td>Sonnet / Haiku</td><td>Voz em casa, comandos curtos</td><td><span class="tag tag-future">futuro</span></td></tr>
  </table>

  <h2>Camadas compartilhadas</h2>
  <ul>
    <li><strong>Mem0</strong> — memória relacional. Brain <code>gustavo</code> (~164 mems) + brain <code>gus</code> (auto-observação). Toda escrita carrega <code>metadata.via=&lt;porta&gt;</code> pra rastreabilidade.</li>
    <li><strong>GitHub vault</strong> (<code>Gustpbbr/Gus</code>) — arquivos <code>.md</code> versionados. Pastas: <code>pessoal/</code>, <code>dimagem/</code>, <code>projetos/</code>, <code>capturado/</code>, <code>dialogos/</code> entre outras.</li>
    <li><strong>Google Drive</strong> — espelho dos <code>.md</code> como Google Docs (sync via GitHub Action). Permite ao Claude Chat ler tudo no app.</li>
    <li><strong>Identidade</strong> — <code>gus/gus-identity.md</code> e <code>gus/gus-bootstrap.md</code> carregados por todas as portas. Mesma persona, canais diferentes.</li>
  </ul>

  <h2>Componentes operacionais</h2>
  <ul>
    <li><strong>Railway</strong> — hospeda o bot Telegram e a API REST do Custom GPT no mesmo processo (<code>asyncio.gather(run_bot, run_api)</code>).</li>
    <li><strong>GitHub Actions</strong> — sync GitHub→Drive, import Drive→GitHub (canal <code>dialogos/</code>), check de saúde diário, exports de Mem0.</li>
    <li><strong>MCP servers locais</strong> — <code>.claude/mcp/mem0_server.py</code> e <code>gus_server.py</code> dão ao Claude Code 9 tools (Mem0, diagnóstico, wikilinks, GPT).</li>
    <li><strong>Hooks do Claude Code</strong> — <code>SessionStart</code> injeta contexto e lê inbox pendente; <code>PreToolUse</code> bloqueia escrita com PII fora de <code>sensivel/</code>.</li>
  </ul>

  <h2>Canal <code>dialogos/</code></h2>
  <p>
    Comunicação assíncrona entre as portas. Cada porta tem sua inbox; quando uma quer pedir algo de outra, deposita um <code>.md</code> com frontmatter padrão na inbox do destino. Workflow <code>import-from-drive.yml</code> (cron 15 min) puxa demandas que nasceram fora do GitHub.
  </p>
<pre>dialogos/
├── inbox-tiogu/
├── inbox-claude-code/
├── inbox-claude-chat/
├── inbox-custom-gpt/
├── archive/
└── streams/   (legado cronológico)</pre>

  <h2>Projetos ativos do Gustavo</h2>
  <ul>
    <li><strong>Phronesis-Bench</strong> — benchmark de metacognição e prudência epistêmica para LLMs.</li>
    <li><strong>MGE / MGX</strong> — pipeline multi-agente de geração criativa estruturada.</li>
    <li><strong>TER</strong> — framework filosófico-computacional de deliberação ética para IA.</li>
    <li><strong>Axon</strong> — governança contextual para famílias com crianças neurodivergentes.</li>
    <li><strong>Gus</strong> — este sistema. Infraestrutura pessoal que sustenta os outros.</li>
  </ul>

  <p class="meta">Snapshot 2026-04-26. Fontes: <code>gus/gus-identity.md</code>, <code>gus/gus-bootstrap.md</code>, <code>projetos/gus/gus-12-portas-futuras.md</code>, <code>projetos/gus/gus-16-canal-unificado.md</code>, <code>projetos/gus/_estado-atual.md</code>, <code>dialogos/README.md</code>.</p>

</body>
</html>
```

## Resultado

[Claude Chat preenche aqui após processar]
