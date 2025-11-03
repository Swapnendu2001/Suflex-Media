from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="PAGE_SERVING_ROUTERS/PAGES")

@router.get("/ghostwriting", response_class=HTMLResponse)
async def get_ghostwriting_page(request: Request):
    return templates.TemplateResponse("ghostwriting.html", {"request": request})