from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/landing_page")
async def get_landing_page():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/landing_page.html")