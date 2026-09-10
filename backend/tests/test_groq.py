import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY was not found in .env")

client = Groq(api_key=api_key)

models = client.models.list()

print("Groq API connection: OK")
print("\nAvailable models:")

for model in models.data:
    print("-", model.id)