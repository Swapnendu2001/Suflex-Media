from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
async def get_homepage():
    # Import and run the script to generate dynamic blog content for home page
    import subprocess
    import sys

    try:
        # Run the generate_blog_sections.py script to update the HTML with dynamic content
        result = subprocess.run([sys.executable, "generate_blog_sections.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running generate_blog_sections.py: {result.stderr}")
    except Exception as e:
        print(f"Error running generate_blog_sections.py: {e}")

    return FileResponse("PAGE_SERVING_ROUTERS/PAGES/home.html")