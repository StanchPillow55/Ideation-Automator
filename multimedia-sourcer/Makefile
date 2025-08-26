SHELL:=/bin/bash
up: ; docker compose up --build -d
down: ; docker compose down -v
logs: ; docker compose logs -f --tail=200
test: ; docker compose exec api pytest -q
seed: ; bash scripts/e2e_smoke.sh
fmt: ; docker compose exec api bash -lc 'black . || true'
