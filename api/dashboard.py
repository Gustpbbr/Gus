"""
Dashboard visual do Gus — grafo de memórias + saúde do sistema.

Acessível em /dashboard?token=SEU_TOKEN
Os endpoints de dados (/graph-data, /health-data) exigem Bearer token.
"""

import asyncio
import os
import time

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

COLLECTION = "gus"


# ---------------------------------------------------------------------------
# Dados
# ---------------------------------------------------------------------------


def _qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )


async def fetch_graph_data() -> dict:
    def _run():
        client = _qdrant_client()
        nodes = []
        offset = None
        while True:
            results, next_offset = client.scroll(
                collection_name=COLLECTION,
                limit=250,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            for pt in results:
                p = pt.payload or {}
                nodes.append({
                    "id": str(pt.id),
                    "memory": p.get("data", ""),
                    "user_id": p.get("user_id", "unknown"),
                    "created_at": p.get("created_at", ""),
                    "via": (p.get("metadata") or {}).get("via", ""),
                })
            if next_offset is None:
                break
            offset = next_offset
        return nodes

    nodes = await asyncio.to_thread(_run)
    gustavo = sum(1 for n in nodes if n["user_id"] == "gustavo")
    gus = sum(1 for n in nodes if n["user_id"] == "gus")
    return {"nodes": nodes, "gustavo_count": gustavo, "gus_count": gus}


async def fetch_health_data() -> dict:
    def _run():
        t0 = time.time()
        try:
            client = _qdrant_client()
            client.get_collection(COLLECTION)
            latency = int((time.time() - t0) * 1000)

            def _count(uid):
                return client.count(
                    COLLECTION,
                    count_filter=Filter(must=[
                        FieldCondition(key="user_id", match=MatchValue(value=uid))
                    ]),
                ).count

            g_count = _count("gustavo")
            gus_count = _count("gus")

            # última memória por created_at
            last = None
            _, _ = client.scroll  # just checking it's available
            pts, _ = client.scroll(
                collection_name=COLLECTION,
                limit=1,
                with_payload=True,
                with_vectors=False,
                order_by="created_at",
            ) if False else ([], None)

            # fallback: scroll all and find max (collection small)
            offset2 = None
            while True:
                pts2, nxt2 = client.scroll(
                    collection_name=COLLECTION,
                    limit=250,
                    offset=offset2,
                    with_payload=True,
                    with_vectors=False,
                )
                for pt in pts2:
                    ca = (pt.payload or {}).get("created_at")
                    if ca and (last is None or ca > last):
                        last = ca
                if nxt2 is None:
                    break
                offset2 = nxt2

            return {
                "qdrant": {"status": "ok", "latency_ms": latency},
                "counts": {"gustavo": g_count, "gus": gus_count},
                "last_memory": last,
            }
        except Exception as e:
            return {
                "qdrant": {"status": "error", "error": str(e)},
                "counts": {"gustavo": 0, "gus": 0},
                "last_memory": None,
            }

    result = await asyncio.to_thread(_run)

    # Railway ping
    api_url = os.getenv("API_PUBLIC_URL", "")
    if api_url:
        try:
            import httpx
            async with httpx.AsyncClient() as hc:
                r = await hc.get(f"{api_url}/health", timeout=4)
                result["railway"] = {"ok": r.status_code == 200}
        except Exception:
            result["railway"] = {"ok": False}
    else:
        result["railway"] = {"ok": None}

    return result


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gus — Cérebro</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family:'Inter',sans-serif;
  background:#030712;
  color:#f1f5f9;
  height:100vh;
  overflow:hidden;
  display:flex;
  flex-direction:column;
}
header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 24px;
  background:rgba(15,23,42,0.9);
  backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(255,255,255,0.06);
  z-index:10;
  flex-shrink:0;
}
.logo { font-size:17px; font-weight:600; letter-spacing:-0.4px; }
.logo span { color:#06b6d4; }
.tabs {
  display:flex;
  gap:4px;
  background:rgba(255,255,255,0.05);
  padding:4px;
  border-radius:8px;
}
.tab {
  padding:6px 18px;
  border-radius:6px;
  cursor:pointer;
  font-size:13px;
  font-weight:500;
  border:none;
  background:transparent;
  color:#64748b;
  transition:all 0.2s;
}
.tab.active { background:rgba(6,182,212,0.12); color:#06b6d4; }
.header-stats { font-size:12px; color:#334155; }
main { flex:1; position:relative; overflow:hidden; }

/* ── Graph ── */
#graph-view { width:100%; height:100%; position:absolute; top:0; left:0; }
#graph-svg { width:100%; height:100%; }
.node circle {
  cursor:pointer;
  transition:r 0.15s;
}
.node circle:hover { stroke-width:3 !important; }
#tooltip {
  position:fixed;
  background:rgba(15,23,42,0.96);
  border:1px solid rgba(255,255,255,0.09);
  border-radius:8px;
  padding:10px 14px;
  font-size:12px;
  line-height:1.6;
  max-width:260px;
  pointer-events:none;
  display:none;
  z-index:200;
  color:#cbd5e1;
}
#sidebar {
  position:absolute;
  right:0; top:0;
  width:340px;
  height:100%;
  background:rgba(10,18,38,0.98);
  border-left:1px solid rgba(255,255,255,0.07);
  padding:28px 24px 24px;
  transform:translateX(100%);
  transition:transform 0.28s ease;
  overflow-y:auto;
  z-index:30;
}
#sidebar.open { transform:translateX(0); }
#sb-close {
  position:absolute; top:14px; right:14px;
  background:none; border:none;
  color:#475569; cursor:pointer; font-size:16px;
}
#sb-close:hover { color:#94a3b8; }
#sb-brain {
  font-size:10px; font-weight:700;
  text-transform:uppercase; letter-spacing:1px;
  margin-bottom:10px;
}
#sb-text {
  font-size:14px; line-height:1.75;
  color:#cbd5e1; margin-bottom:20px;
}
#sb-meta {
  font-size:11px; color:#334155;
  border-top:1px solid rgba(255,255,255,0.06);
  padding-top:14px; line-height:2;
}
#legend {
  position:absolute;
  bottom:20px; left:20px;
  display:flex; gap:16px;
  background:rgba(10,18,38,0.82);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:8px;
  padding:8px 16px;
  font-size:12px; color:#64748b;
}
.ldot {
  width:9px; height:9px; border-radius:50%;
  display:inline-block; margin-right:6px; vertical-align:middle;
}
#controls {
  position:absolute;
  top:16px; left:16px;
  display:flex; gap:8px;
  z-index:20;
}
.ctrl-btn {
  background:rgba(15,23,42,0.85);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:6px;
  color:#64748b;
  font-size:12px;
  padding:5px 12px;
  cursor:pointer;
  font-family:inherit;
  transition:all 0.2s;
}
.ctrl-btn:hover { color:#cbd5e1; border-color:rgba(255,255,255,0.18); }
.ctrl-btn.active { color:#06b6d4; border-color:rgba(6,182,212,0.3); }

/* ── Health ── */
#health-view {
  display:none;
  padding:40px 32px;
  overflow-y:auto;
  height:100%;
}
.health-title {
  font-size:14px; color:#475569;
  margin-bottom:24px; font-weight:500;
}
.health-grid {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
  gap:14px;
  max-width:900px;
}
.hcard {
  background:rgba(15,23,42,0.7);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:12px;
  padding:20px;
  transition:border-color 0.2s;
}
.hcard:hover { border-color:rgba(255,255,255,0.12); }
.hcard-top {
  display:flex; align-items:center;
  justify-content:space-between;
  margin-bottom:14px;
}
.hlabel {
  font-size:11px; font-weight:600;
  text-transform:uppercase; letter-spacing:0.7px;
  color:#475569;
}
.sdot {
  width:8px; height:8px; border-radius:50%;
}
.ok  { background:#22c55e; box-shadow:0 0 7px #22c55e66; }
.warn{ background:#f59e0b; box-shadow:0 0 7px #f59e0b66; }
.err { background:#ef4444; box-shadow:0 0 7px #ef444466; }
.na  { background:#334155; }
.hval {
  font-size:26px; font-weight:600;
  margin-bottom:4px; color:#f1f5f9;
}
.hval.dim { color:#334155; }
.hsub { font-size:11px; color:#334155; }

/* ── Loading ── */
#loading {
  position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%);
  text-align:center; color:#334155;
}
.spin {
  width:30px; height:30px;
  border:2px solid rgba(6,182,212,0.15);
  border-top-color:#06b6d4;
  border-radius:50%;
  animation:rot 0.75s linear infinite;
  margin:0 auto 14px;
}
@keyframes rot { to { transform:rotate(360deg); } }
</style>
</head>
<body>
<header>
  <div class="logo">G<span>u</span>s &mdash; Cérebro</div>
  <div class="tabs">
    <button class="tab active" onclick="showTab('graph')">Grafo</button>
    <button class="tab" onclick="showTab('health')">Saúde</button>
  </div>
  <div class="header-stats" id="hstats">&nbsp;</div>
</header>

<main>
  <div id="graph-view">
    <div id="loading"><div class="spin"></div>carregando memórias...</div>
    <div id="controls">
      <button class="ctrl-btn active" onclick="filterBrain('all',this)">Todos</button>
      <button class="ctrl-btn" onclick="filterBrain('gustavo',this)">Gustavo</button>
      <button class="ctrl-btn" onclick="filterBrain('gus',this)">Gus</button>
    </div>
    <svg id="graph-svg"></svg>
    <div id="legend">
      <span><span class="ldot" style="background:#06b6d4"></span>Gustavo</span>
      <span><span class="ldot" style="background:#8b5cf6"></span>Gus (auto)</span>
    </div>
    <div id="sidebar">
      <button id="sb-close" onclick="closeSidebar()">&#x2715;</button>
      <div id="sb-brain"></div>
      <div id="sb-text"></div>
      <div id="sb-meta"></div>
    </div>
  </div>

  <div id="health-view">
    <div class="health-title">Status do sistema &mdash; atualizado agora</div>
    <div class="health-grid" id="hgrid">
      <div style="color:#334155;grid-column:1/-1;padding:20px 0">carregando...</div>
    </div>
  </div>
</main>

<div id="tooltip"></div>

<script>
// ── Auth ──────────────────────────────────────────────────────────
const params = new URLSearchParams(location.search);
const TOKEN = params.get('token') || localStorage.getItem('gus_token') || '';
if (TOKEN) localStorage.setItem('gus_token', TOKEN);
const HEADERS = TOKEN ? { 'Authorization': 'Bearer ' + TOKEN } : {};

// ── Colors ───────────────────────────────────────────────────────
const C = { gustavo: '#06b6d4', gus: '#8b5cf6', unknown: '#475569' };

// ── Tab ──────────────────────────────────────────────────────────
function showTab(tab) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    t.classList.toggle('active', ['graph','health'][i] === tab);
  });
  document.getElementById('graph-view').style.display = tab === 'graph' ? 'block' : 'none';
  document.getElementById('health-view').style.display = tab === 'health' ? 'block' : 'none';
  if (tab === 'health' && !window._healthLoaded) loadHealth();
}

// ── Sidebar ───────────────────────────────────────────────────────
function openSidebar(d) {
  const brain = d.user_id || 'unknown';
  const el = document.getElementById('sidebar');
  document.getElementById('sb-brain').textContent = brain.toUpperCase();
  document.getElementById('sb-brain').style.color = C[brain] || C.unknown;
  document.getElementById('sb-text').textContent = d.memory || '—';
  const lines = [];
  if (d.created_at) lines.push('Criado: ' + new Date(d.created_at).toLocaleString('pt-BR'));
  if (d.via) lines.push('Via: ' + d.via);
  document.getElementById('sb-meta').textContent = lines.join('  ·  ');
  el.classList.add('open');
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
}

// ── Filter ────────────────────────────────────────────────────────
let _allNodes = [];
let _currentFilter = 'all';
function filterBrain(brain, btn) {
  _currentFilter = brain;
  document.querySelectorAll('.ctrl-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateNodeVisibility();
}
function updateNodeVisibility() {
  if (!_sim) return;
  d3.selectAll('.node')
    .style('opacity', d => _currentFilter === 'all' || d.user_id === _currentFilter ? 1 : 0.08);
}

// ── Graph ─────────────────────────────────────────────────────────
let _sim = null;

async function loadGraph() {
  try {
    const r = await fetch('/graph-data', { headers: HEADERS });
    if (!r.ok) throw new Error('HTTP ' + r.status + ' — verifique o token (?token=...)');
    const data = await r.json();
    document.getElementById('loading').style.display = 'none';
    _allNodes = data.nodes || [];

    const g = data.gustavo_count || 0, gus = data.gus_count || 0;
    document.getElementById('hstats').textContent =
      (g + gus) + ' memórias · ' + g + ' Gustavo · ' + gus + ' Gus';

    renderGraph(_allNodes);
  } catch(e) {
    document.getElementById('loading').innerHTML =
      '<div style="color:#ef4444;font-size:13px">' + e.message + '</div>';
  }
}

function renderGraph(nodes) {
  const svg = d3.select('#graph-svg');
  svg.selectAll('*').remove();
  const W = svg.node().clientWidth, H = svg.node().clientHeight;

  // Glow filters
  const defs = svg.append('defs');
  ['gustavo','gus','unknown'].forEach(k => {
    const f = defs.append('filter').attr('id','glow-'+k).attr('x','-50%').attr('y','-50%').attr('width','200%').attr('height','200%');
    f.append('feGaussianBlur').attr('in','SourceGraphic').attr('stdDeviation','4').attr('result','blur');
    const m = f.append('feMerge');
    m.append('feMergeNode').attr('in','blur');
    m.append('feMergeNode').attr('in','SourceGraphic');
  });

  const g = svg.append('g');

  svg.call(d3.zoom().scaleExtent([0.2,5]).on('zoom', ev => g.attr('transform', ev.transform)));

  const r = d => Math.max(5, Math.min(20, Math.sqrt((d.memory||'').length / 2.5)));

  _sim = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(-70))
    .force('center', d3.forceCenter(W/2, H/2))
    .force('collision', d3.forceCollide().radius(d => r(d) + 10))
    .force('x', d3.forceX(d => d.user_id === 'gus' ? W*0.65 : W*0.35).strength(0.07))
    .force('y', d3.forceY(H/2).strength(0.03));

  const node = g.selectAll('.node')
    .data(nodes)
    .join('g')
    .attr('class','node')
    .call(d3.drag()
      .on('start', (e,d) => { if(!e.active) _sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
      .on('drag',  (e,d) => { d.fx=e.x; d.fy=e.y; })
      .on('end',   (e,d) => { if(!e.active) _sim.alphaTarget(0); d.fx=null; d.fy=null; }));

  node.append('circle')
    .attr('r', r)
    .attr('fill', d => (C[d.user_id]||C.unknown) + '22')
    .attr('stroke', d => C[d.user_id]||C.unknown)
    .attr('stroke-width', 1.5)
    .attr('stroke-opacity', 0.7)
    .attr('filter', d => 'url(#glow-'+(d.user_id||'unknown')+')')
    .on('mousemove', (ev,d) => {
      const t = document.getElementById('tooltip');
      t.style.display = 'block';
      t.style.left = (ev.clientX+16)+'px';
      t.style.top  = (ev.clientY-8)+'px';
      t.textContent = (d.memory||'').slice(0,130)+((d.memory||'').length>130?'…':'');
    })
    .on('mouseleave', () => { document.getElementById('tooltip').style.display='none'; })
    .on('click', (ev,d) => { ev.stopPropagation(); openSidebar(d); });

  svg.on('click', closeSidebar);

  _sim.on('tick', () => node.attr('transform', d => 'translate('+d.x+','+d.y+')'));
  updateNodeVisibility();
}

// ── Health ────────────────────────────────────────────────────────
async function loadHealth() {
  window._healthLoaded = true;
  try {
    const r = await fetch('/health-data', { headers: HEADERS });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    renderHealth(await r.json());
  } catch(e) {
    document.getElementById('hgrid').innerHTML =
      '<div style="color:#ef4444;grid-column:1/-1">'+e.message+'</div>';
  }
}

function sdot(cls) { return '<div class="sdot '+cls+'"></div>'; }

function renderHealth(d) {
  const last = d.last_memory ? new Date(d.last_memory).toLocaleString('pt-BR') : null;
  const qdOk = d.qdrant?.status === 'ok';
  const cards = [
    { label:'Qdrant',           ok: qdOk,
      val: qdOk ? 'Online' : 'Erro',
      sub: qdOk ? d.qdrant.latency_ms+'ms' : (d.qdrant?.error||'timeout') },
    { label:'Brain Gustavo',    ok: (d.counts?.gustavo||0)>0,
      val: d.counts?.gustavo ?? '—',
      sub: 'fragmentos de memória' },
    { label:'Brain Gus',        ok: (d.counts?.gus||0)>0,
      val: d.counts?.gus ?? '—',
      sub: 'autobiografia operacional' },
    { label:'Última memória',   ok: !!last,
      val: last ? last.split(',')[0] : '—',
      sub: last ? last.split(',')[1]?.trim() : 'nenhuma registrada' },
    { label:'Documentos Hub',   ok: d.hub_docs?.ok,
      val: d.hub_docs?.ok ? 'Completo' : 'Incompleto',
      sub: d.hub_docs?.missing?.length ? 'faltando: '+d.hub_docs.missing.join(', ') : 'gus-18 e gus-24 presentes' },
    { label:'Bot Railway',      ok: d.railway?.ok === true,
      val: d.railway?.ok === true ? 'Online' : d.railway?.ok === false ? 'Erro' : '—',
      sub: 'health endpoint' },
  ];
  document.getElementById('hgrid').innerHTML = cards.map(c => {
    const cls = c.ok === null || c.ok === undefined ? 'na' : c.ok ? 'ok' : 'err';
    return '<div class="hcard"><div class="hcard-top"><div class="hlabel">'+c.label+'</div>'+sdot(cls)+'</div>'
      + '<div class="hval'+(c.ok?'':' dim')+'">'+c.val+'</div>'
      + '<div class="hsub">'+c.sub+'</div></div>';
  }).join('');
}

// ── Init ──────────────────────────────────────────────────────────
loadGraph();
</script>
</body>
</html>"""
