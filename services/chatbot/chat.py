from fastapi import Request, HTTPException
from schemas.schemas import Message
from langchain_community.vectorstores import FAISS
from services.authentication.auth import verify_token
from .config import gemini_model, embeddings_model, calligraphy_data
from .prompt import system_prompt 

texts = [doc["content"] for doc in calligraphy_data]

vectorstore = FAISS.from_texts(texts, embeddings_model)

# Simple in-memory chat history store (dictionary keyed by user/session ID)
chat_histories = {}

def retrieve_relevant_docs(query, k=3):
    """
    Retrieve top-k most relevant documents from the vector store for a given query.

    Args:
        query (str): The user query to search for.
        k (int): Number of top relevant documents to retrieve.

    Returns:
        List of documents ranked by relevance.
    """

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.invoke(query)
    return results

def build_prompt(query, user_id):
    """
    Build the full prompt for the language model using system instructions, relevant context, and chat history.

    Args:
        query (str): The current user query.
        user_id (str): Unique identifier for the user (used to retrieve chat history).

    Returns:
        str: The constructed prompt string for the language model.
    """

    # Retrieve relevant docs
    relevant_docs = retrieve_relevant_docs(query)
    context_text = "\n---\n".join([doc.page_content for doc in relevant_docs])

    # Get chat history for user (list of strings)
    history = chat_histories.get(user_id, [])
    
    prompt = system_prompt + context_text + "\n\n"

    if history:
        prompt += "Chat history:\n" + "\n".join(history) + "\n"

    prompt += f"User: {query}\nAssistant:"

    return prompt

def chat_with_chatbot(message: Message, request: Request):
    """
    Handle a chat interaction with the chatbot.

    This function:
    - Verifies Firebase authentication
    - Builds a prompt based on chat history and relevant documents
    - Sends the prompt to the Gemini model
    - Stores the exchange in chat history

    Args:
        message (Message): The input message from the user.
        request (Request): The FastAPI request object containing headers and auth info.

    Returns:
        dict: A dictionary containing the assistant's reply.

    Raises:
        HTTPException: If token verification fails or an internal error occurs.
    """
    
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
