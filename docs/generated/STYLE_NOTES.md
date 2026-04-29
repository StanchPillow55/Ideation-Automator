# 🎨 Style Notes - Ideation-Automator (Multimedia Sourcer)

## Language & Ecosystem
- **Backend:** Python 3.11+ (FastAPI, SQLAlchemy, Celery)
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Database:** PostgreSQL with pgvector extension
- **Queue:** Redis + Celery
- **Storage:** MinIO (S3-compatible)
- **Deployment:** Docker Compose

## Code Conventions

### Backend (Python)
- **Compact style:** Single-line imports, minimal whitespace
- **Naming:** `snake_case` for functions/variables
- **ORM:** SQLAlchemy declarative models
- **Routers:** FastAPI APIRouter with versioned prefix (`/v1`)

### Frontend (TypeScript/React)
- **Framework:** Next.js App Router
- **Components:** Functional with TypeScript
- **Styling:** Tailwind CSS with shadcn/ui components
- **State:** React hooks

### Database Models
- **ID Generation:** `{prefix}_{uuid8}` format (e.g., `doc_abc12345`)
- **Relationships:** SQLAlchemy relationships with cascades
- **JSON Fields:** PostgreSQL JSONB for flexible schemas
- **Vectors:** pgvector for embeddings (dim=8 for MVP)

## Project Structure
```
multimedia-sourcer/
├── api/                    # FastAPI backend
│   ├── app.py             # Main app entry
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── tasks.py           # Celery tasks
│   ├── routers/           # API endpoints
│   └── services/          # Business logic
├── ui/                     # Next.js frontend
│   ├── app/               # App Router pages
│   └── components/        # React components
└── docker-compose.yml     # Full stack orchestration
```

## Error Handling
- Try/except in Celery tasks with job status updates
- FastAPI HTTPException for API errors
- Job model tracks error messages

## Testing
- pytest for API tests
- E2E smoke script (`scripts/e2e_smoke.sh`)
