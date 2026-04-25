"""
Railway logs — puxa logs do bot Gus em produção via Railway GraphQL API.

CONFIGURAÇÃO (env vars no Railway):
- RAILWAY_API_TOKEN (obrigatório): Account/Project token criado no dashboard.
  → Account Settings → Tokens → Create token (ou Project → Settings → Tokens).

- RAILWAY_PROJECT_ID, RAILWAY_SERVICE_ID, RAILWAY_ENVIRONMENT_ID (opcionais):
  Railway INJETA AUTOMATICAMENTE essas variáveis no container do bot — não
  precisa configurar manualmente. Override só se rodar fora do Railway.

USO:
- logs_railway()                                → últimos 50 do deployment ativo
- logs_railway(linhas=100, filtro="Mem0")       → top 100 com 'Mem0'
- logs_railway(linhas=200, since_min=720)       → últimas 12h
- logs_railway(filtro="error", since_min=60)    → erros última hora
"""

import logging
import os
from datetime import datetime, timedelta, timezone

import httpx

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
RAILWAY_GRAPHQL_URL = "https://backboard.railway.app/graphql/v2"


async def _railway_graphql(query: str, variables: dict, token: str) -> dict | None:
    """Helper genérico pra chamar Railway GraphQL. Retorna data ou None em erro."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                RAILWAY_GRAPHQL_URL,
                json={"query": query, "variables": variables},
                headers=headers,
            )
        if resp.status_code != 200:
            logger.warning(
                f"Railway GraphQL status {resp.status_code}: {resp.text[:300]}"
            )
            return None
        body = resp.json()
        if "errors" in body:
            msgs = [e.get("message", "") for e in body["errors"]]
            logger.warning(f"Railway GraphQL errors: {msgs}")
            return None
        return body.get("data")
    except Exception as e:
        logger.error(f"Railway GraphQL exception: {e}")
        return None


async def _descobrir_deployment_id(
    token: str,
    project_id: str,
    service_id: str,
    environment_id: str | None,
) -> str | None:
    """Pega o ID do deployment mais recente do serviço."""
    query = """
    query LatestDeployment($projectId: String!, $serviceId: String, $environmentId: String) {
      deployments(
        input: {projectId: $projectId, serviceId: $serviceId, environmentId: $environmentId},
        first: 1
      ) {
        edges {
          node {
            id
            status
            createdAt
          }
        }
      }
    }
    """
    variables = {
        "projectId": project_id,
        "serviceId": service_id,
        "environmentId": environment_id,
    }
    data = await _railway_graphql(query, variables, token)
    if not data:
        return None
    edges = data.get("deployments", {}).get("edges", [])
    if not edges:
        return None
    return edges[0]["node"]["id"]


async def _puxar_logs(token: str, deployment_id: str, limit: int) -> list[dict] | None:
    """Puxa lista bruta de logs do deployment."""
    query = """
    query Logs($deploymentId: String!, $limit: Int!) {
      deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
        timestamp
        message
        severity
      }
    }
    """
    variables = {"deploymentId": deployment_id, "limit": limit}
    data = await _railway_graphql(query, variables, token)
    if not data:
        return None
    return data.get("deploymentLogs", []) or []


def _filtrar_logs(
    logs: list[dict],
    filtro: str | None,
    since_min: int | None,
) -> list[dict]:
    """Aplica filtros: janela temporal + substring case-insensitive em message."""
    if not logs:
        return []
    out = logs

    if since_min and since_min > 0:
        agora = datetime.now(timezone.utc)
        limite = agora - timedelta(minutes=since_min)
        filtrados = []
        for log in out:
            ts_str = log.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts >= limite:
                    filtrados.append(log)
            except Exception:
                # Sem timestamp parseável — preserva por segurança
                filtrados.append(log)
        out = filtrados

    if filtro:
        f = filtro.lower()
        out = [log for log in out if f in (log.get("message", "") or "").lower()]

    return out


def _formatar_logs(logs: list[dict], max_total: int = 4000) -> str:
    """Formata logs como texto pro Telegram, respeitando limite de chars."""
    if not logs:
        return "Nenhum log encontrado com esses filtros."

    linhas = []
    chars = 0
    for log in logs:
        ts_str = log.get("timestamp", "") or ""
        sev = (log.get("severity") or "").upper() or "INFO"
        msg = (log.get("message") or "").rstrip()

        ts_brt = ts_str
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            ts_brt = ts.astimezone(BRT).strftime("%H:%M:%S")
        except Exception:
            pass

        if len(msg) > 300:
            msg = msg[:297] + "..."

        linha = f"[{ts_brt}] {sev[:4]}: {msg}"
        if chars + len(linha) + 1 > max_total:
            linhas.append(f"... (truncado em {len(linhas)}/{len(logs)} logs)")
            break
        linhas.append(linha)
        chars += len(linha) + 1

    return "\n".join(linhas)


async def logs_railway(
    linhas: int = 50,
    filtro: str | None = None,
    since_min: int | None = None,
) -> str:
    """Puxa logs recentes do bot Gus do Railway.

    Args:
        linhas: máximo de logs (1-500). Default 50.
        filtro: substring case-insensitive em message. Ex: "Mem0", "error".
        since_min: só logs dos últimos N minutos. Ex: 60 = última hora.

    Returns:
        Texto pronto pro Telegram, ou mensagem de erro com instruções de setup.
    """
    token = os.getenv("RAILWAY_API_TOKEN")
    if not token:
        return (
            "RAILWAY_API_TOKEN não configurado. Pra ativar:\n"
            "1. Railway → Account Settings → Tokens → Create token\n"
            "2. Railway → seu projeto → Variables → RAILWAY_API_TOKEN=<token>\n"
            "3. Redeploy"
        )

    try:
        linhas = max(1, min(int(linhas), 500))
    except (TypeError, ValueError):
        linhas = 50

    project_id = os.getenv("RAILWAY_PROJECT_ID")
    service_id = os.getenv("RAILWAY_SERVICE_ID")
    environment_id = os.getenv("RAILWAY_ENVIRONMENT_ID")

    if not project_id or not service_id:
        return (
            "RAILWAY_PROJECT_ID ou RAILWAY_SERVICE_ID não detectado. "
            "Essas variáveis são auto-injetadas pelo Railway no container do bot. "
            "Se você está rodando fora dele, configure manualmente."
        )

    deployment_id = await _descobrir_deployment_id(
        token, project_id, service_id, environment_id
    )
    if not deployment_id:
        return (
            "Não consegui localizar deployment ativo. "
            "Confere que o RAILWAY_API_TOKEN tem permissão de leitura do projeto."
        )

    logs = await _puxar_logs(token, deployment_id, linhas)
    if logs is None:
        return (
            f"Erro ao puxar logs do deployment {deployment_id[:8]}. "
            "Veja warnings no log local pra diagnóstico."
        )

    logs_filtrados = _filtrar_logs(logs, filtro, since_min)

    cabecalho = [f"deploy `{deployment_id[:8]}`"]
    if since_min:
        cabecalho.append(f"últimos {since_min}min")
    if filtro:
        cabecalho.append(f'filtro="{filtro}"')
    cabecalho.append(f"{len(logs_filtrados)}/{len(logs)} logs")

    return f"📋 {' · '.join(cabecalho)}\n\n" + _formatar_logs(logs_filtrados)
