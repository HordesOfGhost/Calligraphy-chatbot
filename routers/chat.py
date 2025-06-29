from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from .config import templates
from schemas.schemas import Message
from services.authentication.auth import verify_token
from services.chatbot.chat import chat_with_chatbot

router = APIRouter()

@router.get("/chat", response_class=HTMLResponse, tags=['chat'])
async def chat_page(request: Request):
    """
    Render the chatbot UI page (index.html).

    Args:
        request (Request): FastAPI request object, needed by the template.

    Returns:
        HTMLResponse: The rendered HTML page.
    """
    
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat", tags=['chat'])
async def chat_endpoint(message: Message, request: Request):
    """
    Handle user input from the chatbot form/API.

    - Verifies Firebase token from the request.
    - Passes user input to the chat model and returns the generated reply.

    Args:
        message (Message): User's message sent from the frontend.
        request (Request): The incoming request with headers (including auth).

    Returns:
        dict: A dictionary with the assistant's reply (JSON).
    """
    verify_token(request)
    return chat_with_chatbot(message, request)