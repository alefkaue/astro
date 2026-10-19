"""Testes da configuração/runtime do AEGIS (sem acesso à rede)."""

import json

from app.ai.aegis import Aegis, GROQ_BASE_URL, _friendly_error, _mask_key


def test_mask_key_hides_secret():
    assert _mask_key("") == ""
    assert _mask_key("short") == "••••"
    masked = _mask_key("gsk_abcd1234efgh")
    assert masked.startswith("gsk_") and masked.endswith("efgh")
    assert "1234" not in masked  # miolo escondido


def test_friendly_error_maps_401():
    assert "401" in _friendly_error(Exception("Error code: 401 - invalid api key"))
    assert "Modelo" in _friendly_error(Exception("model `x` does not exist"))
    assert "429" in _friendly_error(Exception("429 rate limit reached"))


def test_status_offline_by_default(tmp_path):
    a = Aegis()
    a.init("", "llama-3.3-70b-versatile", str(tmp_path / "ai.json"))
    s = a.status()
    assert s["online"] is False
    assert s["source"] == "none"
    assert s["base_url"] == GROQ_BASE_URL
    assert s["key_mask"] == ""
    assert "llama-3.3-70b-versatile" in s["known_models"]


def test_test_key_requires_key():
    a = Aegis()
    r = a.test_key("")
    assert r["ok"] is False and "chave" in r["error"].lower()


def test_init_prefers_env_over_saved(tmp_path):
    cfg = tmp_path / "ai.json"
    cfg.write_text('{"api_key": "gsk_saved", "model": "m", "base_url": "' + GROQ_BASE_URL + '"}')
    a = Aegis()
    a.init("gsk_fromenv", "llama-3.3-70b-versatile", str(cfg))
    assert a.status()["source"] == "env"


def test_init_uses_saved_when_env_absent(tmp_path):
    cfg = tmp_path / "ai.json"
    cfg.write_text('{"api_key": "gsk_saved12345", "model": "m", "base_url": "' + GROQ_BASE_URL + '"}')
    a = Aegis()
    a.init("", "llama-3.3-70b-versatile", str(cfg))
    s = a.status()
    assert s["source"] == "runtime"
    assert s["online"] is True
    assert s["key_mask"].endswith("2345")


# ─── Testes de criptografia em repouso (A11) ────────────────────────────────

_SECRET = "test_secret_key_cymag_a11_32bytes"


def test_encrypted_save_no_plaintext_in_file(tmp_path):
    """Chave não aparece em texto puro no arquivo quando secret_key está presente."""
    pytest_skip_if_no_crypto = False
    try:
        from cryptography.fernet import Fernet  # noqa: F401
    except ImportError:
        pytest_skip_if_no_crypto = True

    if pytest_skip_if_no_crypto:
        return  # cryptography não instalado — fallback plaintext é aceitável

    cfg = tmp_path / "ai.json"
    a = Aegis()
    a.init("", "llama-3.3-70b-versatile", str(cfg), secret_key=_SECRET)
    a._save("gsk_super_secret_9999", "m", GROQ_BASE_URL)

    raw = cfg.read_text(encoding="utf-8")
    assert "gsk_super_secret_9999" not in raw, "Chave em texto puro no arquivo!"
    data = json.loads(raw)
    assert "api_key_enc" in data
    assert "api_key" not in data


def test_encrypted_round_trip(tmp_path):
    """Chave cifrada é recuperada corretamente por outra instância com a mesma secret_key."""
    try:
        from cryptography.fernet import Fernet  # noqa: F401
    except ImportError:
        return

    cfg = tmp_path / "ai.json"
    # Salvar com cifração
    writer = Aegis()
    writer.init("", "llama-3.3-70b-versatile", str(cfg), secret_key=_SECRET)
    writer._save("gsk_round_trip_12345", "m", GROQ_BASE_URL)

    # Ler com a mesma chave
    reader = Aegis()
    reader.init("", "llama-3.3-70b-versatile", str(cfg), secret_key=_SECRET)
    assert reader.status()["source"] == "runtime"
    assert reader.status()["online"] is True
    assert reader.status()["key_mask"].endswith("2345")


def test_wrong_secret_key_goes_offline(tmp_path):
    """Instância com secret_key diferente não consegue ler a chave cifrada."""
    try:
        from cryptography.fernet import Fernet  # noqa: F401
    except ImportError:
        return

    cfg = tmp_path / "ai.json"
    writer = Aegis()
    writer.init("", "llama-3.3-70b-versatile", str(cfg), secret_key=_SECRET)
    writer._save("gsk_round_trip_12345", "m", GROQ_BASE_URL)

    # Ler com chave diferente → deve ficar offline
    reader = Aegis()
    reader.init("", "llama-3.3-70b-versatile", str(cfg), secret_key="wrong_secret_key_other")
    assert reader.status()["online"] is False
    assert reader.status()["source"] == "none"


def test_legacy_plaintext_still_loads(tmp_path):
    """Arquivo legado com api_key em texto puro continua sendo lido."""
    cfg = tmp_path / "ai.json"
    cfg.write_text(
        json.dumps({"api_key": "gsk_legacy_plaintext_0000", "model": "m", "base_url": GROQ_BASE_URL}),
        encoding="utf-8",
    )
    a = Aegis()
    a.init("", "llama-3.3-70b-versatile", str(cfg), secret_key=_SECRET)
    # Legado sem api_key_enc → lido como plaintext mesmo com Fernet disponível
    assert a.status()["source"] == "runtime"
    assert a.status()["online"] is True
    assert a.status()["key_mask"].endswith("0000")
