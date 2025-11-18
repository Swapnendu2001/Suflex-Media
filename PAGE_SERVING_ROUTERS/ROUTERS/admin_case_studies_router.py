from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/admin/case-studies")
async def get_admin_case_studies_page():
    """
    Serve the admin case studies management page
    """
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/admin_case_studies.html")