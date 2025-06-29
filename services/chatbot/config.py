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

# Load data
calligraphy_data = []
json_path = "knowledge_base/calligraphy_content.json"
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        calligraphy_data = json.load(f)
else:
    print(f"Warning: {json_path} does not exist. Starting with empty calligraphy_data.")
