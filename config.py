import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Chroma Database
CHROMA_DB_PATH = "chroma_db"

# Temporary folder for downloaded files
TEMP_FOLDER = "temp"

# Create temp folder if it doesn't exist
os.makedirs(TEMP_FOLDER, exist_ok=True)