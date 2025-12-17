from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.engine import analyze_file

app = FastAPI(title="ProofLayer")

# Allow browser access (required for hosted frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Root route to serve frontend
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = BASE_DIR / "static" / "index.html"
    return index_path.read_text(encoding="utf-8")

# Analysis endpoint
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    result = analyze_file(file.filename, content)
    return JSONResponse(result)
