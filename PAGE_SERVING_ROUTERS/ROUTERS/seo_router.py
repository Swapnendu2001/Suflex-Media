from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/seo")
async def get_seo():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/SEO.html")