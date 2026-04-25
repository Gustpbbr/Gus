"""
sugerir_wikilinks — Haiku propõe wikilinks pra um arquivo do repo.

Generaliza a lógica do .github/scripts/enrich_mem0_export.py: em vez de
processar só o export do Mem0, aceita qualquer .md do vault e sugere
wikilinks pra arquivos relacionados.

NÃO escreve automaticamente no arquivo. Retorna sugestões pro Telegram —
o Gustavo decide se aplica (passo separado, ainda não implementado).

ESTRATÉGIA:
1. Lê o arquivo alvo via GitHub Contents API
2. Lista TODOS os .md do repo via Tree API (1 call recursive)
3. Filtra candidatos: só pastas de conteúdo, exclui o próprio alvo
4. Extrai wikilinks já presentes no alvo (não duplica)
5. Chama Haiku com lista de candidatos + texto do alvo → JSON com sugestões
6. Valida: só aceita wikilinks que mapeiam pra .md real
7. Formata pro Telegram

CUSTO: ~1 call Sonnet por sugestão. ~3k tokens input + 500 output ~ $0.017.
Sonnet (e não Haiku) porque o custo de errar é alto: wikilink ruim polui o
grafo do Obsidian e cria conexão fraca permanente. Sonnet identifica conexão
temática real com mais precisão que Haiku, e a diferença ($0.012/call) é
desprezível.
"""

import base64
import json
import logging
import os
import re
from pathlib import PurePosixPath

import httpx

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-6"

PASTAS_CONTEUDO = (
    "pessoal/", "dimagem/", "projetos/", "receitas/", "esportes/",
    "leituras/", "capturado/", "agenda/", "gus/",
)
EXCLUIR_PREFIXOS = (
    "projetos/gus/",        # metadoc do próprio sistema
    "gus/meta-memoria",     # auto-reflexão, não conteúdo
    "gus/gus-identity",     # identidade
    "sensivel/",            # nunca cruza com sugestões públicas
    "_indices/",            # índices, não conteúdo
    ".github/",
    ".claude/",
)

PROMPT_SISTEMA = """Você analisa um arquivo .md do vault pessoal do Gustavo e sugere wikilinks pra outros .md existentes.

Critério rigoroso: só sugira um wikilink se o arquivo candidato tocar de forma SUBSTANTIVA E TEMÁTICA o tema do arquivo alvo. Na dúvida, NÃO sugira. Silêncio é muito melhor que ruído — wikilink ruim polui o grafo do Obsidian.

CONEXÕES VÁLIDAS (sugerir):
- Mesmo conceito, mesma pessoa, mesma decisão, mesmo projeto
- Continuação direta de tema (ex: dois exames do mesmo paciente, duas notas sobre o mesmo livro)
- Pergunta-resposta entre arquivos (um documenta, outro implementa)

CONEXÕES INVÁLIDAS (NÃO sugerir):
- **Apenas mesma data ou data próxima** — proximidade temporal não é tema. Um arquivo do dia 24/04 NÃO se conecta a outro do dia 24/04 só por isso.
- **Apenas mesma pasta** — pasta é organização, não tema.
- **Apenas palavra solta em comum** sem significado compartilhado.
- **Conexão hipotética** — "poderia ter relação" não basta.

Regras:
- Máximo 5 sugestões. Frequentemente 0 ou 1 é o número certo.
- Use NOME do arquivo sem extensão e sem path (ex: "historico-saude", não "pessoal/saude/historico-saude.md").
- Não sugira wikilinks que já estão presentes no arquivo (lista informada).
- Não sugira o próprio arquivo alvo.
- O motivo deve explicar o ELO TEMÁTICO, não temporal.

Responda EXCLUSIVAMENTE em JSON estrito, sem markdown nem prosa:
{
  "sugestoes": [
    {"wikilink": "historico-saude", "motivo": "menciona hipertireoidismo, tema central do alvo"},
    {"wikilink": "outro-arquivo", "motivo": "..."}
  ]
}
"""


async def _listar_mds_repo(token: str, repo: str, branch: str = "main") -> list[tuple[str, str]]:
    """Lista todos os .md do repo via Tree API. Retorna [(path, stem)]."""
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=headers)
    if r.status_code != 200:
        return []
    tree = r.json().get("tree", [])
    mds = []
    for entry in tree:
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        if not path.endswith(".md"):
            continue
        if not any(path.startswith(p) for p in PASTAS_CONTEUDO):
            continue
        if any(path.startswith(p) for p in EXCLUIR_PREFIXOS):
            continue
        stem = PurePosixPath(path).stem
        mds.append((path, stem))
    return mds


async def _ler_arquivo(token: str, repo: str, path: str, branch: str | None) -> str | None:
    """Lê conteúdo de um .md via Contents API."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {"ref": branch} if branch else None
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=headers, params=params)
    if r.status_code != 200:
        return None
    data = r.json()
    return base64.b64decode(data["content"]).decode("utf-8")


def _extrair_wikilinks(content: str) -> set[str]:
    """Extrai wikilinks já presentes no conteúdo. Normaliza pra stem."""
    matches = re.findall(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", content)
    presentes = set()
    for m in matches:
        # Remove path se vier completo, remove .md
        stem = PurePosixPath(m.strip()).stem
        if stem:
            presentes.add(stem)
    return presentes


async def _chamar_haiku(
    api_key: str,
    conteudo_alvo: str,
    alvo_stem: str,
    candidatos: list[tuple[str, str]],
    ja_presentes: set[str],
) -> list[dict]:
    """Chama Haiku com prompt fixo. Retorna lista de sugestões."""
    # Filtra candidatos: remove próprio alvo + já presentes
    candidatos_filtrados = [
        (p, s) for p, s in candidatos
        if s != alvo_stem and s not in ja_presentes
    ]
    if not candidatos_filtrados:
        return []

    # Trunca conteúdo do alvo se muito longo (Haiku context, custo)
    alvo_truncado = conteudo_alvo[:4000]
    if len(conteudo_alvo) > 4000:
        alvo_truncado += "\n\n[... conteúdo truncado em 4000 chars]"

    candidatos_fmt = "\n".join(f"- {p}  (nome: {s})" for p, s in candidatos_filtrados)
    presentes_fmt = ", ".join(sorted(ja_presentes)) if ja_presentes else "(nenhum)"

    user_msg = (
        f"## Arquivo alvo: `{alvo_stem}.md`\n\n"
        f"### Conteúdo:\n{alvo_truncado}\n\n"
        f"### Wikilinks já presentes (não sugira esses): {presentes_fmt}\n\n"
        f"### Candidatos disponíveis ({len(candidatos_filtrados)} arquivos):\n"
        f"{candidatos_fmt}\n\n"
        f"Retorne JSON com até 5 sugestões substantivas."
    )

    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "system": PROMPT_SISTEMA,
        "messages": [{"role": "user", "content": user_msg}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                "https://api.anthropic.com/v1/messages", json=payload, headers=headers
            )
        if r.status_code != 200:
            logger.warning(f"Haiku status {r.status_code}: {r.text[:200]}")
            return []
        texto = r.json()["content"][0]["text"].strip()
    except Exception as e:
        logger.error(f"Erro chamando Haiku: {e}")
        return []

    match = re.search(r"\{[\s\S]*\}", texto)
    if not match:
        logger.warning(f"Haiku não retornou JSON: {texto[:200]}")
        return []
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return []

    return data.get("sugestoes") or []


async def sugerir_wikilinks(arquivo: str, branch: str | None = None) -> str:
    """Sugere wikilinks pra um .md do repo.

    Args:
        arquivo: path do arquivo (ex: 'dimagem/dia/2026-04-25.md')
        branch: opcional, default main

    Returns:
        Texto pro Telegram com sugestões + wikilinks já presentes.
        Não modifica o arquivo.
    """
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not token:
        return "GITHUB_TOKEN não configurado."
    if not api_key:
        return "ANTHROPIC_API_KEY não configurado."

    arquivo = arquivo.strip().lstrip("/")
    if not arquivo.endswith(".md"):
        arquivo = arquivo + ".md"

    branch_efetivo = branch or "main"

    # Lê alvo + lista candidatos em paralelo? Não — preciso checar alvo primeiro
    # pra garantir existência. List + read sequencial é simples.
    conteudo = await _ler_arquivo(token, repo, arquivo, branch)
    if conteudo is None:
        ref_msg = f" (branch={branch})" if branch else ""
        return f"Arquivo não encontrado: `{arquivo}`{ref_msg}"

    candidatos = await _listar_mds_repo(token, repo, branch_efetivo)
    if not candidatos:
        return "Não consegui listar arquivos candidatos do repo."

    alvo_stem = PurePosixPath(arquivo).stem
    ja_presentes = _extrair_wikilinks(conteudo)

    sugestoes = await _chamar_haiku(
        api_key, conteudo, alvo_stem, candidatos, ja_presentes
    )

    # Valida: só aceita stems que estão na lista de candidatos
    nomes_validos = {s for _, s in candidatos}
    sugestoes_validas = [
        s for s in sugestoes
        if s.get("wikilink") in nomes_validos
        and s.get("wikilink") != alvo_stem
        and s.get("wikilink") not in ja_presentes
    ]

    # Formata saída
    linhas = [f"Sugestões pra `{arquivo}`:\n"]
    if not sugestoes_validas:
        linhas.append("Nenhuma sugestão substantiva — Haiku considerou ruído pra todos os candidatos.")
    else:
        for i, s in enumerate(sugestoes_validas, 1):
            wl = s.get("wikilink", "")
            motivo = s.get("motivo", "").strip()
            linhas.append(f"{i}. `[[{wl}]]` — {motivo}" if motivo else f"{i}. `[[{wl}]]`")

    if ja_presentes:
        linhas.append(f"\nJá presentes (preservados): {', '.join(f'`[[{w}]]`' for w in sorted(ja_presentes))}")

    linhas.append(
        "\nPra aplicar: confirme quais e eu adiciono via save_to_github, "
        "ou edite manual no Obsidian."
    )

    return "\n".join(linhas)
