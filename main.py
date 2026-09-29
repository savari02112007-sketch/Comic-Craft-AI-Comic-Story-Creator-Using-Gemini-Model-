from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


# --------------------------------
# APP
# --------------------------------

app = FastAPI(title="AI Comic Craft")


# --------------------------------
# GENERATED IMAGES FOLDER
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
GENERATED_IMAGES = BASE_DIR / "generated_images"

GENERATED_IMAGES.mkdir(parents=True, exist_ok=True)


# --------------------------------
# rom fastapi.staticfiles import StaticFiles
# --------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GENERATED_IMAGES = BASE_DIR / "generated_images"

GENERATED_IMAGES.mkdir(parents=True, exist_ok=True)

app.mount(
    "/generated_images",
    StaticFiles(directory=str(GENERATED_IMAGES)),
    name="generated_images"
)

# --------------------------------
# ROUTES
# --------------------------------

app.include_router(router)


# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "AI Comic Craft is running"
    }