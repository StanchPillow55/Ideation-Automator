from fastapi import APIRouter,Depends; from sqlalchemy.orm import Session; from db import SessionLocal; from models import SlidePack
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/packs")
def list_packs(db:Session=Depends(get_db)):
    ps=db.query(SlidePack).order_by(SlidePack.created_at.desc()).limit(50).all()
    return [{"pack_id":p.pack_id,"title":p.title,"thesis":p.thesis,"exports":p.exports,"created_at":p.created_at.isoformat()} for p in ps]
