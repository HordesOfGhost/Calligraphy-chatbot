from fastapi import APIRouter
from services.scrape.scraper import get_or_scrape_data

router = APIRouter()

@router.on_event("startup")
async def on_startup():
    """
    Run initialization tasks on application startup.
    """
    get_or_scrape_data()

    