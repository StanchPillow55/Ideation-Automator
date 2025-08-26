import os; from fastapi import FastAPI; from fastapi.middleware.cors import CORSMiddleware; from fastapi.staticfiles import StaticFiles
from db import init_db; from routers import sources,pipelines,packs
app=FastAPI(title="Multimedia Sourcer API",version="0.1.0")
orig=os.getenv("CORS_ALLOW_ORIGIN","*"); app.add_middleware(CORSMiddleware,allow_origins=["*"] if orig=="*" else [orig],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.on_event("startup")
def _startup(): init_db(); os.makedirs(os.getenv("EXPORTS_DIR","/data/exports"),exist_ok=True)
app.include_router(sources.router,prefix="/v1",tags=["sources"]); app.include_router(pipelines.router,prefix="/v1",tags=["pipelines"]); app.include_router(packs.router,prefix="/v1",tags=["packs"])
app.mount("/exports",StaticFiles(directory=os.getenv("EXPORTS_DIR","/data/exports")),name="exports")
@app.get("/health") 
def health(): return {"status":"ok"}
