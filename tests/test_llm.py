"""Testes do dispatcher LLM (gus/llm.py).

Foco em funções puras + lógica de fallback de pricing/erros. Chamadas reais
à API ficam mockadas — sem teste de integração com Anthropic/OpenAI aqui.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

import anthropic

from gus.llm import (
    _get_pricing, _mensagem_erro_amigavel, _mensagem_erro_amigavel_openai,
    _anthropic_to_openai_tools, _history_to_openai, _escolher_provider,
    _build_system_blocks, _build_tools_cached, chamar_claude_com_retry,
    _detectar_tipos_midia, _converter_anthropic_para_openai_vision,
    _tentar_vision_fallback,
    MODEL_PRICING, FALLBACK_PRICING,
)


class TestGetPricing:
    def test_match_exato_gpt_4o_mini(self):
        # gpt-4o-mini é mais barato que gpt-4o — match exato evita confusão
        p = _get_pricing("gpt-4o-mini")
        assert p == MODEL_PRICING["gpt-4o-mini"]
        assert p["input"] < MODEL_PRICING["gpt-4o"]["input"]

    def test_match_exato_gpt_4o(self):
        assert _get_pricing("gpt-4o") == MODEL_PRICING["gpt-4o"]

    def test_familia_sonnet(self):
        # claude-sonnet-4-6 contém "sonnet" — match por substring
        assert _get_pricing("claude-sonnet-4-6") == MODEL_PRICING["sonnet"]

    def test_familia_haiku(self):
        assert _get_pricing("claude-haiku-4-5") == MODEL_PRICING["haiku"]

    def test_familia_opus(self):
        assert _get_pricing("claude-opus-4-7") == MODEL_PRICING["opus"]

    def test_modelo_desconhecido_usa_fallback(self):
        assert _get_pricing("modelo-totalmente-novo") == FALLBACK_PRICING

    def test_case_insensitive(self):
        assert _get_pricing("CLAUDE-SONNET-4-6") == MODEL_PRICING["sonnet"]


class TestMensagemErroAmigavelAnthropic:
    def _build_error(self, status, body=None):
        e = MagicMock(spec=anthropic.APIStatusError)
        e.status_code = status
        e.body = body or {}
        return e

    def test_credit_balance(self):
        e = self._build_error(400, {"error": {"message": "credit balance is too low"}})
        msg = _mensagem_erro_amigavel(e)
        assert "créditos" in msg
        assert "console.anthropic.com" in msg

    def test_status_401_authentication(self):
        e = self._build_error(401, {"error": {"type": "authentication_error", "message": "x"}})
        msg = _mensagem_erro_amigavel(e)
        assert "ANTHROPIC_API_KEY" in msg

    def test_status_413(self):
        e = self._build_error(413, {"error": {"type": "request_too_large", "message": "x"}})
        msg = _mensagem_erro_amigavel(e)
        assert "/reset" in msg

    def test_status_429(self):
        e = self._build_error(429, {"error": {"message": "rate limit"}})
        msg = _mensagem_erro_amigavel(e)
        assert "rate" in msg.lower() or "30s" in msg

    def test_timeout(self):
        e = anthropic.APITimeoutError(request=MagicMock())
        msg = _mensagem_erro_amigavel(e)
        assert "demorou demais" in msg or "1 min" in msg

    def test_connection_error(self):
        e = anthropic.APIConnectionError(request=MagicMock())
        msg = _mensagem_erro_amigavel(e)
        assert "conectar" in msg.lower() or "rede" in msg.lower()


class TestMensagemErroAmigavelOpenAI:
    def test_quota(self):
        e = Exception("insufficient_quota: please add billing")
        msg = _mensagem_erro_amigavel_openai(e)
        assert "OpenAI" in msg
        assert "billing" in msg or "créditos" in msg

    def test_invalid_key(self):
        e = MagicMock()
        e.status_code = 401
        e.__str__ = lambda self: "invalid_api_key"
        msg = _mensagem_erro_amigavel_openai(e)
        # Espera string neutra com mensagem específica
        assert isinstance(msg, str)


class TestAnthropicToOpenAiTools:
    def test_converte_estrutura_basica(self):
        tools = [{
            "name": "test_tool",
            "description": "uma tool",
            "input_schema": {"type": "object", "properties": {"x": {"type": "string"}}}
        }]
        out = _anthropic_to_openai_tools(tools)
        assert len(out) == 1
        assert out[0]["type"] == "function"
        assert out[0]["function"]["name"] == "test_tool"
        assert out[0]["function"]["description"] == "uma tool"
        assert out[0]["function"]["parameters"]["type"] == "object"

    def test_lista_vazia(self):
        assert _anthropic_to_openai_tools([]) == []

    def test_sem_input_schema(self):
        tools = [{"name": "x", "description": "d"}]
        out = _anthropic_to_openai_tools(tools)
        assert out[0]["function"]["parameters"] == {"type": "object", "properties": {}}


class TestHistoryToOpenAi:
    def test_user_string(self):
        msgs = [{"role": "user", "content": "oi"}]
        out = _history_to_openai(msgs)
        assert out == [{"role": "user", "content": "oi"}]

    def test_user_lista_blocos(self):
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": "primeiro"},
            {"type": "text", "text": "segundo"},
        ]}]
        out = _history_to_openai(msgs)
        assert "primeiro" in out[0]["content"]
        assert "segundo" in out[0]["content"]

    def test_imagem_substituida_por_marcador(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {}},
        ]}]
        out = _history_to_openai(msgs)
        assert "[imagem anexada]" in out[0]["content"]

    def test_documento_substituido_por_marcador(self):
        msgs = [{"role": "user", "content": [
            {"type": "document", "source": {}},
        ]}]
        out = _history_to_openai(msgs)
        assert "[documento anexado]" in out[0]["content"]

    def test_assistant_string_preservada(self):
        msgs = [{"role": "assistant", "content": "ok"}]
        out = _history_to_openai(msgs)
        assert out[0]["role"] == "assistant"
        assert out[0]["content"] == "ok"


class TestEscolherProvider:
    def test_texto_puro_va_pra_openai(self):
        msgs = [{"role": "user", "content": [{"type": "text", "text": "oi"}]}]
        provider, motivo = _escolher_provider(msgs)
        assert provider == "openai"

    def test_imagem_va_pra_anthropic(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {}},
        ]}]
        provider, motivo = _escolher_provider(msgs)
        assert provider == "anthropic"
        assert "image" in motivo

    def test_documento_va_pra_anthropic(self):
        msgs = [{"role": "user", "content": [
            {"type": "document", "source": {}},
        ]}]
        provider, motivo = _escolher_provider(msgs)
        assert provider == "anthropic"

    def test_rollback_flag(self, monkeypatch):
        monkeypatch.setenv("MULTIMODEL_ENABLED", "false")
        msgs = [{"role": "user", "content": [{"type": "text", "text": "oi"}]}]
        provider, motivo = _escolher_provider(msgs)
        assert provider == "anthropic"
        assert "rollback" in motivo

    def test_string_content_va_pra_openai(self):
        # content como string (não lista) também roteia
        msgs = [{"role": "user", "content": "texto direto"}]
        provider, motivo = _escolher_provider(msgs)
        assert provider == "openai"


class TestBuildSystemBlocks:
    def test_um_bloco_estavel_com_cache(self):
        blocks = _build_system_blocks("system estável", "")
        assert len(blocks) == 1
        assert blocks[0]["text"] == "system estável"
        assert blocks[0]["cache_control"] == {"type": "ephemeral"}

    def test_dois_blocos_quando_tem_suffix(self):
        blocks = _build_system_blocks("estável", "data atual")
        assert len(blocks) == 2
        assert blocks[0]["cache_control"] == {"type": "ephemeral"}
        assert blocks[1]["text"] == "data atual"
        # bloco variável NÃO tem cache_control
        assert "cache_control" not in blocks[1]


class TestBuildToolsCached:
    def test_lista_vazia(self):
        assert _build_tools_cached([]) == []

    def test_marca_anchor_quando_no_final(self):
        # rotear_arquivo é a anchor configurada — quando está no final, marca lá
        tools = [
            {"name": "a", "description": "1"},
            {"name": "b", "description": "2"},
            {"name": "rotear_arquivo", "description": "3"},
        ]
        out = _build_tools_cached(tools)
        assert "cache_control" not in out[0]
        assert "cache_control" not in out[1]
        assert out[2]["cache_control"] == {"type": "ephemeral"}

    def test_fallback_para_ultimo_se_anchor_ausente(self):
        # sem rotear_arquivo, marca último
        tools = [
            {"name": "a"},
            {"name": "b"},
            {"name": "c"},
        ]
        out = _build_tools_cached(tools)
        assert out[-1]["cache_control"] == {"type": "ephemeral"}

    def test_marca_anchor_no_meio_emite_warn(self, caplog):
        # anchor fora do final — funciona, mas warn no log
        import logging
        caplog.set_level(logging.WARNING)
        tools = [
            {"name": "a"},
            {"name": "rotear_arquivo"},
            {"name": "b"},
        ]
        out = _build_tools_cached(tools)
        assert out[1]["cache_control"] == {"type": "ephemeral"}
        assert "cache_control" not in out[2]
        # Warn emitido
        assert any("CACHE_ANCHOR" in r.message for r in caplog.records)

    def test_nao_muta_lista_original(self):
        tools = [{"name": "rotear_arquivo"}]
        _build_tools_cached(tools)
        assert "cache_control" not in tools[0]


class TestChamarClaudeComRetry:
    @pytest.mark.asyncio
    async def test_omite_system_quando_vazio(self, monkeypatch):
        """Bug histórico: system='' disparou 400 'temperature and top_p'.
        Validação: kwargs['system'] não pode existir se system_prompt é falsy."""
        kwargs_recebido = {}

        async def fake_create(**kwargs):
            kwargs_recebido.update(kwargs)
            resp = MagicMock()
            resp.stop_reason = "end_turn"
            resp.content = [MagicMock(text="ok", type="text")]
            resp.usage.input_tokens = 1
            resp.usage.output_tokens = 1
            return resp

        with patch("gus.llm.client.messages.create", new=fake_create):
            await chamar_claude_com_retry(
                model="claude-sonnet-4-6",
                max_tokens=10,
                system_prompt="",
                messages=[{"role": "user", "content": "oi"}],
            )

        assert "system" not in kwargs_recebido

    @pytest.mark.asyncio
    async def test_inclui_system_quando_truthy(self):
        kwargs_recebido = {}

        async def fake_create(**kwargs):
            kwargs_recebido.update(kwargs)
            resp = MagicMock()
            resp.stop_reason = "end_turn"
            resp.content = [MagicMock(text="ok", type="text")]
            resp.usage.input_tokens = 1
            resp.usage.output_tokens = 1
            return resp

        with patch("gus.llm.client.messages.create", new=fake_create):
            await chamar_claude_com_retry(
                model="claude-sonnet-4-6",
                max_tokens=10,
                system_prompt="você é o gus",
                messages=[{"role": "user", "content": "oi"}],
            )

        assert kwargs_recebido.get("system") == "você é o gus"

    @pytest.mark.asyncio
    async def test_retry_em_5xx_e_eventual_sucesso(self):
        chamadas = {"n": 0}

        async def fake_create(**kwargs):
            chamadas["n"] += 1
            if chamadas["n"] < 3:
                err = MagicMock(spec=anthropic.APIStatusError)
                err.status_code = 503
                raise anthropic.APIStatusError("overloaded", response=MagicMock(status_code=503), body={})
            resp = MagicMock()
            resp.stop_reason = "end_turn"
            resp.content = [MagicMock(text="recuperou", type="text")]
            resp.usage.input_tokens = 1
            resp.usage.output_tokens = 1
            return resp

        with patch("gus.llm.client.messages.create", new=fake_create):
            with patch("gus.llm.asyncio.sleep", new=AsyncMock()):  # acelera teste
                resp = await chamar_claude_com_retry(
                    model="claude-sonnet-4-6",
                    max_tokens=10,
                    system_prompt="x",
                    messages=[{"role": "user", "content": "oi"}],
                    max_tentativas=4,
                )
        assert chamadas["n"] == 3

    @pytest.mark.asyncio
    async def test_4xx_nao_retry_propaga(self):
        chamadas = {"n": 0}

        async def fake_create(**kwargs):
            chamadas["n"] += 1
            raise anthropic.APIStatusError(
                "bad request",
                response=MagicMock(status_code=400),
                body={"error": {"message": "x"}},
            )

        with patch("gus.llm.client.messages.create", new=fake_create):
            with patch("gus.llm.asyncio.sleep", new=AsyncMock()):
                with pytest.raises(anthropic.APIStatusError):
                    await chamar_claude_com_retry(
                        model="claude-sonnet-4-6",
                        max_tokens=10,
                        system_prompt="x",
                        messages=[{"role": "user", "content": "oi"}],
                        max_tentativas=4,
                    )
        # 4xx (exceto 429) não retenta — uma chamada só
        assert chamadas["n"] == 1

    @pytest.mark.asyncio
    async def test_429_retenta(self):
        chamadas = {"n": 0}

        async def fake_create(**kwargs):
            chamadas["n"] += 1
            if chamadas["n"] < 2:
                raise anthropic.APIStatusError(
                    "rate limit",
                    response=MagicMock(status_code=429),
                    body={"error": {"message": "rate limit"}},
                )
            resp = MagicMock()
            resp.stop_reason = "end_turn"
            resp.content = [MagicMock(text="ok", type="text")]
            resp.usage.input_tokens = 1
            resp.usage.output_tokens = 1
            return resp

        with patch("gus.llm.client.messages.create", new=fake_create):
            with patch("gus.llm.asyncio.sleep", new=AsyncMock()):
                await chamar_claude_com_retry(
                    model="claude-sonnet-4-6",
                    max_tokens=10,
                    system_prompt="x",
                    messages=[{"role": "user", "content": "oi"}],
                    max_tentativas=4,
                )
        assert chamadas["n"] == 2


# ===========================================================================
# Vision fallback Anthropic → OpenAI (Fase 3)
# ===========================================================================


class TestDetectarTiposMidia:
    def test_so_texto_retorna_vazio(self):
        msgs = [{"role": "user", "content": "oi"}]
        assert _detectar_tipos_midia(msgs) == set()

    def test_lista_so_texto_retorna_vazio(self):
        msgs = [{"role": "user", "content": [{"type": "text", "text": "oi"}]}]
        assert _detectar_tipos_midia(msgs) == set()

    def test_imagem_retorna_image(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "data": "x"}},
            {"type": "text", "text": "o que é?"},
        ]}]
        assert _detectar_tipos_midia(msgs) == {"image"}

    def test_pdf_retorna_document(self):
        msgs = [{"role": "user", "content": [
            {"type": "document", "source": {"type": "base64", "data": "x"}},
        ]}]
        assert _detectar_tipos_midia(msgs) == {"document"}

    def test_imagem_e_pdf_retorna_ambos(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"data": "x"}},
            {"type": "document", "source": {"data": "y"}},
        ]}]
        assert _detectar_tipos_midia(msgs) == {"image", "document"}

    def test_olha_apenas_ultimo_user_message(self):
        # Imagem em msg antiga não conta — só último user
        msgs = [
            {"role": "user", "content": [{"type": "image", "source": {"data": "x"}}]},
            {"role": "assistant", "content": "vi"},
            {"role": "user", "content": "explica"},
        ]
        assert _detectar_tipos_midia(msgs) == set()

    def test_history_vazio(self):
        assert _detectar_tipos_midia([]) == set()


class TestConverterAnthropicParaOpenAIVision:
    def test_string_content_passa_intacto(self):
        msgs = [{"role": "user", "content": "oi mundo"}]
        out = _converter_anthropic_para_openai_vision(msgs)
        assert out == [{"role": "user", "content": "oi mundo"}]

    def test_imagem_base64_convertida(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64", "media_type": "image/jpeg", "data": "ABC123"
            }},
            {"type": "text", "text": "o que é?"},
        ]}]
        out = _converter_anthropic_para_openai_vision(msgs)
        assert len(out) == 1
        blocks = out[0]["content"]
        # Ambos blocos: image_url + text
        assert len(blocks) == 2
        assert blocks[0]["type"] == "image_url"
        assert blocks[0]["image_url"]["url"] == "data:image/jpeg;base64,ABC123"
        assert blocks[1] == {"type": "text", "text": "o que é?"}

    def test_imagem_sem_media_type_default_jpeg(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"data": "XYZ"}},  # sem media_type
        ]}]
        out = _converter_anthropic_para_openai_vision(msgs)
        # Bloco único de imagem — vira lista
        assert out[0]["content"][0]["image_url"]["url"] == "data:image/jpeg;base64,XYZ"

    def test_pdf_vira_placeholder_texto(self):
        msgs = [{"role": "user", "content": [
            {"type": "document", "source": {"data": "PDFDATA"}},
            {"type": "text", "text": "analisa"},
        ]}]
        out = _converter_anthropic_para_openai_vision(msgs)
        # PDF placeholder + texto — 2 blocks (caller deve recusar antes via _detectar_tipos_midia)
        blocks = out[0]["content"]
        assert any("PDF" in b.get("text", "") for b in blocks if b.get("type") == "text")

    def test_bloco_unico_texto_vira_string(self):
        msgs = [{"role": "user", "content": [{"type": "text", "text": "só texto"}]}]
        out = _converter_anthropic_para_openai_vision(msgs)
        assert out[0]["content"] == "só texto"  # achatado

    def test_assistant_string_preservado(self):
        msgs = [{"role": "assistant", "content": "ok"}]
        out = _converter_anthropic_para_openai_vision(msgs)
        assert out[0] == {"role": "assistant", "content": "ok"}

    def test_imagem_sem_data_ignorada(self):
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {}},  # data ausente
            {"type": "text", "text": "fallback"},
        ]}]
        out = _converter_anthropic_para_openai_vision(msgs)
        # imagem sem data não vira image_url; fica só o texto
        blocks = out[0]["content"]
        # texto único achatado pra string
        assert blocks == "fallback" or (
            isinstance(blocks, list) and all(b.get("type") != "image_url" for b in blocks)
        )


class TestTentarVisionFallback:
    @pytest.mark.asyncio
    async def test_retorna_none_se_multimodel_disabled(self, monkeypatch):
        monkeypatch.setenv("MULTIMODEL_ENABLED", "false")
        msgs = [{"role": "user", "content": [{"type": "image", "source": {"data": "x"}}]}]
        exc = RuntimeError("anthropic down")
        out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is None

    @pytest.mark.asyncio
    async def test_retorna_none_sem_openai_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        msgs = [{"role": "user", "content": [{"type": "image", "source": {"data": "x"}}]}]
        exc = RuntimeError("anthropic down")
        out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is None

    @pytest.mark.asyncio
    async def test_retorna_none_se_so_texto(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "fake")
        monkeypatch.setenv("MULTIMODEL_ENABLED", "true")
        msgs = [{"role": "user", "content": "só texto"}]
        exc = RuntimeError("anthropic down")
        out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is None

    @pytest.mark.asyncio
    async def test_pdf_retorna_msg_especifica(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "fake")
        monkeypatch.setenv("MULTIMODEL_ENABLED", "true")
        msgs = [{"role": "user", "content": [
            {"type": "document", "source": {"data": "pdf"}}
        ]}]
        exc = RuntimeError("anthropic down")
        out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is not None
        text, metadata = out
        assert "PDF" in text
        assert "print" in text.lower() or "fallback" in text.lower()
        assert metadata["error"] == "pdf_sem_fallback"

    @pytest.mark.asyncio
    async def test_imagem_aciona_openai_vision(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "fake")
        monkeypatch.setenv("MULTIMODEL_ENABLED", "true")
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": "ABC"}},
            {"type": "text", "text": "o que é?"},
        ]}]
        exc = RuntimeError("anthropic down")

        # Mocka _gerar_resposta_openai_vision pra retornar valor controlado
        async def fake_vision(messages, memory_context):
            return "uma foto de teste", {
                "model": "gpt-4o", "tokens_in": 10, "tokens_out": 5,
                "cost_usd": 0.001, "provider": "openai-vision-fallback",
            }

        with patch("gus.llm._gerar_resposta_openai_vision", new=fake_vision):
            out = await _tentar_vision_fallback(msgs, "", exc)

        assert out is not None
        text, metadata = out
        assert "fallback" in text.lower()
        assert "uma foto de teste" in text
        assert metadata["provider"] == "openai-vision-fallback"

    @pytest.mark.asyncio
    async def test_vision_explode_retorna_none(self, monkeypatch):
        """Se gpt-4o também falhar, fallback deixa caller usar erro original."""
        monkeypatch.setenv("OPENAI_API_KEY", "fake")
        monkeypatch.setenv("MULTIMODEL_ENABLED", "true")
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"data": "x"}},
        ]}]
        exc = RuntimeError("anthropic down")

        async def fake_vision_fail(messages, memory_context):
            raise RuntimeError("openai também caiu")

        with patch("gus.llm._gerar_resposta_openai_vision", new=fake_vision_fail):
            out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is None

    @pytest.mark.asyncio
    async def test_imagem_e_pdf_juntos_recusa_pdf(self, monkeypatch):
        """Se vier ambos, prevalece o caminho PDF (sem fallback completo)."""
        monkeypatch.setenv("OPENAI_API_KEY", "fake")
        monkeypatch.setenv("MULTIMODEL_ENABLED", "true")
        msgs = [{"role": "user", "content": [
            {"type": "image", "source": {"data": "x"}},
            {"type": "document", "source": {"data": "y"}},
        ]}]
        exc = RuntimeError("anthropic down")
        out = await _tentar_vision_fallback(msgs, "", exc)
        assert out is not None
        text, metadata = out
        assert "PDF" in text
        assert metadata["error"] == "pdf_sem_fallback"


# ===========================================================================
# Regressão SDK Anthropic (M4 — upgrade 0.40 → 0.50+)
# ===========================================================================
#
# gus/llm.py depende de campos específicos do anthropic.types.Usage e
# anthropic.types.Message. Se o SDK Anthropic mudar/remover esses campos,
# `_gerar_resposta_anthropic` quebra silencioso (cost_tracking errado,
# cache_hit_ratio sempre zero, etc.). Estes testes verificam que os
# nomes dos campos continuam disponíveis no SDK instalado.


class TestAnthropicSDKContrato:
    def test_usage_tem_campos_criticos(self):
        """Campos que gus/llm.py:_gerar_resposta_anthropic lê do response.usage."""
        from anthropic.types import Usage
        campos = set(Usage.model_fields.keys())
        # Ler em response.usage.X
        assert "input_tokens" in campos
        assert "output_tokens" in campos
        assert "cache_creation_input_tokens" in campos
        assert "cache_read_input_tokens" in campos

    def test_message_tem_campos_criticos(self):
        """Campos lidos do response Message no loop tool-use."""
        from anthropic.types import Message
        campos = set(Message.model_fields.keys())
        assert "content" in campos
        assert "stop_reason" in campos
        assert "usage" in campos

    def test_excecoes_basicas_existem(self):
        """gus/llm.py importa anthropic.APIStatusError, APIConnectionError,
        APITimeoutError. Se SDK renomear, import quebra no boot."""
        import anthropic
        assert hasattr(anthropic, "APIStatusError")
        assert hasattr(anthropic, "APIConnectionError")
        assert hasattr(anthropic, "APITimeoutError")
        assert hasattr(anthropic, "AsyncAnthropic")
