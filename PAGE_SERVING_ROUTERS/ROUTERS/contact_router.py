from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/contact")
async def get_contact():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/contact_us.html")