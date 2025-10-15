from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/404")
async def get_404():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/404.html")