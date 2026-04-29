# 🗺️ Repo Map - Ideation-Automator (Multimedia Sourcer)

## Project Overview
Full-stack application for ingesting multimedia content (web, YouTube, PDFs, etc.), extracting claims with citations, and synthesizing into presentation slide packs with multiple export formats.

## Directory Structure

```
Ideation-Automator/
├── multimedia-sourcer/
│   ├── api/                          # FastAPI backend
│   │   ├── app.py                   # Main FastAPI app
│   │   ├── models.py                # SQLAlchemy models
│   │   ├── schemas.py               # Pydantic schemas
│   │   ├── db.py                    # Database connection
│   │   ├── celery_app.py            # Celery configuration
│   │   ├── tasks.py                 # Async pipeline tasks
│   │   ├── routers/
│   │   │   ├── sources.py           # Source CRUD endpoints
│   │   │   ├── pipelines.py         # Pipeline execution
│   │   │   └── packs.py             # SlidePack endpoints
│   │   ├── services/
│   │   │   ├── ingestion.py         # Content ingestion
│   │   │   ├── rag.py               # Chunking & embeddings
│   │   │   └── export.py            # Export formats
│   │   └── tests/
│   │       └── test_api.py          # API tests
│   │
│   ├── ui/                           # Next.js frontend
│   │   ├── app/
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── page.tsx             # Home page
│   │   │   ├── sources/page.tsx     # Sources management
│   │   │   ├── jobs/page.tsx        # Job status
│   │   │   └── builder/page.tsx     # Pack builder
│   │   ├── components/ui/           # shadcn/ui components
│   │   └── package.json
│   │
│   ├── docker-compose.yml           # Full stack orchestration
│   ├── scripts/
│   │   └── e2e_smoke.sh             # End-to-end smoke test
│   └── README.md
│
└── README.md                         # Root readme
```

## Core Models (`api/models.py`)

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `Document` | Source document | source_type, url_or_path, raw_text, media, tables |
| `Chunk` | Text chunk with embedding | doc_id, text, order, embedding (Vector) |
| `Claim` | Extracted claim with citation | doc_id, chunk_id, text, support_type, citation_key |
| `SlidePack` | Synthesized presentation | title, thesis, sections, references, exports |
| `Job` | Pipeline execution status | source_ids, status, stages, result, error |

## Source Types
- `web` - Web pages (trafilatura extraction)
- `youtube` - YouTube videos (VTT transcripts)
- `pdf` - PDF documents
- `docx` - Word documents
- `pptx` - PowerPoint presentations
- `audio` - Audio files
- `instagram` - Instagram posts

## Export Formats
- PPTX (python-pptx)
- PDF (simple renderer)
- HTML (from Marp markdown)
- Markdown (Marp format)
- JSON (full data pack)

## Infrastructure
| Service | Purpose | Port |
|---------|---------|------|
| api | FastAPI backend | 8000 |
| ui | Next.js frontend | 3000 |
| db | PostgreSQL + pgvector | 5432 |
| redis | Celery broker | 6379 |
| minio | S3-compatible storage | 9000 |
