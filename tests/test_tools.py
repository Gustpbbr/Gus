"""Testes de funções utilitárias em gus/tools.py.

Foco em validações puras (path, sensível). Tools que fazem HTTP ficam pra
testes de integração separados.
"""

import pytest
from gus.tools import _validar_path, _escanear_sensivel


class TestValidarPath:
    def test_path_simples_ok(self):
        assert _validar_path("pessoal/saude/exame.md") == "pessoal/saude/exame.md"

    def test_remove_barra_inicial(self):
        assert _validar_path("/dimagem/dia/2026-04-30.md") == "dimagem/dia/2026-04-30.md"

    def test_aceita_pasta_hidden(self):
        assert _validar_path(".github/workflows/test.yml") == ".github/workflows/test.yml"

    def test_aceita_underscore_e_hifen(self):
        assert _validar_path("_indices/auditoria-mem0.md") == "_indices/auditoria-mem0.md"

    def test_traversal_rejeitado(self):
        with pytest.raises(ValueError, match="traversal"):
            _validar_path("../../../etc/passwd")

    def test_traversal_no_meio_rejeitado(self):
        with pytest.raises(ValueError, match="traversal"):
            _validar_path("pessoal/../../etc/passwd")

    def test_caracteres_perigosos_rejeitados(self):
        with pytest.raises(ValueError, match="caracteres"):
            _validar_path("pessoal/saude/file;rm -rf.md")

    def test_espacos_rejeitados(self):
        with pytest.raises(ValueError, match="caracteres"):
            _validar_path("pessoal saude/exame.md")

    def test_caracteres_unicode_rejeitados(self):
        with pytest.raises(ValueError, match="caracteres"):
            _validar_path("pessoal/saúde/exame.md")


class TestEscanearSensivel:
    def test_delegado_a_patterns_sensiveis(self):
        assert _escanear_sensivel("oi mundo") == []

    def test_detecta_cpf(self):
        assert "CPF" in _escanear_sensivel("CPF 111.222.333-44")

    def test_detecta_chave_anthropic(self):
        chave = "sk-ant-api03-" + "X" * 30
        assert "API key Anthropic" in _escanear_sensivel(chave)


class TestDispararWorkflowRegex:
    """Regex que valida nome de workflow no dispatcher."""

    def test_regex_aceita_yml(self):
        import re
        regex = r"^[a-z0-9\-]+\.ya?ml$"
        assert re.match(regex, "briefing-matinal.yml")
        assert re.match(regex, "auditoria-mem0.yaml")

    def test_regex_rejeita_uppercase(self):
        import re
        regex = r"^[a-z0-9\-]+\.ya?ml$"
        assert not re.match(regex, "Briefing-Matinal.yml")

    def test_regex_rejeita_traversal(self):
        import re
        regex = r"^[a-z0-9\-]+\.ya?ml$"
        assert not re.match(regex, "../../etc/passwd.yml")

    def test_regex_rejeita_subpath(self):
        import re
        regex = r"^[a-z0-9\-]+\.ya?ml$"
        assert not re.match(regex, "subdir/file.yml")
