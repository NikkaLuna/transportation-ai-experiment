import os
from dotenv import load_dotenv

# Load .env file FIRST
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.0