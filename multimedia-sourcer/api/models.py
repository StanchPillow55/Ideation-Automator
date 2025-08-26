import uuid,enum; from datetime import datetime
from sqlalchemy import Column,String,DateTime,Text,Integer,ForeignKey,Float,Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from db import Base; from pgvector.sqlalchemy import Vector
EMBED_DIM=8
class SourceType(str,enum.Enum): web="web"; youtube="youtube"; pdf="pdf"; docx="docx"; pptx="pptx"; audio="audio"; instagram="instagram"
def gen_id(p): return f"{p}_{uuid.uuid4().hex[:8]}"
class Document(Base):
    __tablename__="documents"; id=Column(String,primary_key=True,default=lambda:gen_id("doc"))
    source_type=Column(Enum(SourceType),nullable=False); url_or_path=Column(String); publisher=Column(String); author=Column(String); published_at=Column(String)
    language=Column(String,default="en"); raw_text=Column(Text,default=""); media=Column(JSONB,default=list); tables=Column(JSONB,default=list); created_at=Column(DateTime,default=datetime.utcnow)
    chunks=relationship("Chunk",back_populates="document",cascade="all, delete-orphan"); claims=relationship("Claim",back_populates="document",cascade="all, delete-orphan")
class Chunk(Base):
    __tablename__="chunks"; id=Column(String,primary_key=True,default=lambda:gen_id("chk"))
    doc_id=Column(String,ForeignKey("documents.id"),nullable=False); text=Column(Text,nullable=False); order=Column(Integer,default=0); embedding=Column(Vector(EMBED_DIM))
    document=relationship("Document",back_populates="chunks")
class Claim(Base):
    __tablename__="claims"; claim_id=Column(String,primary_key=True,default=lambda:gen_id("clm"))
    doc_id=Column(String,ForeignKey("documents.id"),nullable=False); chunk_id=Column(String,ForeignKey("chunks.id"))
    text=Column(Text,nullable=False); support_type=Column(String,default="quote"); support_span=Column(JSONB,default=dict)
    strength=Column(Float,default=0.75); topics=Column(JSONB,default=list); entities=Column(JSONB,default=list); citation_key=Column(String,nullable=False)
    document=relationship("Document",back_populates="claims")
class SlidePack(Base):
    __tablename__="slidepacks"; pack_id=Column(String,primary_key=True,default=lambda:gen_id("pack"))
    title=Column(String,default="Synthesis Pack"); thesis=Column(Text,default=""); sections=Column(JSONB,default=list); references=Column(JSONB,default=list); exports=Column(JSONB,default=dict); created_at=Column(DateTime,default=datetime.utcnow)
class Job(Base):
    __tablename__="jobs"; job_id=Column(String,primary_key=True,default=lambda:gen_id("job"))
    source_ids=Column(JSONB,default=list); status=Column(String,default="queued"); stages=Column(JSONB,default=dict); result=Column(JSONB,default=dict); error=Column(Text)
    created_at=Column(DateTime,default=datetime.utcnow); updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
