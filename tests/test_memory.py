"""Testes da camada de memória (gus/memory.py) — Hub-only após item 1.9."""

import pytest
from unittest.mock import patch, MagicMock

from gus.memory import (
    salvar_memorias, buscar_memorias,
    USER_ID_GUSTAVO, USER_ID_GUS, VIA_DEFAULT,
)


class TestSalvarMemorias:
    @pytest.mark.asyncio
    async def test_salva_string_content(self):
        ingestar_mock = MagicMock(return_value="frag-id-1")
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias(
                [{"role": "user", "content": "Gustavo prefere X"}],
                user_id=USER_ID_GUSTAVO,
            )

        ingestar_mock.assert_called_once()
        texto, metadata = ingestar_mock.call_args[0]
        assert texto == "Gustavo prefere X"
        assert metadata["user_id"] == "gustavo"
        assert metadata["via"] == VIA_DEFAULT

    @pytest.mark.asyncio
    async def test_salva_content_lista_multimodal(self):
        ingestar_mock = MagicMock(return_value="id")
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias([{
                "role": "user",
                "content": [
                    {"type": "text", "text": "primeiro"},
                    {"type": "text", "text": "segundo"},
                    {"type": "image", "source": {}},  # ignorado
                ],
            }])
        texto, _ = ingestar_mock.call_args[0]
        assert "primeiro" in texto
        assert "segundo" in texto

    @pytest.mark.asyncio
    async def test_skip_content_vazio(self):
        ingestar_mock = MagicMock()
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias([{"role": "user", "content": ""}])
            await salvar_memorias([{"role": "user", "content": "   "}])
            await salvar_memorias([{"role": "user", "content": None}])
        ingestar_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_user_id_gus(self):
        ingestar_mock = MagicMock(return_value="id")
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias(
                [{"role": "user", "content": "auto-observação"}],
                user_id=USER_ID_GUS,
            )
        _, metadata = ingestar_mock.call_args[0]
        assert metadata["user_id"] == "gus"

    @pytest.mark.asyncio
    async def test_via_customizado(self):
        ingestar_mock = MagicMock(return_value="id")
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias(
                [{"role": "user", "content": "texto"}],
                via="custom-tag",
            )
        _, metadata = ingestar_mock.call_args[0]
        assert metadata["via"] == "custom-tag"

    @pytest.mark.asyncio
    async def test_falha_no_hub_nao_propaga(self):
        """salvar_memorias é chamado de fluxo fire-and-forget — exceções
        do Hub não devem quebrar a resposta do bot."""
        def fake_ingestar(*args, **kwargs):
            raise RuntimeError("Hub indisponível")

        with patch("hub.store.ingestar", fake_ingestar):
            # Não deve levantar
            await salvar_memorias([{"role": "user", "content": "texto"}])

    @pytest.mark.asyncio
    async def test_multiplas_messages_uma_chamada_cada(self):
        ingestar_mock = MagicMock(return_value="id")
        with patch("hub.store.ingestar", ingestar_mock):
            await salvar_memorias([
                {"role": "user", "content": "primeiro"},
                {"role": "user", "content": "segundo"},
                {"role": "user", "content": ""},  # skip
                {"role": "user", "content": "terceiro"},
            ])
        assert ingestar_mock.call_count == 3


class TestBuscarMemorias:
    @pytest.mark.asyncio
    async def test_hub_retorna_resultados(self):
        hub_mock = MagicMock(return_value=[
            {"conteudo": "fragmento A", "id": "1"},
            {"conteudo": "fragmento B", "id": "2"},
        ])
        with patch("hub.store.lembrar", hub_mock):
            out = await buscar_memorias("query", USER_ID_GUSTAVO)
        assert "fragmento A" in out
        assert "fragmento B" in out

    @pytest.mark.asyncio
    async def test_hub_vazio_retorna_string_vazia(self):
        """Item 1.9: sem fallback Mem0 — Hub vazio retorna '' direto."""
        hub_mock = MagicMock(return_value=[])
        with patch("hub.store.lembrar", hub_mock):
            out = await buscar_memorias("query")
        assert out == ""

    @pytest.mark.asyncio
    async def test_hub_falha_retorna_vazio(self):
        """Item 1.9: sem fallback. Exception no Hub vira string vazia
        (busca é silenciosa, não propaga erro pra resposta do bot)."""
        def hub_fail(*args, **kwargs):
            raise RuntimeError("Hub timeout")

        with patch("hub.store.lembrar", hub_fail):
            out = await buscar_memorias("query")
        assert out == ""

    @pytest.mark.asyncio
    async def test_filtra_conteudo_vazio(self):
        """Hub pode retornar fragmentos sem 'conteudo' — filtrar."""
        hub_mock = MagicMock(return_value=[
            {"conteudo": "ok", "id": "1"},
            {"conteudo": "", "id": "2"},  # filtrado
            {"id": "3"},  # sem campo conteudo, filtrado
        ])
        with patch("hub.store.lembrar", hub_mock):
            out = await buscar_memorias("query")
        assert "ok" in out
        # Conta linhas (1 fragmento => 1 linha)
        assert out.count("\n") == 0
