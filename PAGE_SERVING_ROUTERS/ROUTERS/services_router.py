from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/services")
async def get_services():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/services.html")