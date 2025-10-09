from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from templates.homepage import homepage
from templates.about import about
from templates.services import services
import uvicorn

app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return homepage()

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    return about()

@app.get("/services", response_class=HTMLResponse)
async def services_page():
    return services()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
