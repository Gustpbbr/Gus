"""
NeuroGus — wrapper Python que serve o HTML do grafo 3D do Hub Qdrant.

Difere do padrão dashboard.py/camera.py: HTML mora em arquivo separado
(api/neurogus.html, ~2300 LoC) em vez de string Python embarcada. Razão:
arquivo grande, ganha syntax highlighting / lint / diff legível como HTML.

Servido por api/server.py em GET /neurogus (HTML) e
GET /neurogus/manifest.json (PWA install).

Decisões (gus-30.1):
- HTML lido uma vez no module load (não bytes na cada request)
- MANIFEST mínimo na Parte 1A; Parte 3 completa com ícones SVG inline
- Auth: Parte 1A serve sem auth (mock estático); Parte 1B adiciona
  validação de ?token= antes de retornar (ou serve 401)

Origem: mock HTML de 28/04/2026 da Claude Chat, refatorado por
Claude Code 2026-05-02 com 5 modificações cirúrgicas (Parte 1A.1):
- 14 tipos canônicos do schema gus-18 (era 8)
- 9 áreas + cinza neutro fallback (era 7)
- getNodeColor() regra meio-termo (tipo se ≠ episodico, fallback area)
- Loop REAL_NODES.forEach usa getNodeColor()
- Meta theme-color #050514
"""

import os

# Manifest mínimo (Parte 3 completa com ícones SVG inline)
MANIFEST = {
    "name": "NeuroGus",
    "short_name": "NeuroGus",
    "description": "Memória viva do Gus — grafo 3D em tempo real",
    "start_url": "/neurogus",
    "display": "standalone",
    "orientation": "any",
    "theme_color": "#050514",
    "background_color": "#050514",
}

# Lê o HTML uma vez no module load — cached pra todas as requests
_HTML_PATH = os.path.join(os.path.dirname(__file__), "neurogus.html")
with open(_HTML_PATH, encoding="utf-8") as _f:
    NEUROGUS_HTML = _f.read()
