import os
from dotenv import load_dotenv

home_env = os.path.expanduser("~/.locally/.env")
if os.path.exists(home_env):
    load_dotenv(home_env)

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
