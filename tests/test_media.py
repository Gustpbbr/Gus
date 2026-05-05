"""Testes do cache de mídia em gus/media.py — byte budget + count limit."""

import importlib

import gus.media as media


def _reset_cache():
    """Zera o cache global entre testes."""
    media._media_cache.clear()
    media._media_cache_bytes = 0
    media._audio_cache.clear()


def _content_pdf_fake(size_bytes: int) -> list[dict]:
    """Cria content fake pra cache. base64 = 4/3 do binário, então
    pra simular size_bytes reais geramos len(b64) = 4/3 * size_bytes."""
    b64_len = (size_bytes * 4) // 3
    return [{
        "type": "document",
        "source": {"type": "base64", "media_type": "application/pdf", "data": "X" * b64_len}
    }]


class TestContentBytes:
    def test_calcula_bytes_de_base64(self):
        _reset_cache()
        content = _content_pdf_fake(1000)  # 1KB
        size = media._content_bytes(content)
        # Tolerância de ±2 bytes pela divisão inteira
        assert abs(size - 1000) < 5

    def test_inclui_texto(self):
        _reset_cache()
        content = [{"type": "text", "text": "olá mundo"}]
        size = media._content_bytes(content)
        assert size == len("olá mundo".encode("utf-8"))

    def test_lista_vazia(self):
        assert media._content_bytes([]) == 0

    def test_blocos_invalidos_ignorados(self):
        assert media._content_bytes([None, "string", 42]) == 0


class TestCachePutCount:
    def test_cache_normal_armazena(self):
        _reset_cache()
        content = _content_pdf_fake(100)
        media._cache_put("hash1", content)
        assert media._cache_get("hash1") == content

    def test_count_limit_50(self):
        _reset_cache()
        # 51 itens pequenos → ejeta o primeiro
        for i in range(51):
            media._cache_put(f"hash{i}", _content_pdf_fake(100))
        assert "hash0" not in media._media_cache
        assert "hash50" in media._media_cache
        assert len(media._media_cache) == 50

    def test_count_ejecao_em_ordem_de_insercao(self):
        _reset_cache()
        # Adiciona até count_max + 3
        for i in range(media._CACHE_MAX_ITEMS + 3):
            media._cache_put(f"k{i}", _content_pdf_fake(100))
        # Os 3 mais antigos devem ter saído
        for i in range(3):
            assert f"k{i}" not in media._media_cache
        for i in range(3, media._CACHE_MAX_ITEMS + 3):
            assert f"k{i}" in media._media_cache


class TestCachePutBytes:
    def test_byte_budget_ejeta_quando_excede(self):
        _reset_cache()
        # 4 itens de 60MB cada = 240MB > limite 200MB
        # Primeiro deve ser ejetado pra caber o quarto
        big = 60 * 1024 * 1024  # 60MB
        for i in range(4):
            media._cache_put(f"big{i}", _content_pdf_fake(big))

        # big0 ejetado pra caber big3
        assert "big0" not in media._media_cache
        assert "big3" in media._media_cache
        # Total bytes <= limite
        assert media._media_cache_bytes <= media._CACHE_MAX_BYTES

    def test_bytes_decrementa_no_ejecao(self):
        _reset_cache()
        # Item grande (1000 bytes) + count limit force ejeta ele
        media._cache_put("a", _content_pdf_fake(1000))

        # Força ejeção: enche count_max+1 com itens pequenos
        for i in range(media._CACHE_MAX_ITEMS + 1):
            media._cache_put(f"k{i}", _content_pdf_fake(100))

        # 'a' foi ejetado, decrementando soma de bytes
        assert "a" not in media._media_cache
        # Soma reflete só os items presentes (50 items × ~100 bytes = ~5000),
        # NÃO inclui mais os 1000 do 'a'
        assert media._media_cache_bytes < 6000  # tolerância pra arredondamento
        assert media._media_cache_bytes > 0
        # Conta == count atual
        assert len(media._media_cache) == media._CACHE_MAX_ITEMS

    def test_item_unico_grande_aceito(self):
        _reset_cache()
        # PDF max do projeto é 32MB; 100MB é teste extremo.
        # Cache aceita mesmo se único item exceder budget — só ele cabe.
        huge = 100 * 1024 * 1024
        content = _content_pdf_fake(huge)
        media._cache_put("huge", content)
        assert "huge" in media._media_cache

    def test_item_consultado_apos_outros_ejetarem_ainda_existe(self):
        _reset_cache()
        media._cache_put("alvo", _content_pdf_fake(1000))
        # Adiciona mais 49 (total 50, dentro do limite)
        for i in range(49):
            media._cache_put(f"f{i}", _content_pdf_fake(100))
        # alvo (mais antigo) ainda está
        assert media._cache_get("alvo") is not None
        # 50º item entra → alvo ejetado
        media._cache_put("novo", _content_pdf_fake(100))
        assert media._cache_get("alvo") is None
        assert media._cache_get("novo") is not None


class TestCacheGet:
    def test_hit_retorna_content(self):
        _reset_cache()
        content = _content_pdf_fake(100)
        media._cache_put("h", content)
        assert media._cache_get("h") == content

    def test_miss_retorna_none(self):
        _reset_cache()
        assert media._cache_get("inexistente") is None
