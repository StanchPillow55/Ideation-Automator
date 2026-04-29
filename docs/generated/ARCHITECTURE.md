# 🏗️ Architecture - Ideation-Automator (Multimedia Sourcer)

## System Overview

```
┌─────────────────┐     ┌─────────────────┐
│   Next.js UI    │────▶│   FastAPI API   │
│   (Port 3000)   │     │   (Port 8000)   │
└─────────────────┘     └────────┬────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PostgreSQL    │     │     Redis       │     │     MinIO       │
│   + pgvector    │     │   (Celery)      │     │   (S3 Storage)  │
│   (Port 5432)   │     │   (Port 6379)   │     │   (Port 9000)   │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                        ┌────────▼────────┐
                        │  Celery Worker  │
                        │  (Pipeline)     │
                        └─────────────────┘
```

## Pipeline Stages (`tasks.py`)

```
POST /v1/pipelines/run
         │
         ▼
┌─────────────────┐
│  1. INGEST      │  Fetch content by source type
│  (ingestion.py) │  Web: trafilatura, YouTube: VTT, etc.
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. NORMALIZE   │  Chunk text into ~300 char segments
│  (rag.py)       │  Delete old chunks, create new
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. EMBED       │  Generate embeddings (sha256-based MVP)
│  (rag.py)       │  Store in pgvector column
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. ANALYZE     │  Extract claims from chunks
│  (tasks.py)     │  Add citation keys, support spans
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. SYNTHESIZE  │  Build SlidePack from claims
│  (tasks.py)     │  Create sections, references
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. EXPORT      │  Generate all formats
│  (export.py)    │  PPTX, PDF, HTML, MD, JSON → MinIO
└─────────────────┘
```

## Data Flow

### Document Ingestion
```
Source URL/Path → ingest_by_type() → raw_text + language
                         │
                 ┌───────┴────────┐
                 │  Source Types  │
                 ├────────────────┤
                 │ web: trafilatura│
                 │ youtube: VTT   │
                 │ pdf: stub      │
                 │ docx: stub     │
                 │ pptx: stub     │
                 │ audio: stub    │
                 │ instagram: stub│
                 └────────────────┘
```

### Embedding & RAG
```
raw_text → chunk_text(max=300) → embed_chunks() → Vector(8)
                                       │
                               SHA256-based hash
                               (normalized 8-dim)
```

### Export Pipeline
```
SlidePack → render_pptx()  → pack_{id}.pptx
          → render_pdf()   → pack_{id}.pdf
          → render_html()  → pack_{id}.html
          → save_marp_md() → pack_{id}.md
          → save_json()    → pack_{id}.json
                   │
                   └── upload_to_minio()
```

## Database Schema

```
Document (1) ──┬── (N) Chunk
               └── (N) Claim

Chunk (1) ──── (N) Claim

Job ──── tracks pipeline execution
SlidePack ──── synthesized output
```

## Key Design Decisions

### Celery for Async Processing
- Long-running pipeline stages
- Job status tracking
- Error recovery

### pgvector for Embeddings
- Native PostgreSQL vector support
- Efficient similarity search
- Simple deployment

### MinIO for Exports
- S3-compatible API
- Local development friendly
- Production-ready
