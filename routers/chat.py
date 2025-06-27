from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from .config import templates
from schemas.schemas import Message
from services.authentication.auth import verify_token
from services.chatbot.chat import chat_with_chatbot

router = APIRouter()

@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat")
async def chat_endpoint(message: Message, request: Request):
    verify_token(request)
    return chat_with_chatbot(message, request)