from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/website-development")
async def get_website_development():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/Website_development.html")