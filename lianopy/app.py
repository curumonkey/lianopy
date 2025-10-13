import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import os
import hashlib
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import mimetypes
from PIL import Image

from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Config ---
STORAGE_ROOT = Path(os.environ.get("LIANOPY_STORAGE", "storage_root")).resolve()
THUMB_ROOT = Path(".thumbnails").resolve()
THUMB_SIZE = (256, 256)
PAGE_SIZE_DEFAULT = 20

app = FastAPI(title="MyProject API")   # EDIT: project title

# Serve static assets bundled with the package
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- Helpers ---
def ensure_root(path: Path) -> Path:
    """Prevent path traversal outside STORAGE_ROOT."""
    p = (STORAGE_ROOT / path).resolve()
    if not str(p).startswith(str(STORAGE_ROOT)):
        raise HTTPException(status_code=400, detail="Invalid path")
    return p

def thumb_path_for(file_path: Path) -> Path:
    """Generate a unique thumbnail path based on file path + mtime."""
    try:
        mtime = int(file_path.stat().st_mtime)
    except FileNotFoundError:
        mtime = 0
    h = hashlib.sha256(str(file_path).encode()).hexdigest()
    rel = file_path.relative_to(STORAGE_ROOT).parent
    outdir = THUMB_ROOT / rel
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir / f"{h}_{mtime}.jpg"

def ensure_thumbnail(file_path: Path) -> Optional[Path]:
    """Create or reuse thumbnail for images."""
    dst = thumb_path_for(file_path)
    if dst.exists():
        return dst
    try:
        with Image.open(file_path) as img:
            img.thumbnail(THUMB_SIZE)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(dst, "JPEG", quality=80)
        return dst
    except Exception:
        return None

# Path to your static folder
STATIC_DIR = Path(__file__).parent / "static"

# Mount the static directory so assets are served at /static/*
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- API ---
# @app.get("/")
# def root():
    # return {"status": "ok", "root": str(STORAGE_ROOT)}

# Redirect root (/) to /static/index.html
# Serve index.html directly at /
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/list")
def list_files(
    path: str = "",
    page: int = 1,
    page_size: int = PAGE_SIZE_DEFAULT,
    thumbnails: bool = True,
):
    base = ensure_root(Path(path))
    if not base.exists():
        raise HTTPException(status_code=404, detail="Path not found")

    if base.is_file():
        return {"items": [{"name": base.name, "is_dir": False}]}

    entries = sorted(base.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    total = len(entries)
    start = max(0, (page - 1) * page_size)
    end = min(total, start + page_size)
    page_entries = entries[start:end]

    items = []
    for p in page_entries:
        item = {
            "name": p.name,
            "is_dir": p.is_dir(),
            "size": p.stat().st_size if p.is_file() else None,
            "path": str(p.relative_to(STORAGE_ROOT)),
            "thumb": None,
        }
        if thumbnails and p.is_file():
            thumb = ensure_thumbnail(p)
            if thumb:
                item["thumb"] = f"/thumb/{thumb.relative_to(THUMB_ROOT)}"
        items.append(item)

    return {
        "path": str(base.relative_to(STORAGE_ROOT)) if base != STORAGE_ROOT else "",
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items,
    }

@app.get("/thumb/{rel_path:path}")
def serve_thumbnail(rel_path: str):
    p = (THUMB_ROOT / rel_path).resolve()
    if not str(p).startswith(str(THUMB_ROOT)) or not p.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(p, media_type="image/jpeg")

@app.get("/api/download")
def download_file(path: str):
    file_path = ensure_root(Path(path))
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=file_path.name)

@app.get("/api/open")
def open_file(path: str):
    file_path = ensure_root(Path(path))
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    mime, _ = mimetypes.guess_type(str(file_path))
    return FileResponse(file_path, media_type=mime or "application/octet-stream")

@app.post("/api/download-zip")
async def download_zip(paths: List[str]):
    import zipfile
    from tempfile import SpooledTemporaryFile

    temp = SpooledTemporaryFile(max_size=50 * 1024 * 1024)
    with zipfile.ZipFile(temp, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in paths:
            p = ensure_root(Path(rel))
            if p.exists() and p.is_file():
                zf.write(p, arcname=p.name)
    temp.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="selection.zip"'}
    return StreamingResponse(temp, media_type="application/zip", headers=headers)


@app.on_event("startup")
def startup():
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    THUMB_ROOT.mkdir(parents=True, exist_ok=True)
