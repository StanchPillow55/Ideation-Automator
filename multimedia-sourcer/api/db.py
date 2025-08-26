import os; from contextlib import contextmanager; from sqlalchemy import create_engine,text; from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://msource:msource@db:5432/msourcer"); engine=create_engine(DATABASE_URL,pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False); Base=declarative_base()
def init_db(): 
    with engine.connect() as c:
        try: c.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        except Exception: pass
    Base.metadata.create_all(bind=engine)
@contextmanager
def session_scope():
    s=SessionLocal()
    try: yield s; s.commit()
    except Exception: s.rollback(); raise
    finally: s.close()
