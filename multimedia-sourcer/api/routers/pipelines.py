from fastapi import APIRouter,HTTPException,Depends; from sqlalchemy.orm import Session; from sqlalchemy import select
from db import SessionLocal; from schemas import PipelineRunRequest,JobOut; from models import Job,Document; from tasks import run_pipeline
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pipelines/run",response_model=JobOut)
def run_pipeline_endpoint(req:PipelineRunRequest,db:Session=Depends(get_db)):
    got=db.execute(select(Document.id).where(Document.id.in_(req.source_ids))).scalars().all()
    if len(got)!=len(req.source_ids): raise HTTPException(status_code=400,detail="Some source_ids not found")
    job=Job(source_ids=req.source_ids,status="queued",stages={k:"pending" for k in ["ingest","normalize","embed","analyze","synthesize","export"]}); db.add(job); db.commit(); db.refresh(job)
    run_pipeline.delay(job.job_id,req.source_ids,req.export_options or {}); return JobOut(job_id=job.job_id,status=job.status,stages=job.stages,result=job.result,error=job.error)

@router.get("/jobs/{job_id}",response_model=JobOut)
def get_job(job_id:str,db:Session=Depends(get_db)):
    j=db.get(Job,job_id); 
    if not j: raise HTTPException(status_code=404,detail="Job not found")
    return JobOut(job_id=j.job_id,status=j.status,stages=j.stages,result=j.result,error=j.error)
