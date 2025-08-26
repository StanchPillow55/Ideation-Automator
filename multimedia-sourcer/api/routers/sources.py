import os; from typing import List,Optional; from fastapi import APIRouter,UploadFile,File,Form,HTTPException,Depends; from sqlalchemy.orm import Session
from db import SessionLocal; from models import Document,SourceType; from schemas import SourceCreateJson,DocumentOut
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sources/json",response_model=DocumentOut)
def create_source_json(p:SourceCreateJson,db:Session=Depends(get_db)):
    d=Document(source_type=p.source_type,url_or_path=p.url_or_path,language=p.language or "en"); db.add(d); db.commit(); db.refresh(d); return d

@router.post("/sources",response_model=DocumentOut)
async def create_source_form(source_type:SourceType=Form(...),url:Optional[str]=Form(None),file:Optional[UploadFile]=File(None),db:Session=Depends(get_db)):
    path=url
    if file:
        os.makedirs("/data/uploads",exist_ok=True); dest=os.path.join("/data/uploads",file.filename)
        with open(dest,"wb") as f: f.write(await file.read()); path=dest
    if not path: raise HTTPException(status_code=400,detail="Provide url or file")
    d=Document(source_type=source_type,url_or_path=path,language="en"); db.add(d); db.commit(); db.refresh(d); return d

@router.get("/sources",response_model=List[DocumentOut])
def list_sources(db:Session=Depends(get_db)): return db.query(Document).order_by(Document.created_at.desc()).limit(100).all()
