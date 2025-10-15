from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/about")
async def get_about():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/about_us.html")