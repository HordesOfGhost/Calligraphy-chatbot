from .embedding import HFMiniLMEmbeddings
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
load_dotenv()


# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Hugging Face API Key
hf_token = os.getenv("HF_TOKEN")

# Models
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
embeddings_model = HFMiniLMEmbeddings(hf_token)

# Load scraped data and build vectorstore on app startup
with open("knowledge_base/calligraphy_content.json", "r", encoding="utf-8") as f:
    calligraphy_data = json.load(f)

