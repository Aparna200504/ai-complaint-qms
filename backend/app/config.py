import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_EXTRACTION_MODEL = os.getenv(
    "GROQ_EXTRACTION_MODEL",
    "openai/gpt-oss-20b",
)
GROQ_REASONING_MODEL = os.getenv(
    "GROQ_REASONING_MODEL",
    "openai/gpt-oss-120b",
)


if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured.")

if not GROQ_EXTRACTION_MODEL:
    raise RuntimeError("GROQ_EXTRACTION_MODEL is not configured.")

if not GROQ_REASONING_MODEL:
    raise RuntimeError("GROQ_REASONING_MODEL is not configured.")

