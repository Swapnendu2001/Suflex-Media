from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/ghostwriting")
async def get_ghostwriting():
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/Book_writing.html")