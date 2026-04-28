# capturado/

Captura rápida — coisas sem lar definido. Caixa de entrada do agente.

## Estrutura

| Subpasta | Pra que |
|---|---|
| **`links/`** | Artigos, posts, vídeos salvos da web. Cada link em `<titulo-curto>.md` com URL + resumo + tags. |
| **`ideias/`** | Insights soltos, brainstorms, ideias de projeto que ainda não viraram um. Cada ideia em `<tema>.md`. |
| **`misc/`** | Tudo que não cabe em links/ideias/visual. Não usar como dump preguiçoso — se aparecer padrão, criar subpasta. |
| **`visual/`** | Capturas visuais (placeholder pro projeto S8 câmera + IP Webcam, futuro). |

## Regras

- Nome de arquivo curto e descritivo (`romeu-julieta-cremoso.md`,
  não `coisa-do-dia-3.md`)
- Frontmatter automático no save: `capturado_em`, `via`
- Quando algo em `capturado/` cresce (ex: 5+ ideias sobre Phronesis), migrar pra
  pasta dedicada do projeto (`projetos/phronesis-bench/`)

## Diferença pra `_indices/`

- **`capturado/`**: conteúdo bruto, raw input
- **`_indices/`**: dashboards consolidados, gerados automaticamente

## Quando o bot salva aqui

Se Gustavo manda algo sem contexto claro de área (saúde, finanças,
projeto específico, dimagem), bot salva em `capturado/<categoria>/`
e oferece sugestão de pasta mais específica em mensagem de retorno.
