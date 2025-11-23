from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from typing import Dict

from DATABASE_HANDLER.utils.generate_blog_sections import get_blogs_html, get_home_insights_html

router = APIRouter()

STATIC_PAGES: Dict[str, str] = {
    "/about": "PAGE_SERVING_ROUTERS/PAGES/about_us.html",
    "/content-writing": "PAGE_SERVING_ROUTERS/PAGES/Content_writing.html",
    "/ghostwriting": "PAGE_SERVING_ROUTERS/PAGES/Book_writing.html",
    "/landing": "PAGE_SERVING_ROUTERS/PAGES/landing_page.html",
    "/linkedin-branding": "PAGE_SERVING_ROUTERS/PAGES/LinkedIn_branding.html",
    "/performance-marketing": "PAGE_SERVING_ROUTERS/PAGES/Performance_marketing.html",
    "/portfolio": "PAGE_SERVING_ROUTERS/PAGES/portfolio.html",
    "/seo": "PAGE_SERVING_ROUTERS/PAGES/SEO.html",
    "/website-development": "PAGE_SERVING_ROUTERS/PAGES/Website_development.html",
    "/contact": "PAGE_SERVING_ROUTERS/PAGES/contact_us.html",
    "/cancellation-and-refund-policy": "PAGE_SERVING_ROUTERS/PAGES/cancellation_and_refund_policy.html",
    "/terms-of-service": "PAGE_SERVING_ROUTERS/PAGES/terms_of_service.html",
    "/privacy-policy": "PAGE_SERVING_ROUTERS/PAGES/privacy_policy.html",
}

def create_page_route(route_path: str, html_file: str):
    """
    Factory function to create a static page route handler
    
    Args:
        route_path: The URL path for the route
        html_file: The file path to the HTML file to serve
        
    Returns:
        Async function that returns FileResponse
    """
    async def page_handler():
        return FileResponse(html_file)
    return page_handler



for route_path, html_file in STATIC_PAGES.items():
    router.add_api_route(
        route_path,
        create_page_route(route_path, html_file),
        methods=["GET"],
        name=f"serve_{route_path.replace('/', '_').strip('_')}_page"
    )

@router.get("/", response_class=HTMLResponse)
async def get_homepage():
    _, _, _, top_editors_choice_data = await get_blogs_html()
    home_insights_html = await get_home_insights_html(top_editors_choice_data)

    with open("PAGE_SERVING_ROUTERS/PAGES/home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    print(home_insights_html)
    html_content = html_content.replace(
        '<!-- TOP EDITOR\'S CHOICE BLOGS WILL BE INSERTED HERE DYNAMICALLY -->',
        home_insights_html
    )

    return HTMLResponse(content=html_content)