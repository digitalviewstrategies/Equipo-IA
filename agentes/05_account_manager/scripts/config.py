"""Variables de entorno centralizadas."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

WABA_TOKEN = os.getenv("WABA_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")
WABA_ID = os.getenv("WABA_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
APP_SECRET = os.getenv("APP_SECRET", "")

FELIPE_WA_NUMBER = os.getenv("FELIPE_WA_NUMBER", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
INTENT_MODEL = os.getenv("INTENT_MODEL", "claude-haiku-4-5-20251001")
DRAFT_MODEL = os.getenv("DRAFT_MODEL", "claude-sonnet-4-6")

OUTPUTS_DIR = ROOT / "outputs"
CONTEXT_DIR = ROOT / "context"
TEMPLATES_DIR = ROOT / "templates"
BRANDS_DIR = ROOT.parent.parent / "shared" / "brands"
