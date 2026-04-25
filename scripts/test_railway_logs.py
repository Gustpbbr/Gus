#!/usr/bin/env python3
"""
Script standalone pra testar a integração Railway antes de mergear pro main.

Faz uma cascata diagnóstica:
  1. Auth (chama 'me' — confirma que o token funciona)
  2. Lista projetos do user
  3. Pra cada projeto, lista services
  4. Pega último deployment do primeiro service encontrado
  5. Tenta puxar logs desse deployment

A cada passo imprime resposta CRUA (raw JSON) — útil pra diagnosticar
divergências entre o schema GraphQL real do Railway e o que o código
em gus/integrations/railway.py assume.

USO:
    Railway_diagnostic=<seu_token> python3 scripts/test_railway_logs.py

OU passando direto:
    python3 scripts/test_railway_logs.py <token>

NÃO commitar o token. Esse script só lê do env (ou argv) e não persiste.
"""

import asyncio
import json
import os
import sys

import httpx

RAILWAY_URL = "https://backboard.railway.app/graphql/v2"


async def gql(token: str, query: str, variables: dict | None = None) -> dict:
    """Chama Railway GraphQL e retorna body cru (com 'data' e/ou 'errors')."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"query": query, "variables": variables or {}}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(RAILWAY_URL, json=payload, headers=headers)
    print(f"  HTTP {resp.status_code}")
    try:
        return resp.json()
    except Exception:
        return {"_raw": resp.text}


def show(label: str, body: dict, max_chars: int = 1500):
    print(f"\n=== {label} ===")
    pretty = json.dumps(body, indent=2, ensure_ascii=False)
    if len(pretty) > max_chars:
        pretty = pretty[:max_chars] + f"\n... (truncado, total {len(pretty)} chars)"
    print(pretty)


async def main():
    token = os.environ.get("Railway_diagnostic") or (
        sys.argv[1] if len(sys.argv) > 1 else None
    )
    if not token:
        print("ERRO: Token não fornecido.")
        print("Uso: Railway_diagnostic=<token> python3 scripts/test_railway_logs.py")
        print("OU:  python3 scripts/test_railway_logs.py <token>")
        sys.exit(1)

    print(f"Token detectado: {token[:8]}...{token[-4:]} ({len(token)} chars)\n")

    # ---- Passo 1: auth via 'me' -------------------------------------------
    print(">>> Passo 1/5: confirmando auth via 'me' { id, email }")
    body = await gql(token, "{ me { id email name } }")
    show("Resposta 'me'", body)
    if "errors" in body:
        print("\n[!] 'me' não funciona. Tentando alternativas...")
        body = await gql(token, "{ viewer { id } }")
        show("Tentativa 'viewer'", body)

    # ---- Passo 2: listar projetos -----------------------------------------
    print("\n>>> Passo 2/5: listando projetos")
    query_projects = """
    query {
      me {
        projects {
          edges {
            node {
              id
              name
              services {
                edges { node { id name } }
              }
            }
          }
        }
      }
    }
    """
    body = await gql(token, query_projects)
    show("Resposta 'projects'", body)

    project_id = None
    service_id = None
    try:
        edges = body["data"]["me"]["projects"]["edges"]
        if edges:
            proj = edges[0]["node"]
            project_id = proj["id"]
            print(f"\n  Projeto encontrado: {proj['name']} (id={project_id[:8]}...)")
            services = proj.get("services", {}).get("edges", [])
            if services:
                svc = services[0]["node"]
                service_id = svc["id"]
                print(f"  Service encontrado: {svc['name']} (id={service_id[:8]}...)")
    except (KeyError, TypeError, IndexError):
        print("  [!] Schema diferente do esperado. Veja resposta crua acima.")

    if not project_id:
        print("\n[!] Sem project_id, parando aqui. Ajuste o script ou me cole a resposta crua.")
        return

    # ---- Passo 3: último deployment ---------------------------------------
    print(f"\n>>> Passo 3/5: último deployment do service")
    query_deploy = """
    query LatestDeployment($projectId: String!, $serviceId: String) {
      deployments(
        input: {projectId: $projectId, serviceId: $serviceId},
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
    body = await gql(token, query_deploy, {"projectId": project_id, "serviceId": service_id})
    show("Resposta 'deployments'", body)

    deployment_id = None
    try:
        deployment_id = body["data"]["deployments"]["edges"][0]["node"]["id"]
        status = body["data"]["deployments"]["edges"][0]["node"]["status"]
        print(f"\n  Deployment: {deployment_id[:8]}... (status={status})")
    except (KeyError, TypeError, IndexError):
        print("  [!] Schema 'deployments' divergente. Tentando query alternativa.")
        # Fallback: pode ser que o input seja outro
        alt_query = """
        query AltDeployments($projectId: String!) {
          project(id: $projectId) {
            deployments {
              edges { node { id status createdAt } }
            }
          }
        }
        """
        body_alt = await gql(token, alt_query, {"projectId": project_id})
        show("Tentativa alternativa 'project.deployments'", body_alt)
        try:
            deployment_id = body_alt["data"]["project"]["deployments"]["edges"][0]["node"]["id"]
        except Exception:
            pass

    if not deployment_id:
        print("\n[!] Sem deployment_id, parando aqui.")
        return

    # ---- Passo 4: logs do deployment --------------------------------------
    print(f"\n>>> Passo 4/5: puxando logs (limit=10)")
    query_logs = """
    query Logs($deploymentId: String!, $limit: Int!) {
      deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
        timestamp
        message
        severity
      }
    }
    """
    body = await gql(token, query_logs, {"deploymentId": deployment_id, "limit": 10})
    show("Resposta 'deploymentLogs'", body, max_chars=3000)

    if "errors" in body:
        print("\n[!] 'deploymentLogs' falhou. Possíveis nomes alternativos:")
        for alt_field in ["logs", "deploymentLog", "buildLogs"]:
            alt = (
                f"query A($id: String!) {{ {alt_field}(deploymentId: $id, limit: 5) "
                f"{{ timestamp message severity }} }}"
            )
            body_alt = await gql(token, alt, {"id": deployment_id})
            show(f"Tentativa '{alt_field}'", body_alt, max_chars=800)
            if "errors" not in body_alt:
                print(f"\n[OK] Campo correto é '{alt_field}'.")
                break

    # ---- Passo 5: resumo --------------------------------------------------
    print("\n>>> Passo 5/5: RESUMO")
    print(f"  Project ID:    {project_id or '—'}")
    print(f"  Service ID:    {service_id or '—'}")
    print(f"  Deployment ID: {deployment_id or '—'}")
    print("\nSe os 4 passos retornaram 'data' sem 'errors', o código em")
    print("gus/integrations/railway.py vai funcionar. Se algum tiver erro,")
    print("cola a resposta crua e eu corrijo o schema.")


if __name__ == "__main__":
    asyncio.run(main())
