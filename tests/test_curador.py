"""Testes do curador (hub/curador.py) — extração JSON, validação, hashing."""

import pytest
from hub.curador import (
    _extrair_json, _validar_fragmento, _hash_janela,
    _texto_de_message, _serializar_trecho,
    _render_prompt, PROMPT_CURADOR, PROMPT_CURADOR_ARQUIVO,
    TIPOS_VALIDOS, CAMADAS_VALIDAS, AREAS_VALIDAS,
)


class TestExtrairJson:
    def test_array_direto(self):
        out = _extrair_json('[{"conteudo": "x", "tipo": "fato"}]')
        assert len(out) == 1
        assert out[0]["conteudo"] == "x"

    def test_array_vazio(self):
        assert _extrair_json("[]") == []

    def test_string_vazia(self):
        assert _extrair_json("") == []

    def test_none(self):
        assert _extrair_json(None) == []

    def test_com_cerca_markdown(self):
        texto = '```json\n[{"conteudo": "y"}]\n```'
        out = _extrair_json(texto)
        assert out == [{"conteudo": "y"}]

    def test_com_cerca_sem_lang(self):
        texto = '```\n[{"conteudo": "z"}]\n```'
        out = _extrair_json(texto)
        assert out == [{"conteudo": "z"}]

    def test_texto_antes_e_depois_via_regex(self):
        texto = 'Aqui está: [{"conteudo": "y"}] espero que ajude'
        out = _extrair_json(texto)
        assert len(out) == 1
        assert out[0]["conteudo"] == "y"

    def test_json_invalido_retorna_vazio(self):
        assert _extrair_json("não é JSON {") == []

    def test_objeto_solo_em_vez_de_array(self):
        # _extrair_json espera array — objeto solto não é lista
        assert _extrair_json('{"conteudo": "x"}') == []

    def test_array_complexo_multilinha(self):
        texto = '''[
            {"conteudo": "primeiro", "tipo": "fato"},
            {"conteudo": "segundo", "tipo": "decisao"}
        ]'''
        out = _extrair_json(texto)
        assert len(out) == 2


class TestValidarFragmento:
    def test_valido_com_todos_campos(self):
        f = _validar_fragmento({
            "conteudo": "Gustavo prefere crítica direta",
            "tipo": "preferencia",
            "camada_temporal": "permanente",
            "area": "gus",
            "confianca": 0.9,
        })
        assert f is not None
        assert f["conteudo"] == "Gustavo prefere crítica direta"
        assert f["tipo"] == "preferencia"
        assert f["confianca"] == 0.9

    def test_aplica_defaults(self):
        f = _validar_fragmento({"conteudo": "fato auto-suficiente aqui"})
        assert f["tipo"] == "episodico"
        assert f["camada_temporal"] == "sessao"
        assert f["area"] == ""
        assert f["confianca"] == 0.7

    def test_descarta_conteudo_vazio(self):
        assert _validar_fragmento({"conteudo": ""}) is None
        assert _validar_fragmento({"conteudo": "   "}) is None

    def test_descarta_conteudo_curto(self):
        # Mínimo 10 chars
        assert _validar_fragmento({"conteudo": "curto"}) is None

    def test_descarta_nao_dict(self):
        assert _validar_fragmento(None) is None
        assert _validar_fragmento("string") is None
        assert _validar_fragmento(["lista"]) is None

    def test_descarta_sem_conteudo(self):
        assert _validar_fragmento({"tipo": "fato"}) is None

    def test_strip_aplicado(self):
        f = _validar_fragmento({"conteudo": "  texto com espaços  "})
        assert f["conteudo"] == "texto com espaços"


class TestHashJanela:
    def test_hash_deterministico(self):
        a = _hash_janela("trecho de teste")
        b = _hash_janela("trecho de teste")
        assert a == b

    def test_hash_muda_com_input(self):
        a = _hash_janela("um")
        b = _hash_janela("dois")
        assert a != b

    def test_hash_tem_8_chars(self):
        h = _hash_janela("qualquer texto")
        assert len(h) == 8


class TestTextoDeMessage:
    def test_user_str(self):
        out = _texto_de_message({"role": "user", "content": "oi"})
        assert out == "Gustavo: oi"

    def test_assistant_str(self):
        out = _texto_de_message({"role": "assistant", "content": "olá"})
        assert out == "Gus: olá"

    def test_user_lista_blocos_text(self):
        msg = {"role": "user", "content": [
            {"type": "text", "text": "primeiro"},
            {"type": "text", "text": "segundo"},
        ]}
        out = _texto_de_message(msg)
        assert "primeiro" in out
        assert "segundo" in out

    def test_user_lista_sem_text(self):
        msg = {"role": "user", "content": [
            {"type": "image", "source": {}},
        ]}
        out = _texto_de_message(msg)
        assert "[mídia]" in out

    def test_content_none_ou_vazio(self):
        out = _texto_de_message({"role": "user", "content": None})
        assert "Gustavo:" in out


class TestSerializarTrecho:
    def test_serializa_lista(self):
        msgs = [
            {"role": "user", "content": "pergunta"},
            {"role": "assistant", "content": "resposta"},
        ]
        out = _serializar_trecho(msgs)
        assert "Gustavo: pergunta" in out
        assert "Gus: resposta" in out

    def test_lista_vazia(self):
        assert _serializar_trecho([]) == ""


class TestRenderPrompt:
    """Regressão do bug crítico do PR #72.

    str.format() interpretava { } literais do JSON example dentro dos
    templates como placeholders (`{`'\\n    "conteudo"'`}`), gerando
    KeyError em toda chamada do curador. Hub ficou vazio ≥3 dias.
    Fix: replace() em vez de format(). Estes testes garantem que o
    bug não regride.
    """

    def test_substitui_via_e_conversa(self):
        out = _render_prompt(PROMPT_CURADOR, via="telegram-claude", input_texto="oi")
        assert "telegram-claude" in out
        assert "{via}" not in out
        assert "{conversa}" not in out

    def test_substitui_via_e_conteudo_no_template_arquivo(self):
        # PROMPT_CURADOR_ARQUIVO usa {conteudo} (não {conversa})
        out = _render_prompt(PROMPT_CURADOR_ARQUIVO, via="claude-chat", input_texto="texto")
        assert "claude-chat" in out
        assert "texto" in out
        assert "{conteudo}" not in out
        assert "{via}" not in out

    def test_preserva_chaves_json_literais_curador(self):
        """O coração da regressão: { } do exemplo JSON sobrevivem."""
        out = _render_prompt(PROMPT_CURADOR, via="x", input_texto="y")
        # JSON example tem `{` antes de "conteudo" — não pode sumir
        assert '"conteudo"' in out
        assert '"tipo"' in out
        assert '"confianca"' in out
        # Estrutura JSON visível pro modelo
        assert "[\n  {" in out or "[\n    {" in out or "[" in out

    def test_preserva_chaves_json_literais_arquivo(self):
        out = _render_prompt(PROMPT_CURADOR_ARQUIVO, via="x", input_texto="y")
        assert '"conteudo"' in out
        assert '"tipo"' in out

    def test_input_com_chaves_nao_explode(self):
        """Bug original: input do user com { } não pode quebrar o render.
        Replace é literal, não interpreta — diferente de format()."""
        # Mensagem que SIMULA o bug: usuário copia JSON na conversa
        input_problematico = '{"key": "value"}'
        out = _render_prompt(PROMPT_CURADOR, via="x", input_texto=input_problematico)
        assert input_problematico in out  # passou inteiro

    def test_format_regresion_sentinel(self):
        """Sentinel: se alguém trocar replace() de volta pra format() no
        _render_prompt, este teste falha. Usa um template mínimo que
        reproduz o KeyError exato do bug original."""
        # Template real do projeto contém JSON example com `{` `"conteudo"` `}`
        # — replace() é seguro, format() crashava com:
        #   KeyError: '\n    "conteudo"'
        # Aqui só validamos que a função NÃO levanta exceção.
        try:
            _render_prompt(PROMPT_CURADOR, via="t", input_texto="trecho")
            _render_prompt(PROMPT_CURADOR_ARQUIVO, via="t", input_texto="arquivo")
        except KeyError as e:  # pragma: no cover
            pytest.fail(f"Regressão do bug do format(): KeyError {e!r}")
        except Exception as e:  # pragma: no cover
            pytest.fail(f"Render quebrou inesperadamente: {type(e).__name__}: {e}")


class TestEnumsCanonicos:
    """Os enums gus-18 são contrato — fragmentos com valores fora viram
    default (PR #72). Testa que o conjunto canônico está intacto."""

    def test_tipos_validos_contem_canon_gus18(self):
        # 14 tipos do schema gus-18
        canon = {
            "identidade_operacional", "biografico", "emocional", "decisao",
            "procedural", "rotina", "meta_reflexao", "conexao_emergente",
            "episodico", "cronologico", "fato", "preferencia", "lacuna", "projeto",
        }
        assert canon == TIPOS_VALIDOS

    def test_camadas_validas_canon_gus18(self):
        canon = {"momento", "sessao", "semana", "rotina", "permanente"}
        assert canon == CAMADAS_VALIDAS

    def test_areas_validas_canon_gus18(self):
        canon = {
            "gus", "saude", "financeiro", "projetos", "pessoal",
            "dimagem", "pesquisa", "receitas", "esportes",
        }
        assert canon == AREAS_VALIDAS


class TestValidarFragmentoEnums:
    """Validação contra enums (PR #72) — modelo às vezes inventa
    `tipo: "reflexivo"` ou `area: "vida"`. Validador troca por default
    e loga warn em vez de poluir vocabulário do Hub."""

    def test_tipo_invalido_vira_episodico(self, caplog):
        import logging
        caplog.set_level(logging.WARNING)
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "tipo": "reflexivo",  # inventado pelo modelo
        })
        assert f["tipo"] == "episodico"
        assert any("tipo inválido" in r.message for r in caplog.records)

    def test_camada_invalida_vira_sessao(self, caplog):
        import logging
        caplog.set_level(logging.WARNING)
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "camada_temporal": "eterno",
        })
        assert f["camada_temporal"] == "sessao"
        assert any("camada inválida" in r.message for r in caplog.records)

    def test_area_invalida_vira_string_vazia(self, caplog):
        import logging
        caplog.set_level(logging.WARNING)
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "area": "vida",
        })
        assert f["area"] == ""
        assert any("area inválida" in r.message for r in caplog.records)

    def test_confianca_acima_1_vira_clamp(self):
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "confianca": 1.5,
        })
        assert f["confianca"] == 1.0

    def test_confianca_abaixo_0_vira_clamp(self):
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "confianca": -0.3,
        })
        assert f["confianca"] == 0.0

    def test_confianca_string_vira_default(self):
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "confianca": "alta",  # modelo inventa string
        })
        assert f["confianca"] == 0.7  # default

    def test_confianca_none_vira_default(self):
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "confianca": None,
        })
        assert f["confianca"] == 0.7

    def test_tipo_camada_area_simultaneamente_invalidos(self, caplog):
        import logging
        caplog.set_level(logging.WARNING)
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "tipo": "estranho",
            "camada_temporal": "instantaneo",
            "area": "vida",
            "confianca": 99.0,
        })
        assert f["tipo"] == "episodico"
        assert f["camada_temporal"] == "sessao"
        assert f["area"] == ""
        assert f["confianca"] == 1.0
        # 3 warns (tipo, camada, area)
        warns = [r for r in caplog.records if r.levelname == "WARNING"]
        assert len(warns) >= 3

    def test_area_vazia_nao_loga_warn(self, caplog):
        import logging
        caplog.set_level(logging.WARNING)
        # area="" é OK — só não loga warn (vazio é default explícito)
        f = _validar_fragmento({
            "conteudo": "fragmento auto-suficiente legível",
            "area": "",
        })
        assert f["area"] == ""
        warns = [r for r in caplog.records if "area" in r.message]
        assert len(warns) == 0

