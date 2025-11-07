from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/linkedin-branding")
async def get_linkedin_branding():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/LinkedIn_branding.html")