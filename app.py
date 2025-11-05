from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import uvicorn
from contextlib import asynccontextmanager

from DATABASE_HANDLER import initialize_database
from PAGE_SERVING_ROUTERS.ROUTERS.homepage_router import router as homepage_router
from PAGE_SERVING_ROUTERS.ROUTERS.about_router import router as about_router
from PAGE_SERVING_ROUTERS.ROUTERS.contact_router import router as contact_router
from PAGE_SERVING_ROUTERS.ROUTERS.portfolio_router import router as portfolio_router
from PAGE_SERVING_ROUTERS.ROUTERS.blogs_router import router as blogs_router
from PAGE_SERVING_ROUTERS.ROUTERS.error_router import router as error_router
from PAGE_SERVING_ROUTERS.ROUTERS.login_router import router as login_router
from PAGE_SERVING_ROUTERS.ROUTERS.admin_homepage_router import router as admin_homepage_router
from PAGE_SERVING_ROUTERS.ROUTERS.admin_users_router import router as admin_users_router
from PAGE_SERVING_ROUTERS.ROUTERS.admin_blogs_router import router as admin_blogs_router
from PAGE_SERVING_ROUTERS.ROUTERS.Blog_Creator_router import router as blog_creator_router
from PAGE_SERVING_ROUTERS.ROUTERS.ghostwriting_router import router as ghostwriting_router
from PAGE_SERVING_ROUTERS.ROUTERS.linkedin_branding_router import router as linkedin_branding_router
from PAGE_SERVING_ROUTERS.ROUTERS.content_writing_router import router as content_writing_router
from PAGE_SERVING_ROUTERS.ROUTERS.performance_marketing_router import router as performance_marketing_router
from PAGE_SERVING_ROUTERS.ROUTERS.website_development_router import router as website_development_router
from PAGE_SERVING_ROUTERS.ROUTERS.seo_router import router as seo_router
from API_ROUTERS.login_api_router import router as login_api_router
from API_ROUTERS.admin_users_api_router import router as admin_users_api_router
from API_ROUTERS.serve_images_api_router import router as serve_images_api_router
from API_ROUTERS.blogs_api_router import router as blogs_api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await initialize_database()
    print("Database initialized successfully!")
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/css", StaticFiles(directory="PAGE_SERVING_ROUTERS/CSS"), name="css")
app.mount("/icons", StaticFiles(directory="PAGE_SERVING_ROUTERS/ICONS"), name="icons")
app.mount("/images", StaticFiles(directory="PAGE_SERVING_ROUTERS/IMAGES"), name="images")
app.mount("/js", StaticFiles(directory="PAGE_SERVING_ROUTERS/JS"), name="js")
app.mount("/pages", StaticFiles(directory="PAGE_SERVING_ROUTERS/PAGES"), name="pages")
app.mount("/fonts", StaticFiles(directory="PAGE_SERVING_ROUTERS/FONTS"), name="fonts")

app.include_router(homepage_router)
app.include_router(about_router)
app.include_router(contact_router)
app.include_router(portfolio_router)
app.include_router(blogs_router)
app.include_router(error_router)
app.include_router(login_router)
app.include_router(admin_homepage_router)
app.include_router(admin_users_router)
app.include_router(admin_blogs_router)
app.include_router(blog_creator_router)
app.include_router(ghostwriting_router)
app.include_router(linkedin_branding_router)
app.include_router(content_writing_router)
app.include_router(performance_marketing_router)
app.include_router(website_development_router)
app.include_router(seo_router)
app.include_router(login_api_router)
app.include_router(admin_users_api_router)
app.include_router(serve_images_api_router)
app.include_router(blogs_api_router)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/404.html", status_code=404)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
