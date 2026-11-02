from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
STORE_DIR = DATA_DIR / "store"
CHUNK_STORE_PATH = STORE_DIR / "chunks.json"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 1
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"


def load_settings() -> str:
    """Load environment variables and return the API key."""
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. Add it to the .env file in the project root."
        )
    return api_key
