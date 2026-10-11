"""
Configuração central do CYMAG Enterprise.

Lê tudo de variáveis de ambiente (carregadas de um `.env` na raiz do projeto
quando presente). Mantém segredos fora do código-fonte.
"""

import os
import secrets
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv é opcional em runtime
    pass

# BASE_DIR = raiz do projeto (um nível acima do pacote app/)
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)


def _bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


class Config:
    # ─── Ambiente ────────────────────────────────────────────────────────────
    # development | test | demo | staging | production. Controla fail-closed:
    # produção/staging NÃO semeiam dados demo e EXIGEM segredos fortes.
    ENV = os.environ.get("CYMAG_ENV", "development").strip().lower()

    # ─── Segurança / sessão ──────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("CYMAG_SECRET_KEY", "").strip()

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Em produção o cookie de sessão deve viajar só por HTTPS, salvo override explícito.
    SESSION_COOKIE_SECURE = _bool("CYMAG_COOKIE_SECURE", ENV in ("production", "staging"))
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("CYMAG_SESSION_HOURS", "12")) * 3600

    @classmethod
    def is_production_like(cls) -> bool:
        return cls.ENV in ("production", "staging")

    @classmethod
    def seeding_allowed(cls) -> bool:
        """Massa de demonstração só em ambientes não-produtivos."""
        return cls.ENV in ("development", "test", "demo")

    # ─── Banco de dados ────────────────────────────────────────────────────────
    DB_PATH = os.environ.get("CYMAG_DB_PATH", "").strip() or str(INSTANCE_DIR / "cymag.db")

    # ─── IA (Groq / AEGIS) ──────────────────────────────────────────────────────
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
    AEGIS_MODEL = os.environ.get("CYMAG_AEGIS_MODEL", "llama-3.3-70b-versatile")
    # Onde o painel admin persiste a chave configurada em runtime (fica em
    # instance/, que é gitignored — nunca vai para o repositório).
    AI_CONFIG_PATH = str(INSTANCE_DIR / "ai_config.json")

    # ─── Servidor ────────────────────────────────────────────────────────────────
    HOST = os.environ.get("CYMAG_HOST", "127.0.0.1").strip()
    PORT = int(os.environ.get("CYMAG_PORT", "5000"))

    # ─── Bootstrap admin ─────────────────────────────────────────────────────────
    ADMIN_EMAIL = os.environ.get("CYMAG_ADMIN_EMAIL", "admin@cymag.com").strip().lower()
    ADMIN_PASSWORD = os.environ.get("CYMAG_ADMIN_PASSWORD", "").strip()

    @classmethod
    def resolve_secret_key(cls) -> str:
        """Devolve a SECRET_KEY. Em produção/staging é OBRIGATÓRIA e forte (fail-closed);
        em dev/test/demo, gera e persiste uma automaticamente por conveniência."""
        if cls.is_production_like():
            if len(cls.SECRET_KEY) < 32:
                raise RuntimeError(
                    "CYMAG_SECRET_KEY ausente ou fraca em ambiente "
                    f"'{cls.ENV}': defina uma chave forte (>=32 chars). "
                    "Gere com: python -c \"import secrets; print(secrets.token_hex(32))\""
                )
            return cls.SECRET_KEY
        if cls.SECRET_KEY:
            return cls.SECRET_KEY
        key_file = INSTANCE_DIR / ".secret_key"
        try:
            if key_file.exists():
                return key_file.read_text().strip()
            key = secrets.token_hex(32)
            key_file.write_text(key)
            return key
        except OSError:
            return secrets.token_hex(32)


config = Config()
