from langchain_groq import ChatGroq
from app.config.settings import settings

def get_llm():
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please run 'locally set-key <YOUR_API_KEY>' to configure it globally.")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=settings.GROQ_API_KEY,
        temperature=0.2,
        max_retries=2
    )
