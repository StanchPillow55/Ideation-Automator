# 🧪 Testing - Ideation-Automator (Multimedia Sourcer)

## Running Tests

### Full Stack Setup
```bash
# Start all services
docker compose up --build -d

# Run E2E smoke test (seeds data)
bash scripts/e2e_smoke.sh

# Run API tests
docker compose exec api pytest -q
```

### API Tests (`api/tests/test_api.py`)
- Source CRUD operations
- Pipeline execution
- Job status tracking
- Export endpoints

## Test Coverage

### Endpoints Tested
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/v1/sources` | POST | Create source |
| `/v1/sources` | GET | List sources |
| `/v1/pipelines/run` | POST | Start pipeline |
| `/v1/jobs/{id}` | GET | Job status |
| `/v1/packs` | GET | List packs |
| `/exports/{file}` | GET | Download export |

### E2E Smoke Test
The `e2e_smoke.sh` script:
1. Creates sample sources (web, youtube)
2. Triggers pipeline execution
3. Waits for job completion
4. Verifies exports exist

## Manual Testing

### Test Web Ingestion
```bash
curl -X POST http://localhost:8000/v1/sources \
  -H "Content-Type: application/json" \
  -d '{"source_type": "web", "url_or_path": "https://example.com"}'
```

### Test Pipeline
```bash
curl -X POST http://localhost:8000/v1/pipelines/run \
  -H "Content-Type: application/json" \
  -d '{"source_ids": ["doc_xxx"], "export_options": {}}'
```

## Known Limitations

1. **Stub ingestion:** PDF, DOCX, PPTX, audio, Instagram return stub content
2. **MVP embeddings:** SHA256-based, not semantic (8-dim)
3. **No authentication:** API is open in development

## CI/CD Status
**Docker-based** - Tests run in containers via `docker compose exec`.
