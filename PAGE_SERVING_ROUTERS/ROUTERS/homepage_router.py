from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
async def get_homepage():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/home.html")