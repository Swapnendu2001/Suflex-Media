from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="PAGE_SERVING_ROUTERS/PAGES")

@router.get("/landing_page", response_class=HTMLResponse)
async def get_landing_page(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})