import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set.")

CHROMA_DB_PATH = "chroma_db"

TEMP_FOLDER = "temp"

os.makedirs(TEMP_FOLDER, exist_ok=True)