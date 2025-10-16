from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/admin/blogs")
async def get_admin_blogs_page():
    """
    Serve the admin blogs management page
    """
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/admin_blogs.html")