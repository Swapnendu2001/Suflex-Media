from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from templates.homepage import homepage
from templates.about import about
from templates.services import services
from templates.contact import contact
from templates.portfolio import portfolio
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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
