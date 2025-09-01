from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from components.header import header_style, header_content
from components.footer import footer_style, footer_content
import uvicorn

app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    style = """
    <style>
        body {
            margin: 0;
            padding-top: 8vh;
            padding-bottom: 28vh;
        }
    </style>
    """
    return f"""
    <html>
        <head>
            <title>Suflex Media</title>
            {header_style()}
            {footer_style()}
            {style}
        </head>
        <body>
            {header_content()}
            {footer_content()}
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
