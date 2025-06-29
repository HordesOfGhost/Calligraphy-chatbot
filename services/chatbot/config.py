from .embedding import HFMiniLMEmbeddings
from dotenv import load_dotenv
import os
import google.generativeai as genai
from services.scrape.scraper import get_or_scrape_data

load_dotenv()


# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Hugging Face API Key
hf_token = os.getenv("HF_TOKEN")

# Models
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
embeddings_model = HFMiniLMEmbeddings(hf_token)

# Load data
calligraphy_data = get_or_scrape_data()    
