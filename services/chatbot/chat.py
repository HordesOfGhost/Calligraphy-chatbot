import os
from fastapi import Request, HTTPException
from services.authentication.auth import verify_token
from schemas.schemas import Message
from langchain_community.vectorstores import FAISS
from .config import gemini_model, embeddings_model, calligraphy_data
from .prompt import system_prompt 

texts = [doc["content"] for doc in calligraphy_data]

vectorstore = FAISS.from_texts(texts, embeddings_model)

# Simple in-memory chat history store (dictionary keyed by user/session ID)
chat_histories = {}

def retrieve_relevant_docs(query, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.invoke(query)
    return results

def build_prompt(query, user_id):
    # Retrieve relevant docs
    relevant_docs = retrieve_relevant_docs(query)
    context_text = "\n---\n".join([doc.page_content for doc in relevant_docs])

    # Get chat history for user (list of strings)
    history = chat_histories.get(user_id, [])
    # prompt = "You are a helpful assistant. Refrain from saying things out of context. Use the following context to answer:\n"
    # Build the prompt: system/context + history + user query
    prompt = system_prompt + context_text + "\n\n"

    if history:
        prompt += "Chat history:\n" + "\n".join(history) + "\n"

    prompt += f"User: {query}\nAssistant:"

    return prompt

def chat_with_chatbot(message: Message, request: Request):
    verify_token(request)  # Validate Firebase token

    # Use some user ID from token or request to track chat (simplified here)
    user_id = request.headers.get("X-User-ID", "anonymous")

    try:
        prompt = build_prompt(message.prompt, user_id)

        response = gemini_model.generate_content(prompt)
        reply = response.text.strip()

        # Save interaction in chat history
        chat_histories.setdefault(user_id, []).append(f"User: {message.prompt}")
        chat_histories[user_id].append(f"Assistant: {reply}")

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
