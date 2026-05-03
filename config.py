"""Centraliza todas as configurações via variáveis de ambiente."""

import os
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY: str = os.environ.get("OPEN_ROUTER", "")

DEFAULT_MODEL: str = "google/gemini-2.0-flash-001"
MAX_TOKENS: int = 4096
