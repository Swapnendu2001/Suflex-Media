from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from generate_blog_sections import get_blogs_html # Import the new function

load_dotenv()

router = APIRouter()

@router.get("/blogs", response_class=HTMLResponse)
async def get_blogs(request: Request):
    # Get dynamic blog content
    latest_gossips_html, editors_choice_html, _ = await get_blogs_html()

    # Read the original HTML file
    with open("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace the placeholders with dynamic content
    html_content = html_content.replace(
        '<div id="dynamic-latest-gossips-content"></div>',
        latest_gossips_html
    )
    html_content = html_content.replace(
        '<div id="dynamic-editors-choice-content"></div>',
        editors_choice_html
    )

    return HTMLResponse(content=html_content)