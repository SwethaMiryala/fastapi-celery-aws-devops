# DevOps Assessment: FastAPI + Celery + Redis on AWS

A containerized FastAPI backend, Celery worker and Redis, deployed to AWS ECS Fargate with Terraform and GitHub Actions.

- Architecture diagram: [docs/architecture.md](docs/architecture.md)
- Local setup: [instructions.md](instructions.md)
- Decisions and challenges: [journey.md](journey.md)

## Layout
```
backend/      FastAPI app (main.py), Celery worker (worker.py)
frontend/     index.html single-page UI
docker/       Dockerfile.backend, Dockerfile.worker
terraform/    AWS infrastructure (VPC, ECR, ElastiCache, ECS, ALB, CloudWatch)
.github/workflows/deploy.yml   CI/CD pipeline
docker-compose.yml             full local stack
```

## Quick start (local)
```bash
cp .env.example .env
docker compose up -d --build
# open http://localhost:8000
```

## Deploy to AWS
1. Create an IAM role that GitHub Actions can assume via OIDC (trust your repo) with permissions for ECR, ECS, EC2/VPC, ElastiCache, ELB, IAM, CloudWatch.
2. In the GitHub repo add secret `AWS_ROLE_ARN` (and optional variable `AWS_REGION`, default `ap-south-1`).
3. Configure a remote Terraform backend (S3 + DynamoDB) so state persists between CI runs.
4. Push to `main`. The pipeline builds images, pushes them to ECR and runs `terraform apply`. The app URL is printed at the end (`terraform output app_url`).

Manual deploy: `cd terraform && terraform init && terraform apply`.

## API
| Method | Path | Description |
|---|---|---|
| POST | `/notify/` | Enqueue a background task, returns `task_id` |
| GET | `/task_status/{task_id}` | Task status and result |
| GET | `/health` | Health check |
