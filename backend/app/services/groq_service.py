from groq import Groq

from app.config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

