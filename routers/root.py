from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root_redirect():
    # Redirect root to login page
    return HTMLResponse(status_code=307, headers={"Location": "/login"})
