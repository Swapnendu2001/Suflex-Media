from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/performance-marketing")
async def get_performance_marketing():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/Performance_marketing.html")