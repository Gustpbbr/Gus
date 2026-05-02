"""Testes do logger de custo/tokens (gus/logger.py)."""

import json
import importlib
from datetime import datetime, timedelta


def _reload_logger(monkeypatch, log_dir):
    """LOG_DIR é avaliado no import — recarrega o módulo após setar env."""
    monkeypatch.setenv("LOG_DIR", str(log_dir))
    import gus.logger
    importlib.reload(gus.logger)
    return gus.logger


class TestRegistrar:
    def test_cria_arquivo_jsonl(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        logger.registrar(direction="out", cost_usd=0.001, tokens_in=10, tokens_out=5)
        assert logger.LOG_FILE.exists()

    def test_uma_linha_por_entrada(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        logger.registrar(direction="out", cost_usd=0.001)
        logger.registrar(direction="out", cost_usd=0.002)
        linhas = logger.LOG_FILE.read_text().strip().split("\n")
        assert len(linhas) == 2

    def test_jsonl_valido(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        logger.registrar(direction="out", cost_usd=0.001, model="claude-sonnet-4-6")
        entry = json.loads(logger.LOG_FILE.read_text().strip())
        assert entry["direction"] == "out"
        assert entry["cost_usd"] == 0.001
        assert entry["model"] == "claude-sonnet-4-6"
        assert "timestamp" in entry


class TestStatsMesAtual:
    def test_arquivo_inexistente_retorna_zerado(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        if logger.LOG_FILE.exists():
            logger.LOG_FILE.unlink()
        s = logger.stats_mes_atual()
        assert s["cost_usd"] == 0.0
        assert s["tokens_in"] == 0
        assert s["calls"] == 0

    def test_agrega_apenas_mes_corrente(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        agora = datetime.now()
        logger.LOG_FILE.write_text(
            json.dumps({
                "timestamp": agora.isoformat(),
                "cost_usd": 0.5,
                "tokens_in": 100,
                "tokens_out": 50,
                "cache_creation": 0,
                "cache_read": 0,
            }) + "\n" +
            json.dumps({
                "timestamp": (agora - timedelta(days=70)).isoformat(),
                "cost_usd": 99.9,
                "tokens_in": 99999,
                "tokens_out": 99999,
                "cache_creation": 0,
                "cache_read": 0,
            }) + "\n"
        )
        s = logger.stats_mes_atual()
        assert s["cost_usd"] == 0.5
        assert s["tokens_in"] == 100
        assert s["tokens_out"] == 50
        assert s["calls"] == 1

    def test_soma_multiplas_entradas(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        agora = datetime.now()
        linhas = []
        for i in range(3):
            linhas.append(json.dumps({
                "timestamp": agora.isoformat(),
                "cost_usd": 0.1,
                "tokens_in": 100,
                "tokens_out": 50,
                "cache_creation": 10,
                "cache_read": 20,
            }))
        logger.LOG_FILE.write_text("\n".join(linhas) + "\n")
        s = logger.stats_mes_atual()
        assert abs(s["cost_usd"] - 0.3) < 1e-9
        assert s["tokens_in"] == 300
        assert s["cache_read"] == 60
        assert s["calls"] == 3

    def test_linha_corrompida_nao_quebra(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        agora = datetime.now()
        logger.LOG_FILE.write_text(
            json.dumps({"timestamp": agora.isoformat(), "cost_usd": 0.1}) + "\n" +
            "lixo nao json\n" +
            json.dumps({"timestamp": agora.isoformat(), "cost_usd": 0.2}) + "\n"
        )
        s = logger.stats_mes_atual()
        assert abs(s["cost_usd"] - 0.3) < 1e-9
        assert s["calls"] == 2

    def test_custo_mes_atual_retrocompat(self, tmp_log_dir, monkeypatch):
        logger = _reload_logger(monkeypatch, tmp_log_dir)
        agora = datetime.now()
        logger.LOG_FILE.write_text(
            json.dumps({"timestamp": agora.isoformat(), "cost_usd": 1.5}) + "\n"
        )
        assert logger.custo_mes_atual() == 1.5
