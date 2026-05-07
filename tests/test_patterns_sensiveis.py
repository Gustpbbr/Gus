"""Testes da fonte única de patterns sensíveis (gus/patterns_sensiveis.py).

Os strings deste arquivo são fixtures sintéticas pra validar deteção. Hook
scan_sensivel está com `tests/` em ALLOW_PREFIXES.
"""

from gus.patterns_sensiveis import PATTERNS_SENSIVEIS, escanear, redact


class TestEscanear:
    def test_texto_limpo_retorna_lista_vazia(self):
        assert escanear("oi tudo bem com voce hoje?") == []

    def test_detecta_cpf_formatado(self):
        assert "CPF" in escanear("meu CPF é 123.456.789-00")

    def test_detecta_cpf_sem_pontuacao(self):
        assert "CPF" in escanear("CPF 12345678900")

    def test_detecta_cnpj(self):
        assert "CNPJ" in escanear("CNPJ 12.345.678/0001-90")

    def test_detecta_anthropic_key(self):
        chave = "sk-ant-api03-" + "X" * 30
        assert "API key Anthropic" in escanear(f"key: {chave}")

    def test_detecta_openai_key(self):
        chave = "sk-" + "A" * 50
        assert "API key OpenAI" in escanear(chave)

    def test_detecta_github_pat_classic(self):
        assert "GitHub PAT" in escanear("ghp_" + "x" * 30)

    def test_detecta_github_pat_finegrained(self):
        assert "GitHub PAT" in escanear("github_pat_" + "x" * 30)

    def test_detecta_telegram_bot_token(self):
        token = "1234567890:" + "X" * 35
        assert "Telegram bot token" in escanear(token)

    def test_detecta_google_pem(self):
        pem = "-----BEGIN PRIVATE KEY-----\nMII...\n-----END PRIVATE KEY-----"
        assert "Google service account key" in escanear(pem)

    def test_detecta_google_oauth_client_secret(self):
        assert "Google OAuth client secret" in escanear("GOCSPX-" + "x" * 25)

    def test_detecta_railway_token_env_line(self):
        linha = "RAILWAY_API_TOKEN=abc123def456ghi789jkl012"
        assert "Railway token (env line)" in escanear(linha)

    def test_multiplos_patterns_no_mesmo_texto(self):
        texto = (
            "CPF 111.222.333-44 e API key sk-" + "X" * 50 +
            " token ghp_" + "y" * 30
        )
        encontrados = set(escanear(texto))
        assert "CPF" in encontrados
        assert "API key OpenAI" in encontrados
        assert "GitHub PAT" in encontrados


class TestRedact:
    def test_texto_limpo_inalterado(self):
        texto, redatados = redact("oi mundo")
        assert texto == "oi mundo"
        assert redatados == []

    def test_redige_cpf(self):
        texto, redatados = redact("CPF 123.456.789-00 fim")
        assert "[REDACTED-CPF]" in texto
        assert "123.456.789-00" not in texto
        assert redatados == ["CPF"]

    def test_redige_multiplas_ocorrencias_mesmo_tipo(self):
        texto, redatados = redact("CPF 111.222.333-44 e CPF 555.666.777-88")
        assert texto.count("[REDACTED-CPF]") == 2
        assert redatados.count("CPF") == 2

    def test_redige_tipos_diferentes(self):
        chave = "sk-" + "A" * 50
        texto, redatados = redact(f"CPF 123.456.789-00 key {chave}")
        assert "[REDACTED-CPF]" in texto
        assert "[REDACTED-API-key-OpenAI]" in texto
        assert set(redatados) == {"CPF", "API key OpenAI"}

    def test_marcador_substitui_espaco_por_traco(self):
        texto, _ = redact("1234567890:" + "X" * 35)
        assert "[REDACTED-Telegram-bot-token]" in texto


class TestPatternsRegex:
    def test_todos_patterns_sao_compilados(self):
        import re
        for nome, padrao in PATTERNS_SENSIVEIS.items():
            assert isinstance(padrao, re.Pattern), f"{nome} não é compilado"

    def test_lista_nao_vazia(self):
        assert len(PATTERNS_SENSIVEIS) >= 10
