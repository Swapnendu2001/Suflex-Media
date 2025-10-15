from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/test_blog")
async def get_test_blog():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/Blog_sample.html")