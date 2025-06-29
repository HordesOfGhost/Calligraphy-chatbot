from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from .config import templates

router = APIRouter()

@router.get("/login", response_class=HTMLResponse, tags=['auth'])
async def login_page(request: Request):
    """
    Render the login page template.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        HTMLResponse: The rendered login.html template response.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse, tags=['auth'])
async def register_page(request: Request):
    """
    Render the registration page template.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        HTMLResponse: The rendered register.html template response.
    """
    return templates.TemplateResponse("register.html", {"request": request})