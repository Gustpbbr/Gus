"""Testes do curador (hub/curador.py) — extração JSON, validação, hashing."""

import pytest
from hub.curador import (
    _extrair_json, _validar_fragmento, _hash_janela,
    _texto_de_message, _serializar_trecho,
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
