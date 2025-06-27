from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.authentication.auth import verify_token
from services.chatbot import chat_with_chatbot
from schemas.schemas import Message
from services.scrape.scraper import get_or_scrape_data

# Load or scrape content
scraped_docs = get_or_scrape_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates") 

@app.get("/", response_class=HTMLResponse)
async def root_redirect():
    # Redirect root to login page
    return HTMLResponse(status_code=307, headers={"Location": "/login"})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# **This must exist** for your frontend POST to work:
@app.post("/chat")
async def chat_endpoint(message: Message, request: Request):
    verify_token(request)
    return chat_with_chatbot(message, request)
