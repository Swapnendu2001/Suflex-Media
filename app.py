from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import uvicorn
from contextlib import asynccontextmanager

from DATABASE_HANDLER import initialize_database
from PAGE_SERVING_ROUTERS.ROUTERS.homepage_router import router as homepage_router
from PAGE_SERVING_ROUTERS.ROUTERS.about_router import router as about_router
from PAGE_SERVING_ROUTERS.ROUTERS.services_router import router as services_router
from PAGE_SERVING_ROUTERS.ROUTERS.contact_router import router as contact_router
from PAGE_SERVING_ROUTERS.ROUTERS.portfolio_router import router as portfolio_router
from PAGE_SERVING_ROUTERS.ROUTERS.blogs_router import router as blogs_router
from PAGE_SERVING_ROUTERS.ROUTERS.error_router import router as error_router

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

app.include_router(homepage_router)
app.include_router(about_router)
app.include_router(services_router)
app.include_router(contact_router)
app.include_router(portfolio_router)
app.include_router(blogs_router)
app.include_router(error_router)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/404.html", status_code=404)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
