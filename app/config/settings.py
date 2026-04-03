import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
