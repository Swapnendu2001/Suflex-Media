from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/blogs")
async def get_blogs():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html")