from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/admin/users")
async def get_admin_users_page():
    """
    Serve the admin users management page
    """
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/admin_users.html")