from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from generate_blog_sections import get_blogs_html, get_home_insights_html

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_homepage():
    _, _, top_editors_choice_data = await get_blogs_html()
    home_insights_html = await get_home_insights_html(top_editors_choice_data)

    with open("PAGE_SERVING_ROUTERS/PAGES/home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    html_content = html_content.replace(
        '<!-- TOP EDITOR\'S CHOICE BLOGS WILL BE INSERTED HERE DYNAMICALLY -->',
        home_insights_html
    )

    return HTMLResponse(content=html_content)