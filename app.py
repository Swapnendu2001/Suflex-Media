from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from templates.homepage import homepage
from templates.about import about
from templates.services import services
from templates.contact import contact
from templates.portfolio import portfolio
from templates.blogs import blogs
import uvicorn

# Import admin routes
from admin_routes import router as admin_router

from data.db_handler_async import initialize_database

app = FastAPI()

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    print("Initializing database...")
    await initialize_database()
    print("Database initialized successfully!")

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include admin routes
app.include_router(admin_router, tags=["admin"])

@app.get("/", response_class=HTMLResponse)
async def root():
    return homepage()

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    return about()

@app.get("/services", response_class=HTMLResponse)
async def services_page():
    return services()

@app.get("/contact", response_class=HTMLResponse)
async def contact_page():
    return contact()

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page():
    return portfolio()

@app.get("/blogs", response_class=HTMLResponse)
async def blogs_page():
    return blogs()

@app.get("/blog/{blog_id}", response_class=HTMLResponse)
async def display_blog(blog_id: str):
    """Display a single blog post"""
    from data.page_handler import get_blog_page
    
    blog_data = get_blog_page(blog_id)
    
    if blog_data.get('status') == "not_found":
        return HTMLResponse(content="<h1>Blog not found</h1>", status_code=404)
    
    if blog_data.get('status') == "error":
        return HTMLResponse(content="<h1>Error loading blog</h1>", status_code=500)
    
    if blog_data.get('status') == "redirect":
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            return RedirectResponse(url=redirect_url)
        else:
            return HTMLResponse(content="<h1>Blog not found</h1>", status_code=404)
    
    if blog_data.get("status") == "deleted":
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            return RedirectResponse(url=redirect_url)
        else:
            return HTMLResponse(content="<h1>Blog has been deleted</h1>", status_code=404)

    return blog_data['html']

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
