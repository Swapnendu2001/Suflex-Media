from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/admin")
async def get_admin_homepage():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/admin_homepage.html")