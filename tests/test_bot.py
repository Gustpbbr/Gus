"""Testes de funções utilitárias e de estado do bot (gus/bot.py).

Não testa handlers Telegram diretamente (precisaria mockar Update/Context).
Foca em: state load/save, validação, queries, regex de fluxo Dimagem.
"""

import json
import importlib
import time
from collections import deque

import pytest


def _reload_bot(monkeypatch, state_path):
    """STATE_FILE é avaliado no import — recarrega após setar.

    Como gus.bot agora só re-exporta gus.state (split M1 do plano de
    saneamento), recarregamos state PRIMEIRO pra constantes pegarem env
    novas, depois bot pra re-exports apontarem pros símbolos atualizados.
    """
    monkeypatch.setenv("STATE_FILE", str(state_path))
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    import gus.state
    importlib.reload(gus.state)
    import gus.handlers.responder
    importlib.reload(gus.handlers.responder)
    import gus.handlers.commands
    importlib.reload(gus.handlers.commands)
    import gus.bot
    importlib.reload(gus.bot)
    return gus.bot


class TestLoadSaveState:
    def test_round_trip(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        # popula state em memória
        bot.conversation_histories["12345"] = [
            {"role": "user", "content": "oi"},
            {"role": "assistant", "content": "olá"},
        ]
        bot.turn_counters["12345"] = 5
        bot.last_saved_turn["12345"] = 3
        bot.message_timestamps["12345"] = deque([time.time(), time.time()])
        bot.dimagem_pending["12345"] = {"path": "x.md"}

        bot._save_state()
        assert tmp_state_file.exists()

        # zera memória, recarrega
        bot.conversation_histories.clear()
        bot.turn_counters.clear()
        bot.last_saved_turn.clear()
        bot.message_timestamps.clear()
        bot.dimagem_pending.clear()

        bot._load_state()
        assert bot.conversation_histories["12345"][0]["content"] == "oi"
        assert bot.turn_counters["12345"] == 5
        assert bot.last_saved_turn["12345"] == 3
        assert len(bot.message_timestamps["12345"]) == 2
        assert bot.dimagem_pending["12345"]["path"] == "x.md"

    def test_load_arquivo_inexistente_silencioso(self, tmp_path, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_path / "nao-existe.json")
        # Não deve levantar
        bot._load_state()
        assert bot.conversation_histories == {}

    def test_save_atomico_via_tmp(self, tmp_state_file, monkeypatch):
        """Garante que o save usa write tmp + replace (não corrompe se kill mid-write)."""
        bot = _reload_bot(monkeypatch, tmp_state_file)
        bot.conversation_histories["1"] = [{"role": "user", "content": "x"}]
        bot._save_state()

        # arquivo final existe; tmp não deve sobrar
        assert tmp_state_file.exists()
        assert not (tmp_state_file.parent / (tmp_state_file.name + ".tmp")).exists()

    def test_save_silent_on_error(self, tmp_path, monkeypatch):
        # Path inválido (diretório sem permissão simulado por path absurdo)
        invalid = tmp_path / "subdir" / "file.json"
        bot = _reload_bot(monkeypatch, invalid)
        bot.conversation_histories["1"] = [{"role": "user", "content": "x"}]
        # Mesmo se o save falhar, não deve propagar
        bot._save_state()


class TestAutorizado:
    def test_chat_id_correto(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        assert bot._autorizado("12345") is True

    def test_chat_id_diferente(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        assert bot._autorizado("99999") is False

    def test_sem_telegram_chat_id_nega_tudo(self, tmp_state_file, monkeypatch):
        monkeypatch.setenv("STATE_FILE", str(tmp_state_file))
        monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "")
        # Recarrega state (fonte real das env vars) E bot (re-export)
        import gus.state
        importlib.reload(gus.state)
        import gus.bot
        importlib.reload(gus.bot)
        assert gus.bot._autorizado("12345") is False
        assert gus.bot._autorizado("") is False


class TestTextoDeContent:
    def test_string_direta(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        assert bot._texto_de_content("oi mundo") == "oi mundo"

    def test_lista_blocos_text(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        content = [
            {"type": "text", "text": "primeiro"},
            {"type": "text", "text": "segundo"},
        ]
        out = bot._texto_de_content(content)
        assert "primeiro" in out
        assert "segundo" in out

    def test_lista_sem_text_blocks(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        content = [{"type": "image", "source": {}}]
        assert bot._texto_de_content(content) == ""

    def test_outros_tipos(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        assert bot._texto_de_content(None) == ""
        assert bot._texto_de_content(42) == ""


class TestQueryMem0Contextual:
    def test_pega_ultimas_3_user(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        history = [
            {"role": "user", "content": "antiga"},
            {"role": "user", "content": "primeira"},
            {"role": "assistant", "content": "resp"},
            {"role": "user", "content": "segunda"},
            {"role": "user", "content": "terceira"},
        ]
        out = bot._query_mem0_contextual(history, "fallback")
        # Pega as 3 últimas user msgs (primeira, segunda, terceira)
        assert "primeira" in out
        assert "segunda" in out
        assert "terceira" in out
        assert "antiga" not in out  # passou do limite de 3

    def test_history_vazio_usa_fallback(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        out = bot._query_mem0_contextual([], "fallback msg")
        assert out == "fallback msg"

    def test_so_assistant_usa_fallback(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        history = [{"role": "assistant", "content": "resp"}]
        out = bot._query_mem0_contextual(history, "fallback")
        assert out == "fallback"


class TestLimparFocosAntigos:
    """M7 — /foco deleta FOCO-ATUAL existentes antes de salvar novo."""

    @pytest.mark.asyncio
    async def test_deleta_apenas_com_marker(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        # Mock retorna 3 fragmentos: 2 com [FOCO-ATUAL], 1 sem (relacionado mas não é foco)
        from unittest.mock import patch, MagicMock
        fake_lembrar = MagicMock(return_value=[
            {"id": "id1", "conteudo": "[FOCO-ATUAL] phronesis"},
            {"id": "id2", "conteudo": "Gustavo gosta de foco profundo"},  # filtrado
            {"id": "id3", "conteudo": "[FOCO-ATUAL] mge"},
        ])
        deletados = []
        fake_deletar = MagicMock(side_effect=lambda mid, motivo: deletados.append((mid, motivo)))

        with patch("hub.store.lembrar", fake_lembrar):
            with patch("hub.store.deletar", fake_deletar):
                count = await bot._limpar_focos_antigos()

        assert count == 2
        assert ("id1", "/foco substituicao") in deletados
        assert ("id3", "/foco substituicao") in deletados
        # id2 não tem marker — não deleta
        assert "id2" not in [d[0] for d in deletados]

    @pytest.mark.asyncio
    async def test_lembrar_falha_retorna_zero(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        from unittest.mock import patch, MagicMock
        fake_lembrar = MagicMock(side_effect=RuntimeError("Hub down"))

        with patch("hub.store.lembrar", fake_lembrar):
            count = await bot._limpar_focos_antigos()
        assert count == 0

    @pytest.mark.asyncio
    async def test_deletar_falha_continua(self, tmp_state_file, monkeypatch):
        """Se deletar falha em 1 fragmento, segue tentando os outros."""
        bot = _reload_bot(monkeypatch, tmp_state_file)
        from unittest.mock import patch, MagicMock
        fake_lembrar = MagicMock(return_value=[
            {"id": "id1", "conteudo": "[FOCO-ATUAL] a"},
            {"id": "id2", "conteudo": "[FOCO-ATUAL] b"},
        ])

        chamadas = []
        def fake_deletar(mid, motivo):
            chamadas.append(mid)
            if mid == "id1":
                raise RuntimeError("oops")

        with patch("hub.store.lembrar", fake_lembrar):
            with patch("hub.store.deletar", side_effect=fake_deletar):
                count = await bot._limpar_focos_antigos()

        # id1 falhou, id2 OK — count = 1
        assert count == 1
        assert chamadas == ["id1", "id2"]

    @pytest.mark.asyncio
    async def test_lista_vazia(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        from unittest.mock import patch, MagicMock
        with patch("hub.store.lembrar", MagicMock(return_value=[])):
            count = await bot._limpar_focos_antigos()
        assert count == 0


class TestDimagemImportPath:
    """C7 — dimagem.py movido pra gus/integrations/."""

    def test_dimagem_importa_de_integrations(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        # Se import quebrou, _reload_bot já teria explodido. Confirma path.
        import gus.integrations.dimagem as d
        assert hasattr(d, "analisar_os_dimagem")
        assert hasattr(d, "salvar_os_dimagem")


class TestRedigirResposta:
    def test_resposta_limpa_inalterada(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        out, redatados = bot._redigir_resposta("oi mundo, tudo bem?")
        assert out == "oi mundo, tudo bem?"
        assert redatados == []

    def test_redige_cpf_no_output(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        out, redatados = bot._redigir_resposta(
            "O paciente João tem CPF 111.222.333-44 e foi atendido."
        )
        assert "[REDACTED-CPF]" in out
        assert "111.222.333-44" not in out
        assert "CPF" in redatados

    def test_anexa_nota_visivel_quando_redige(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        out, _ = bot._redigir_resposta("CPF 111.222.333-44")
        assert "redatado" in out
        assert "CPF" in out

    def test_nao_anexa_nota_quando_limpo(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        out, _ = bot._redigir_resposta("texto normal sem dados")
        assert "redatado" not in out

    def test_resposta_vazia(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        assert bot._redigir_resposta("") == ("", [])
        assert bot._redigir_resposta(None) == (None, [])

    def test_multiplos_tipos_aparecem_na_nota(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        chave = "sk-" + "A" * 50
        out, redatados = bot._redigir_resposta(
            f"CPF 123.456.789-00 e key {chave}"
        )
        # Nota lista os tipos únicos em ordem alfabética
        assert "API key OpenAI" in out
        assert "CPF" in out
        assert set(redatados) == {"CPF", "API key OpenAI"}


class TestRegexDimagem:
    def test_confirma_sim(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        for s in ["sim", "Sim!", "ok", "OK", "pode", "manda", "vai", "bora", "1", "👍", "salva"]:
            assert bot._DIMAGEM_CONFIRMA_RE.match(s), f"falha em '{s}'"

    def test_confirma_nao_match_random(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        for s in ["talvez", "depois eu vejo", "olha aquilo", "qualquer coisa"]:
            assert not bot._DIMAGEM_CONFIRMA_RE.match(s), f"falsamente matched '{s}'"

    def test_cancela(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        for s in ["não", "nao", "Cancela", "ignora", "esquece", "deixa pra lá", "aborta"]:
            assert bot._DIMAGEM_CANCELA_RE.match(s), f"falha em '{s}'"

    def test_cancela_nao_match_confirma(self, tmp_state_file, monkeypatch):
        bot = _reload_bot(monkeypatch, tmp_state_file)
        # confirmações não devem matchar cancela
        for s in ["sim", "ok", "pode"]:
            assert not bot._DIMAGEM_CANCELA_RE.match(s)
