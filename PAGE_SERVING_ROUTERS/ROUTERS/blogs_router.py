from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import os
import re
from dotenv import load_dotenv
from DATABASE_HANDLER.utils import get_blogs_html

load_dotenv()

router = APIRouter()

@router.get("/blogs", response_class=HTMLResponse)
async def get_blogs(request: Request):
    editors_choice_html, latest_gossips_html, read_more_html, _, top_blog, editors_choice_mobile_html = await get_blogs_html()

    with open("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    if top_blog:
        dynamic_hero_section = f"""<section class="hero-section">
            <div class="hero-image-container">
                <img src="{top_blog.get('cover_image', '')}" alt="Blog post image">
            </div>
            <div class="hero-content">
                <div class="hero-meta">
                    <span class="hero-badge">{top_blog.get('category', 'News!')}</span>
                    <span class="hero-read-time">{top_blog.get('read_time')} mins read</span>
                </div>
                <h1 class="hero-title">{top_blog.get('title', '')}</h1>
                <p class="hero-summary">{top_blog.get('summary', '')}</p>
                <a href="/blog/{top_blog.get('slug', '#')}" class="hero-read-more">Read More &rarr;</a>
            </div>
        </section>"""
        html_content = re.sub(
            r'\s*<section class="hero-section">.*?</section>',
            dynamic_hero_section,
            html_content,
            count=1,
            flags=re.DOTALL
        )

    html_content = re.sub(
        r'(<div class="editors-choice-right" id="editors-choice-grid">)(.*?)(</div>)',
        f'\\1{editors_choice_html}\\3',
        html_content,
        flags=re.DOTALL
    )
    html_content = html_content.replace(
        '<div class="blogs-grid" id="latest-gossip-grid"></div>',
        f'<div class="blogs-grid" id="latest-gossip-grid">{latest_gossips_html}</div>'
    )
    html_content = html_content.replace(
        '<div class="blogs-grid" id="read-more-grid"></div>',
        f'<div class="blogs-grid" id="read-more-grid">{read_more_html}</div>'
    )
    html_content = html_content.replace(
        '<div class="blogs-grid" id="mobile-editors-choice-grid"></div>',
        f'<div class="blogs-grid" id="mobile-editors-choice-grid">{editors_choice_mobile_html}</div>'
    )

    return HTMLResponse(content=html_content)