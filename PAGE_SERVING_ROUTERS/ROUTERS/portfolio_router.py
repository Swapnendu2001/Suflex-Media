from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/portfolio")
async def get_portfolio():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/portfolio.html")