# 🎯 Interview Prep - Ideation-Automator (Multimedia Sourcer)

**Last Updated:** 2026-04-29

---

## 60-90 Second STAR Pitch

### Situation
Content creators and researchers need to synthesize information from multiple multimedia sources (web, YouTube, PDFs) into cohesive presentations with proper citations.

### Task
Build a full-stack application that ingests diverse multimedia, extracts claims with citation tracking, and generates presentation slide packs in multiple export formats.

### Action
- Designed **6-stage async pipeline** (ingest → normalize → embed → analyze → synthesize → export)
- Built **FastAPI + Celery** backend with job tracking and error recovery
- Implemented **pgvector embeddings** for future semantic search
- Created **Next.js frontend** with shadcn/ui components
- Deployed via **Docker Compose** (5 services: api, ui, db, redis, minio)

### Result

| Feature | Status | Evidence |
|---------|--------|----------|
| 7 source types | **Confirmed** | `models.py:7` |
| 5 export formats | **Confirmed** | PPTX, PDF, HTML, MD, JSON |
| Async pipeline | **Confirmed** | Celery + Redis |
| Docker deployment | **Confirmed** | `docker-compose.yml` |

---

## Technical Deep Dive

### Architecture
- **Backend:** FastAPI + SQLAlchemy + Celery
- **Frontend:** Next.js 14 + Tailwind + shadcn/ui
- **Database:** PostgreSQL + pgvector
- **Queue:** Redis
- **Storage:** MinIO (S3-compatible)

### Pipeline Stages
1. **Ingest:** Fetch content by type (web: trafilatura, YouTube: VTT)
2. **Normalize:** Chunk text (~300 chars)
3. **Embed:** Generate vectors (SHA256 MVP, pgvector storage)
4. **Analyze:** Extract claims with citations
5. **Synthesize:** Build SlidePack structure
6. **Export:** PPTX, PDF, HTML, MD, JSON → MinIO

---

## Drill-Down Q&A

### Q1: "How does the pipeline handle failures?"

**Answer (Confirmed):**
- Job model tracks status per stage
- Try/except in Celery task updates error field
- Frontend polls job status for progress

**Evidence:** `api/tasks.py:56-57`

### Q2: "Why Celery instead of async FastAPI?"

**Answer (Confirmed):**
- Long-running tasks (minutes)
- Need job persistence and status tracking
- Redis provides reliable message queue
- Can scale workers independently

**Evidence:** `api/celery_app.py`, `api/tasks.py`

### Q3: "How do you handle different source types?"

**Answer (Confirmed):**
- Enum-based source types (7 types)
- `ingest_by_type()` dispatches to specific handlers
- Web uses trafilatura for extraction
- Others use stub implementations (MVP)

**Evidence:** `api/services/ingestion.py:19-24`

### Q4: "Why pgvector instead of Pinecone/Weaviate?"

**Answer (Confirmed):**
- Single database for all data
- Simpler deployment
- Native PostgreSQL integration
- Good enough for MVP scale

**Evidence:** `api/models.py:5-6`

### Q5: "How do citations work?"

**Answer (Confirmed):**
- Citation key format: `{doc_id}:{chunk_id}`
- Support types: quote (char range) or timestamp (YouTube)
- Stored in JSONB `support_span` field

**Evidence:** `api/models.py:21-22`, `api/tasks.py:34-35`

### Q6: "What export formats are supported?"

**Answer (Confirmed):**
- **PPTX:** python-pptx with sections/bullets
- **PDF:** Simple text-based renderer
- **HTML:** Rendered from Marp markdown
- **Markdown:** Marp-compatible slides
- **JSON:** Full data pack with all claims

**Evidence:** `api/services/export.py`

### Q7: "How does the frontend work?"

**Answer (Confirmed):**
- Next.js 14 App Router
- Pages: home, sources, jobs, builder
- shadcn/ui components (button, input)
- Tailwind CSS styling

**Evidence:** `ui/app/` directory

---

## Reflection

### Technical Debt (Confirmed)

| Item | Issue |
|------|-------|
| Stub ingestion | PDF, DOCX, PPTX, audio, Instagram not implemented |
| MVP embeddings | SHA256 instead of semantic (no similarity) |
| No auth | API is open |

### What I'd Do Differently

| Change | Rationale |
|--------|-----------|
| Real embeddings | Use OpenAI/Sentence-Transformers for semantic search |
| Auth layer | JWT or API keys for production |
| Progress streaming | WebSockets for real-time pipeline updates |

---

## Quick Reference Pointers

| Topic | Document |
|-------|----------|
| Architecture | `docs/generated/ARCHITECTURE.md` |
| Decisions | `docs/generated/DECISIONS.md` |
| Testing | `docs/generated/TESTING.md` |
| Repo structure | `docs/generated/REPO_MAP.md` |
