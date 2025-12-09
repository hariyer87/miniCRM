import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
from app.api.routes import api_router
from app.services.dicom_connector import scan_and_import
from app.core.config import get_settings

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    # Kick off a light background loop to process DICOM inbox periodically.
    async def dicom_watcher():
        while True:
            from app.db.session import SessionLocal

            db = SessionLocal()
            try:
                scan_and_import(db)
            finally:
                db.close()
            await asyncio.sleep(300)  # every 5 minutes

    asyncio.create_task(dicom_watcher())
