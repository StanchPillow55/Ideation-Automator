from sqlalchemy.orm import Session; from sqlalchemy import select
from celery_app import celery; from db import SessionLocal
from models import Job,Document,Chunk,Claim,SlidePack
from services import ingestion as ing, rag, export as ex

def _upd(s:Session,j:Job,st:str,stt:str): j.stages[st]=stt; s.add(j); s.commit()

def _docs(s:Session,ids): return s.execute(select(Document).where(Document.id.in_(ids))).scalars().all()

@celery.task(name="run_pipeline")
def run_pipeline(job_id:str,source_ids,export_options):
    s=SessionLocal(); j=s.get(Job,job_id)
    if not j: s.close(); return
    try:
        j.status="running"; s.add(j); s.commit()
        _upd(s,j,"ingest","running"); ds=_docs(s,source_ids)
        for d in ds: txt,lang=ing.ingest_by_type(d.source_type.value,d.url_or_path or ""); d.raw_text=txt; d.language=lang; s.add(d)
        s.commit(); _upd(s,j,"ingest","completed")
        _upd(s,j,"normalize","running"); 
        for d in ds:
            s.query(Chunk).filter(Chunk.doc_id==d.id).delete()
            for i,ch in enumerate(rag.chunk_text(d.raw_text or "")): s.add(Chunk(doc_id=d.id,text=ch,order=i))
        s.commit(); _upd(s,j,"normalize","completed")
        _upd(s,j,"embed","running")
        for d in ds:
            chs=s.execute(select(Chunk).where(Chunk.doc_id==d.id).order_by(Chunk.order)).scalars().all()
            vecs=rag.embed_chunks([c.text for c in chs])
            for c,v in zip(chs,vecs): c.embedding=v; s.add(c)
        s.commit(); _upd(s,j,"embed","completed")
        _upd(s,j,"analyze","running"); s.query(Claim).filter(Claim.doc_id.in_(source_ids)).delete(synchronize_session=False)
        for d in ds:
            chs=s.execute(select(Chunk).where(Chunk.doc_id==d.id).order_by(Chunk.order)).scalars().all()
            for c in chs[:5]:
                st="timestamp" if d.source_type.value=="youtube" else "quote"; span={"start":"00:00","end":"00:10"} if st=="timestamp" else {"charRange":[0,min(50,len(c.text))]}
                s.add(Claim(doc_id=d.id,chunk_id=c.id,text=(c.text[:180]+"...") if len(c.text)>180 else c.text,support_type=st,support_span=span,citation_key=f"{d.id}:{c.id}"))
        s.commit(); _upd(s,j,"analyze","completed")
        _upd(s,j,"synthesize","running"); secs=[]; refs=[]
        for d in ds:
            cls=s.execute(select(Claim).where(Claim.doc_id==d.id)).scalars().all()
            secs.append({"title":f"{d.source_type.value.upper()} {d.id[:6]}","bullets":[{"text":cl.text,"citation_key":cl.citation_key} for cl in cls[:5]],"figures":[]})
            refs.append({"doc_id":d.id,"source_type":d.source_type.value,"url_or_path":d.url_or_path})
        p=SlidePack(title="Multimedia Sourcer Pack",thesis="Synthesized claims and summaries.",sections=secs,references=refs,exports={}); s.add(p); s.commit(); s.refresh(p)
        _upd(s,j,"synthesize","completed")
        _upd(s,j,"export","running")
        notes=[f"- {d.id} includes timestamps like [00:00-00:10]." for d in ds if d.source_type.value=="youtube"] or ["No speaker notes available."]
        notes_p=ex.save_notes_md(p.pack_id,notes); md_p=ex.save_marp_markdown(p.pack_id,p.title,p.sections)
        html_p=ex.render_html_from_markdown(md_p,p.pack_id); pdf_p=ex.render_pdf_simple(p.pack_id,p.title,p.sections); pptx_p=ex.render_pptx(p.pack_id,p.title,p.sections)
        all_claims=[]; 
        for d in ds:
            for cl in s.execute(select(Claim).where(Claim.doc_id==d.id)).scalars().all():
                all_claims.append({"claim_id":cl.claim_id,"doc_id":cl.doc_id,"chunk_id":cl.chunk_id,"text":cl.text,"support_type":cl.support_type,"support_span":cl.support_span,"citation_key":cl.citation_key})
        json_p=ex.save_datapack_json(p.pack_id,{"pack_id":p.pack_id,"title":p.title,"sections":p.sections,"references":p.references,"claims":all_claims,"coverage_confidence":{"coverage":0.8,"confidence":0.7}})
        _=[ex.upload_to_minio(x) for x in [pptx_p,pdf_p,html_p,notes_p,json_p]]
        p.exports={"pptx":pptx_p,"pdf":pdf_p,"html":html_p,"md":notes_p,"json":json_p}; s.add(p); s.commit()
        j.status="completed"; j.result={"pack_id":p.pack_id,"exports":p.exports}; s.add(j); s.commit(); s.close()
    except Exception as e:
        j.status="failed"; j.error=str(e); s.add(j); s.commit(); s.close(); raise
