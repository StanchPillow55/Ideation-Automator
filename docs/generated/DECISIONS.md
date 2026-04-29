# 📋 Decisions - Ideation-Automator (Multimedia Sourcer)

## ADR-001: Celery for Pipeline Processing

### Status
Accepted

### Decision
Use Celery with Redis for async pipeline execution.

### Rationale
- 6-stage pipeline can take minutes
- Job status tracking needed
- Error recovery per stage

### Evidence
`api/tasks.py`, `api/celery_app.py`

---

## ADR-002: pgvector for Embeddings

### Status
Accepted

### Decision
Use PostgreSQL pgvector extension for vector storage.

### Rationale
- Single database for all data
- Native similarity search
- Simpler than separate vector DB

### Evidence
`api/models.py:16-17`

---

## ADR-003: SHA256-based MVP Embeddings

### Status
Accepted (MVP)

### Decision
Use SHA256 hash for embeddings instead of semantic models.

### Rationale
- MVP simplicity
- No ML dependencies for basic testing
- Plan to upgrade to real embeddings

### Trade-off
- No semantic similarity (exact match only)

### Evidence
`api/services/rag.py:2-3`

---

## ADR-004: MinIO for Export Storage

### Status
Accepted

### Decision
Use MinIO (S3-compatible) for export file storage.

### Rationale
- S3 API compatibility
- Easy local development
- Production-ready scaling

### Evidence
`api/services/export.py`

---

## ADR-005: Trafilatura for Web Scraping

### Status
Accepted

### Decision
Use trafilatura for web content extraction.

### Rationale
- Excellent boilerplate removal
- Multi-language support
- Handles various HTML structures

### Evidence
`api/services/ingestion.py:1,7-8`

---

## ADR-006: Docker Compose Deployment

### Status
Accepted

### Decision
Full-stack Docker Compose with 5 services.

### Rationale
- Reproducible development environment
- One-command startup
- Matches production topology

### Evidence
`docker-compose.yml`
