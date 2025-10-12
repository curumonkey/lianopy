import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="MyProject API")   # EDIT: project title

# Serve static assets bundled with the package
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def root():
    return {"message": "Hello from MyProject!"}   # EDIT: default response
# You can add more routes and logic as needed