# Running the stack locally

## Prerequisites
- Docker 24+ and Docker Compose v2 (`docker compose version`)

## 1. Configure environment
```bash
cp .env.example .env
```
Edit `.env` if you want a different port or task duration.

## 2. Build all images
```bash
docker compose build
```

## 3. Start the full stack
```bash
docker compose up -d
docker compose ps
```
Open http://localhost:8000 and click **Trigger task**. The status moves from PENDING to STARTED to SUCCESS after about 10 seconds.

## 4. Test the API directly
```bash
curl -X POST http://localhost:8000/notify/ -H "Content-Type: application/json" -d '{"message":"hi"}'
curl http://localhost:8000/task_status/<task_id>
curl http://localhost:8000/health
```

## 5. Logs and debugging
```bash
docker compose logs -f              # all services
docker compose logs -f worker       # only the Celery worker
docker compose exec redis redis-cli ping
docker compose exec backend sh      # shell inside the backend
docker compose restart worker
```

## 6. Stop and clean up
```bash
docker compose down            # stop containers
docker compose down --rmi local -v   # also remove images and volumes
```

## Troubleshooting
- **Task stays PENDING**: the worker is not running or cannot reach Redis. Check `docker compose logs worker`.
- **Port already in use**: change `BACKEND_PORT` in `.env`.
- **Changed code not showing**: run `docker compose up -d --build`.
