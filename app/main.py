from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
import os
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download")
async def download_video(url: str = Form(...), format: str = Form(...)):
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestaudio/best" if format == "mp3" else "bestvideo+bestaudio/best",
        "merge_output_format": format,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = format if format != "mp3" else "mp3"
            filename = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
            return FileResponse(path=filename, filename=info.get("title", video_id) + f".{ext}", media_type="application/octet-stream")
    except Exception as e:
        return HTMLResponse(f"<h3>Error downloading video: {str(e)}</h3>", status_code=500)
