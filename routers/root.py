from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root_redirect():
    """
    Handle requests to the root URL '/' by redirecting the client to the '/login' page.

    Returns:
        HTMLResponse: An HTTP 307 Temporary Redirect response with 'Location' header set to '/login'.
    """
    return HTMLResponse(status_code=307, headers={"Location": "/login"})
