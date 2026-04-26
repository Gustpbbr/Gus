"""
Módulo de análise visual via câmera (S8 PWA).

Fluxo:
  1. PWA captura frame (JPEG base64) a cada 30s ou sob demanda
  2. POST /analise_camera → analisa com Claude Sonnet Vision
  3. Salva JPG + MD em capturado/visual/YYYY-MM-DD-HHMMSS.*
  4. Atualiza capturado/visual/_ultimo.md (sempre a captura mais recente)
  5. Custom GPT lê _ultimo.md via ver_ultima_captura tool
"""

import asyncio
import base64
import os
from datetime import datetime, timezone, timedelta

import anthropic
import httpx

BRT = timezone(timedelta(hours=-3))
VISUAL_FOLDER = "capturado/visual"
ULTIMO_PATH = "capturado/visual/_ultimo.md"
MODEL_VISION = "claude-sonnet-4-6"

PROMPT_ANALISE = """Analise esta imagem de forma objetiva e estruturada.

{contexto_extra}

Retorne em Markdown com exatamente estas seções:

## O que foi visto
(Descrição direta do que está na imagem, 2-4 frases)

## Detalhes identificados
- (lista de elementos específicos: objetos, textos, gestos, pessoas, ambiente)

## Texto visível
(Transcrição literal de qualquer texto na imagem. Se não houver: "Nenhum")

## Contexto inferido
(Situação provável, o que está acontecendo, ambiente)

## Confiança
(Alta / Média / Baixa — baseada na qualidade e clareza da imagem)

Seja direto e específico. Não faça suposições além do que está visível."""


async def analisar_imagem(image_base64: str, contexto: str = "") -> str:
    """Envia imagem pro Claude Sonnet Vision e retorna análise em Markdown."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "ANTHROPIC_API_KEY não configurado."

    contexto_extra = (
        f'Contexto fornecido pelo usuário: "{contexto}"' if contexto else ""
    )

    client = anthropic.AsyncAnthropic(api_key=api_key)
    try:
        response = await client.messages.create(
            model=os.getenv("MODEL_VISION", MODEL_VISION),
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": PROMPT_ANALISE.format(contexto_extra=contexto_extra),
                    },
                ],
            }],
        )
        return next((b.text for b in response.content if hasattr(b, "text")), "")
    except Exception as e:
        return f"Erro na análise visual: {e}"


async def _github_put(path: str, content_b64: str, commit_msg: str) -> bool:
    """PUT genérico no GitHub API. Retorna True se sucesso."""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    if not token:
        return False

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        sha = None
        check = await client.get(url, headers=headers)
        if check.status_code == 200:
            sha = check.json().get("sha")

        payload = {"message": commit_msg, "content": content_b64, "branch": "main"}
        if sha:
            payload["sha"] = sha

        response = await client.put(url, json=payload, headers=headers)

    return response.status_code in (200, 201)


async def salvar_captura(image_base64: str, analise_md: str, timestamp: str) -> dict:
    """Salva JPG + MD de análise + _ultimo.md no GitHub em paralelo."""
    now_str = datetime.now(BRT).strftime("%d/%m/%Y às %H:%M")

    img_path = f"{VISUAL_FOLDER}/{timestamp}.jpg"
    md_path = f"{VISUAL_FOLDER}/{timestamp}.md"

    md_content = (
        f"---\n"
        f"tipo: captura-visual\n"
        f"data: {timestamp}\n"
        f"via: camera-pwa\n"
        f"imagem: ./{timestamp}.jpg\n"
        f"---\n\n"
        f"# Captura visual — {now_str}\n\n"
        f"{analise_md}\n\n"
        f"---\n"
        f"*Foto: [{timestamp}.jpg](./{timestamp}.jpg)*\n"
    )

    ultimo_content = (
        f"---\n"
        f"tipo: ultima-captura-visual\n"
        f"captura: {timestamp}\n"
        f"atualizado: {datetime.now(BRT).isoformat()}\n"
        f"---\n\n"
        f"# Última captura visual\n\n"
        f"**Quando:** {now_str}  \n"
        f"**Arquivo completo:** `{md_path}`\n\n"
        f"---\n\n"
        f"{analise_md}\n"
    )

    md_b64 = base64.b64encode(md_content.encode()).decode()
    ultimo_b64 = base64.b64encode(ultimo_content.encode()).decode()

    ok_img, ok_md, ok_ultimo = await asyncio.gather(
        _github_put(img_path, image_base64, f"camera: foto {timestamp}"),
        _github_put(md_path, md_b64, f"camera: análise {timestamp}"),
        _github_put(ULTIMO_PATH, ultimo_b64, f"camera: _ultimo {timestamp}"),
    )

    return {
        "img_path": img_path if ok_img else None,
        "md_path": md_path if ok_md else None,
        "ultimo_ok": ok_ultimo,
    }


# HTML da PWA — servido em GET /camera (sem auth)
CAMERA_PWA_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0d1117">
<title>Gus — Câmera</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;height:100dvh;display:flex;flex-direction:column;overflow:hidden}
#preview{width:100%;flex:1;object-fit:cover;background:#161b22;display:block}
#panel{background:#161b22;border-top:1px solid #30363d;padding:14px;flex-shrink:0}
#status{font-size:13px;color:#8b949e;text-align:center;margin-bottom:10px;min-height:18px;transition:color .3s}
#status.active{color:#58a6ff}
#status.ok{color:#3fb950}
#status.err{color:#f85149}
#context{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#e6edf3;font-size:14px;padding:8px 12px;margin-bottom:10px;outline:none}
#context:focus{border-color:#58a6ff}
#context::placeholder{color:#484f58}
#buttons{display:flex;gap:10px;align-items:center;margin-bottom:10px}
#btn-capture{width:62px;height:62px;border-radius:50%;background:#fff;border:4px solid #58a6ff;cursor:pointer;flex-shrink:0;transition:transform .1s,background .15s;-webkit-appearance:none}
#btn-capture:active{transform:scale(.88);background:#58a6ff}
#btn-capture.busy{background:#58a6ff;animation:pulse 1s infinite}
#btn-auto{flex:1;padding:13px;border-radius:8px;border:1px solid #30363d;background:#21262d;color:#8b949e;font-size:14px;cursor:pointer;transition:all .2s}
#btn-auto.on{background:#1f6feb;border-color:#58a6ff;color:#fff}
#cd{font-size:26px;font-weight:700;color:#58a6ff;width:44px;text-align:center;flex-shrink:0;display:none}
#result{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:11px;font-size:12px;line-height:1.55;max-height:130px;overflow-y:auto;display:none}
#result h2{font-size:12px;color:#58a6ff;margin:7px 0 3px;font-weight:600}
#result h2:first-child{margin-top:0}
#ts-overlay{position:fixed;inset:0;background:#0d1117;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px;gap:16px;z-index:99}
#ts-overlay h1{font-size:22px;color:#58a6ff;letter-spacing:.5px}
#ts-overlay p{color:#8b949e;font-size:14px;text-align:center;line-height:1.5}
#ts-input{width:100%;background:#161b22;border:1px solid #30363d;border-radius:8px;color:#e6edf3;font-size:14px;padding:12px;outline:none;font-family:monospace}
#ts-input:focus{border-color:#58a6ff}
#ts-btn{width:100%;padding:14px;background:#1f6feb;border:none;border-radius:8px;color:#fff;font-size:15px;cursor:pointer;font-weight:600}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}
</style>
</head>
<body>

<div id="ts-overlay">
  <h1>Gus — Câmera</h1>
  <p>Cole o <strong>CUSTOM_GPT_TOKEN</strong> do Railway.<br>Salvo localmente, não sai do dispositivo.</p>
  <input type="password" id="ts-input" placeholder="Token..." autocomplete="off"/>
  <button id="ts-btn" onclick="saveToken()">Salvar e abrir câmera</button>
</div>

<video id="preview" autoplay muted playsinline></video>
<canvas id="canvas" style="display:none"></canvas>

<div id="panel">
  <div id="status">Iniciando câmera...</div>
  <input type="text" id="context" placeholder="Contexto opcional (ex: o que estou fazendo?)" autocomplete="off"/>
  <div id="buttons">
    <button id="btn-auto" onclick="toggleAuto()">⏱ Auto 30s</button>
    <div id="cd">30</div>
    <button id="btn-capture" onclick="captureNow()" title="Capturar"></button>
  </div>
  <div id="result"></div>
</div>

<script>
const API = window.location.origin;
let autoOn=false, autoTimer=null, cdTimer=null, cdVal=30, busy=false;

function tok(){return localStorage.getItem('gus_cam_token')||'';}
function saveToken(){
  const v=document.getElementById('ts-input').value.trim();
  if(!v)return;
  localStorage.setItem('gus_cam_token',v);
  document.getElementById('ts-overlay').style.display='none';
  initCam();
}
if(tok()){document.getElementById('ts-overlay').style.display='none';initCam();}

async function initCam(){
  try{
    const s=await navigator.mediaDevices.getUserMedia({
      video:{facingMode:'environment',width:{ideal:1280},height:{ideal:720}},audio:false
    });
    document.getElementById('preview').srcObject=s;
    st('Pronto para capturar','');
  }catch(e){st('Erro câmera: '+e.message,'err');}
}

async function captureNow(){
  if(busy)return;
  busy=true;
  const btn=document.getElementById('btn-capture');
  btn.classList.add('busy');
  st('Capturando...','active');
  try{
    const vid=document.getElementById('preview');
    const cv=document.getElementById('canvas');
    cv.width=vid.videoWidth||1280;
    cv.height=vid.videoHeight||720;
    cv.getContext('2d').drawImage(vid,0,0);
    const b64=cv.toDataURL('image/jpeg',.85).split(',')[1];
    const ctx=document.getElementById('context').value.trim();
    st('Analisando com Claude Vision...','active');
    const r=await fetch(API+'/analise_camera',{
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+tok()},
      body:JSON.stringify({image_base64:b64,contexto:ctx})
    });
    if(r.status===401||r.status===403){localStorage.removeItem('gus_cam_token');location.reload();return;}
    const d=await r.json();
    if(r.ok){st('✓ Salvo no GitHub','ok');showResult(d.result);}
    else{st('Erro: '+(d.detail||r.status),'err');}
  }catch(e){st('Erro: '+e.message,'err');}
  finally{busy=false;btn.classList.remove('busy');if(autoOn)resetCd();}
}

function toggleAuto(){
  autoOn=!autoOn;
  const btn=document.getElementById('btn-auto');
  const cd=document.getElementById('cd');
  if(autoOn){
    btn.classList.add('on');btn.textContent='⏱ Auto ON';cd.style.display='block';
    captureNow();
    autoTimer=setInterval(captureNow,30000);
    resetCd();
    cdTimer=setInterval(()=>{cdVal--;document.getElementById('cd').textContent=cdVal;if(cdVal<=0)resetCd();},1000);
  }else{
    btn.classList.remove('on');btn.textContent='⏱ Auto 30s';cd.style.display='none';
    clearInterval(autoTimer);clearInterval(cdTimer);autoTimer=null;cdTimer=null;
  }
}
function resetCd(){cdVal=30;document.getElementById('cd').textContent='30';}

function st(msg,cls){const e=document.getElementById('status');e.textContent=msg;e.className=cls;}

function showResult(txt){
  const el=document.getElementById('result');
  el.innerHTML=txt
    .replace(/^## (.+)$/gm,'<h2>$1</h2>')
    .replace(/^- (.+)$/gm,'<li style="margin-left:14px">$1</li>')
    .replace(/\n/g,'<br>');
  el.style.display='block';
}

// Impede tela apagar (Screen Wake Lock API)
if('wakeLock' in navigator){navigator.wakeLock.request('screen').catch(()=>{});}
</script>
</body>
</html>"""
