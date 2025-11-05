from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/content-writing")
async def get_content_writing():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/Content_writing.html")