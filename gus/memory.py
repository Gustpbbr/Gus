"""Acesso ao Hub Qdrant (gus_hub) — sem fallback Mem0 (item 1.9 do plano).

Histórico:
- Pré-ADR-001: este módulo era wrapper sobre `mem0ai.Memory`, escrevia/lia
  na coleção `gus` (Mem0 self-hosted) com fallback pro SaaS (api.mem0.ai).
- ADR-001 Fase 3 (27/04/2026): salvar_memorias migrou pra `hub.store.ingestar`,
  busca/delete tinham fallback Mem0 como rede de segurança.
- Fase 0 do plano de saneamento (02/05/2026): coleção legada Qdrant `gus` está
  vazia (Achado A8); conteúdo histórico do Mem0 SaaS preservado em
  `historico/mem0-saas-export-final-2026-05-02.json`.
- Item 1.9: fallback Mem0 removido completamente. Módulo é fina camada sobre
  `hub.store` agora — só preserva API antiga (`buscar_memorias`,
  `salvar_memorias`, `deletar_memoria`, `salvar_observacao_gus`,
  `buscar_memorias_gus`) pra não reescrever todos os callers.
"""

import os
import asyncio
import logging

logger = logging.getLogger(__name__)

# Dois "cérebros" no Hub:
# - USER_ID_GUSTAVO: memórias sobre o Gustavo (fatos, preferências, contexto pessoal)
# - USER_ID_GUS: autobiografia do próprio Gus (padrões operacionais, história do sistema)
USER_ID_GUSTAVO = "gustavo"
USER_ID_GUS = "gus"
USER_ID = USER_ID_GUSTAVO  # default retrocompatível

# Tag de origem default — identifica qual porta gerou essa memória.
# Lê env em cada call (em vez de cachear no import) — facilita testes e
# permite mudança runtime sem restart do processo.
def _via_default() -> str:
    return os.getenv("MEM0_VIA_TAG", "telegram-claude")


# Mantido como atributo do módulo pra compatibilidade com testes/imports
# que faziam `from gus.memory import VIA_DEFAULT`. Hoje resolvido via
# property-like — mas mantemos o nome legacy.
VIA_DEFAULT = _via_default()


async def buscar_memorias(query: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias relevantes para o contexto da conversa (Hub Qdrant)."""
    try:
        from hub.store import lembrar as hub_lembrar
        hub_results = await asyncio.to_thread(hub_lembrar, query, user_id, 5)
        if not hub_results:
            return ""
        linhas = [f"- {r['conteudo']}" for r in hub_results if r.get("conteudo")]
        if not linhas:
            return ""
        logger.info(f"Memória servida pelo Hub ({len(linhas)} fragmentos, user_id={user_id})")
        return "\n".join(linhas)
    except Exception as e:
        logger.warning(f"Hub.lembrar falhou (user_id={user_id}): {e}")
        return ""


async def salvar_memorias(
    messages: list[dict],
    user_id: str = USER_ID_GUSTAVO,
    via: str | None = None,
) -> None:
    """Salva fragmentos no Hub Qdrant (gus_hub) com tag de origem.

    Cada message vira um fragmento atômico via `hub.store.ingestar`.

    Casos de uso:
    - /foco no Telegram (gus/bot.py:handle_foco) — salva [FOCO-ATUAL] ...
    - salvar_observacao_gus (brain user_id=gus)

    Args:
        messages: lista de {role, content} — só "content" string é aproveitado.
                  Para content como lista (multimodal), só blocos type=text contam.
        user_id: 'gustavo' (default) ou 'gus' (auto-observações).
        via: tag de origem ('telegram-claude', 'claude-code', etc.).
    """
    from hub.store import ingestar

    via_tag = via or _via_default()
    metadata = {
        "user_id": user_id,
        "via": via_tag,
        # Sem classificação automática (tipo/area/camada) — quem chama essa
        # função (handle_foco) não tem o LLM curador no caminho.
        # Default tipo=episodico, camada=sessao no schema do Hub.
    }

    for msg in messages:
        content = msg.get("content")
        if isinstance(content, str):
            texto = content.strip()
        elif isinstance(content, list):
            partes = [
                c.get("text", "")
                for c in content
                if isinstance(c, dict) and c.get("type") == "text"
            ]
            texto = " ".join(p for p in partes if p).strip()
        else:
            texto = ""

        if not texto:
            continue

        try:
            await asyncio.to_thread(ingestar, texto, metadata)
        except Exception as e:
            logger.warning(f"Hub.ingestar falhou em salvar_memorias (user_id={user_id}): {e}")


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias com limite configurável, incluindo ID para deleção (Hub Qdrant)."""
    try:
        from hub.store import lembrar as hub_lembrar
        hub_results = await asyncio.to_thread(hub_lembrar, query, user_id, limit)
    except Exception as e:
        return f"Erro ao buscar (Hub) (user_id={user_id}): {e}"

    if not hub_results:
        return f"Nenhuma memória encontrada pra `{query}` no brain `{user_id}`."

    linhas = [f"Encontradas {len(hub_results)} memória(s) em `{user_id}` pra `{query}`:"]
    for i, r in enumerate(hub_results, 1):
        conteudo = (r.get("conteudo") or "").strip()
        mem_id = r.get("id") or "?"
        tipo = r.get("tipo") or "?"
        area = r.get("area") or "-"
        if conteudo:
            linhas.append(f"{i}. [{mem_id}] [{tipo}/{area}] {conteudo}")
    return "\n".join(linhas)


async def deletar_memoria(memory_id: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Deleta uma memória pelo ID. IRREVERSÍVEL.

    Trilha de auditoria automática gravada em `_log/deletar-hub/AAAA-MM-DD.jsonl`
    via `hub.store.deletar` (item 1.3 do plano de saneamento).
    """
    if not memory_id or not memory_id.strip():
        return "memory_id vazio, não dá pra deletar."
    mid = memory_id.strip()

    try:
        from hub.store import deletar as hub_deletar
        motivo = f"gus.memory.deletar_memoria user_id={user_id}"
        await asyncio.to_thread(hub_deletar, mid, motivo)
        return f"Memória `{mid}` deletada do Hub (user_id=`{user_id}`)."
    except Exception as e:
        return f"Erro ao deletar memória `{mid}`: {e}"


async def salvar_observacao_gus(observacao: str, via: str | None = None) -> str:
    """Salva uma observação autobiográfica do Gus (brain `gus`)."""
    if not observacao or not observacao.strip():
        return "Observação vazia, não salvei."
    try:
        await salvar_memorias(
            [{"role": "user", "content": observacao.strip()}],
            user_id=USER_ID_GUS,
            via=via,
        )
        return f"Observação salva no brain `gus`: \"{observacao[:80]}\""
    except Exception as e:
        return f"Erro ao salvar (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    """Busca nas memórias autobiográficas do Gus (brain `gus`)."""
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
