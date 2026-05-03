"""Testes do cache de auto_diagnostico (gus/integrations/diagnostico.py).

Item M5 do plano: cache TTL 5min pra evitar queimar 6 chamadas externas + 1
Anthropic (~$0.000004) toda vez que Gustavo pede /check em rajada.
"""

import time
from unittest.mock import patch, AsyncMock

import pytest

import gus.integrations.diagnostico as diag


def _reset_cache():
    diag._diag_cache = None


@pytest.fixture(autouse=True)
def _autoreset():
    _reset_cache()
    yield
    _reset_cache()


class TestCache:
    @pytest.mark.asyncio
    async def test_primeira_chamada_executa_checks(self):
        with patch.object(diag, "_check_github_pat", new=AsyncMock(return_value={"name": "GitHub Token", "status": "ok", "detail": "x"})):
            with patch.object(diag, "_check_hub", new=AsyncMock(return_value={"name": "Hub Qdrant", "status": "ok", "detail": "x"})):
                with patch.object(diag, "_check_anthropic", new=AsyncMock(return_value={"name": "Anthropic", "status": "ok", "detail": "x"})):
                    with patch.object(diag, "_check_tavily", new=AsyncMock(return_value={"name": "Tavily", "status": "ok", "detail": "x"})):
                        with patch.object(diag, "_check_volume", new=AsyncMock(return_value={"name": "Volume Railway", "status": "ok", "detail": "x"})):
                            with patch.object(diag, "_check_workflows", new=AsyncMock(return_value={"name": "Workflows GH", "status": "ok", "detail": "x"})):
                                out = await diag.auto_diagnostico()
        assert "Diagnóstico" in out
        assert "GitHub Token" in out
        assert "cache" not in out  # primeira call não tem prefixo de cache

    @pytest.mark.asyncio
    async def test_segunda_chamada_dentro_ttl_retorna_cache(self):
        # Popula cache manualmente
        diag._diag_cache = {"timestamp": time.time(), "result": "tabela cacheada"}

        # Mocka pra detectar se rodou (não deve)
        ran = {"count": 0}
        async def fake_check(*args, **kwargs):
            ran["count"] += 1
            return {"name": "x", "status": "ok", "detail": "x"}

        with patch.object(diag, "_check_github_pat", side_effect=fake_check):
            out = await diag.auto_diagnostico()
        assert "tabela cacheada" in out
        assert "cache" in out  # prefixo informativo
        assert ran["count"] == 0  # checks não rodaram

    @pytest.mark.asyncio
    async def test_force_true_ignora_cache(self):
        diag._diag_cache = {"timestamp": time.time(), "result": "deveria ser ignorado"}

        with patch.object(diag, "_check_github_pat", new=AsyncMock(return_value={"name": "GitHub Token", "status": "ok", "detail": "fresh"})):
            with patch.object(diag, "_check_hub", new=AsyncMock(return_value={"name": "Hub Qdrant", "status": "ok", "detail": "x"})):
                with patch.object(diag, "_check_anthropic", new=AsyncMock(return_value={"name": "Anthropic", "status": "ok", "detail": "x"})):
                    with patch.object(diag, "_check_tavily", new=AsyncMock(return_value={"name": "Tavily", "status": "ok", "detail": "x"})):
                        with patch.object(diag, "_check_volume", new=AsyncMock(return_value={"name": "Volume Railway", "status": "ok", "detail": "x"})):
                            with patch.object(diag, "_check_workflows", new=AsyncMock(return_value={"name": "Workflows GH", "status": "ok", "detail": "x"})):
                                out = await diag.auto_diagnostico(force=True)
        assert "fresh" in out  # rodou checks
        assert "deveria ser ignorado" not in out

    @pytest.mark.asyncio
    async def test_cache_expira_apos_ttl(self):
        # Cache expirado (timestamp velho)
        diag._diag_cache = {
            "timestamp": time.time() - diag._DIAG_CACHE_TTL_SEC - 10,
            "result": "expirado"
        }

        with patch.object(diag, "_check_github_pat", new=AsyncMock(return_value={"name": "GitHub Token", "status": "ok", "detail": "novo"})):
            with patch.object(diag, "_check_hub", new=AsyncMock(return_value={"name": "Hub Qdrant", "status": "ok", "detail": "x"})):
                with patch.object(diag, "_check_anthropic", new=AsyncMock(return_value={"name": "Anthropic", "status": "ok", "detail": "x"})):
                    with patch.object(diag, "_check_tavily", new=AsyncMock(return_value={"name": "Tavily", "status": "ok", "detail": "x"})):
                        with patch.object(diag, "_check_volume", new=AsyncMock(return_value={"name": "Volume Railway", "status": "ok", "detail": "x"})):
                            with patch.object(diag, "_check_workflows", new=AsyncMock(return_value={"name": "Workflows GH", "status": "ok", "detail": "x"})):
                                out = await diag.auto_diagnostico()
        assert "novo" in out
        assert "expirado" not in out

    @pytest.mark.asyncio
    async def test_cache_atualiza_apos_run(self):
        with patch.object(diag, "_check_github_pat", new=AsyncMock(return_value={"name": "GitHub Token", "status": "ok", "detail": "x"})):
            with patch.object(diag, "_check_hub", new=AsyncMock(return_value={"name": "Hub Qdrant", "status": "ok", "detail": "x"})):
                with patch.object(diag, "_check_anthropic", new=AsyncMock(return_value={"name": "Anthropic", "status": "ok", "detail": "x"})):
                    with patch.object(diag, "_check_tavily", new=AsyncMock(return_value={"name": "Tavily", "status": "ok", "detail": "x"})):
                        with patch.object(diag, "_check_volume", new=AsyncMock(return_value={"name": "Volume Railway", "status": "ok", "detail": "x"})):
                            with patch.object(diag, "_check_workflows", new=AsyncMock(return_value={"name": "Workflows GH", "status": "ok", "detail": "x"})):
                                await diag.auto_diagnostico()
        assert diag._diag_cache is not None
        assert "timestamp" in diag._diag_cache
        assert "result" in diag._diag_cache
