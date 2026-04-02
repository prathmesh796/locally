from langchain_groq import ChatGroq
from config.settings import settings

def get_llm():
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables. Please create a .env file and set GROQ_API_KEY.")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=settings.GROQ_API_KEY,
        temperature=0.2,
        max_retries=2
    )
