import os
import json
from fastapi import Request, HTTPException
from auth import verify_token
from schemas import Message
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from embedding import HFMiniLMEmbeddings
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
hf_token = os.getenv("HF_TOKEN")

model = genai.GenerativeModel("gemini-2.0-flash")

# Load scraped data and build vectorstore on app startup
with open("scraped_data/calligraphy_content.json", "r", encoding="utf-8") as f:
    docs = json.load(f)
texts = [doc["content"] for doc in docs]

embeddings = HFMiniLMEmbeddings(hf_token)
vectorstore = FAISS.from_texts(texts, embeddings)

# Simple in-memory chat history store (dictionary keyed by user/session ID)
chat_histories = {}

def retrieve_relevant_docs(query, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)
    return results

def build_prompt(query, user_id):
    # Retrieve relevant docs
    relevant_docs = retrieve_relevant_docs(query)
    context_text = "\n---\n".join([doc.page_content for doc in relevant_docs])

    # Get chat history for user (list of strings)
    history = chat_histories.get(user_id, [])

    # Build the prompt: system/context + history + user query
    prompt = "You are a helpful assistant. Use the following context to answer:\n"
    prompt += context_text + "\n\n"

    if history:
        prompt += "Chat history:\n" + "\n".join(history) + "\n"

    prompt += f"User: {query}\nAssistant:"

    return prompt

def chat_with_gpt(message: Message, request: Request):
    verify_token(request)  # Validate Firebase token

    # Use some user ID from token or request to track chat (simplified here)
    user_id = request.headers.get("X-User-ID", "anonymous")

    try:
        prompt = build_prompt(message.prompt, user_id)

        response = model.generate_content(prompt)
        reply = response.text.strip()

        # Save interaction in chat history
        chat_histories.setdefault(user_id, []).append(f"User: {message.prompt}")
        chat_histories[user_id].append(f"Assistant: {reply}")

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
