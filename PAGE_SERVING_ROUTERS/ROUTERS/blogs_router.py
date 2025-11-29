from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from DATABASE_HANDLER.utils import get_blogs_html

load_dotenv()

router = APIRouter()

@router.get("/blogs", response_class=HTMLResponse)
async def get_blogs(request: Request):
    editors_choice_html, latest_gossips_html, read_more_html, _ = await get_blogs_html()

    with open("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.replace(
        '<div class="blogs-grid" id="editors-choice-grid"></div>',
        f'<div class="blogs-grid" id="editors-choice-grid">{editors_choice_html}</div>'
    )
    html_content = html_content.replace(
        '<div class="blogs-grid" id="latest-gossip-grid"></div>',
        f'<div class="blogs-grid" id="latest-gossip-grid">{latest_gossips_html}</div>'
    )
    html_content = html_content.replace(
        '<div class="blogs-grid" id="read-more-grid"></div>',
        f'<div class="blogs-grid" id="read-more-grid">{read_more_html}</div>'
    )

    return HTMLResponse(content=html_content)