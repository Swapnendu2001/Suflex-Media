from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/login")
async def get_login():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/login.html")