from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncpg
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates")

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

@router.get("/blogs")
async def get_blogs(request: Request):
    # Import and run the script to generate dynamic blog content
    import subprocess
    import sys

    try:
        # Run the generate_blog_sections.py script to update the HTML with dynamic content
        result = subprocess.run([sys.executable, "generate_blog_sections.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running generate_blog_sections.py: {result.stderr}")
    except Exception as e:
        print(f"Error running generate_blog_sections.py: {e}")

    # Return the updated HTML file
    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html")