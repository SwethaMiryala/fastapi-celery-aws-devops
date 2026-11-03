# Journey

## Starting point
The assignment links to a source repo (`kumarnitesh2000-cardit/devops-assignment`). I could not access it while building this, so I re-created the app from the written description: FastAPI with `POST /notify/` and `GET /task_status/{task_id}`, a Celery worker, Redis, and a single-page frontend. If you have the original code, drop its `main.py`/`worker.py` over `backend/` and keep the env-var config.

## Decisions
- **Config via env vars**: Redis URL, CORS origins, port, task duration and worker concurrency are all environment variables with safe defaults.
- **Two Dockerfiles, one codebase**: `Dockerfile.backend` and `Dockerfile.worker` share `backend/`. Both run as a non-root user.
- **Frontend served by the backend**: this removes CORS issues and means one public endpoint (the ALB) serves both UI and API.
- **AWS + Terraform**: ECS Fargate (no servers to manage), ElastiCache for managed Redis, ALB, ECR, CloudWatch logs and a CPU alarm.
- **Networking**: ALB in public subnets; backend, worker and Redis in private subnets. Redis only accepts traffic from the backend and worker security groups.
- **CI/CD**: GitHub Actions with OIDC (no long-lived AWS keys). Order: create ECR, build and push images tagged with the git SHA, then full `terraform apply`.

## Trade-offs and known limitations
- **Terraform state is local.** For CI to work across runs you must add a remote backend (S3 bucket plus DynamoDB lock table) in `terraform/main.tf`. I left it out so the project runs without pre-existing resources.
- One NAT gateway and single-node Redis keep cost low but are not highly available.
- HTTP only on the ALB; add an ACM certificate and HTTPS listener for production.
- The AWS IAM role for GitHub OIDC must be created manually once (see README).

## Challenges
- ECR repos must exist before images are pushed, but ECS needs the images; solved with a targeted apply first.
- Making the frontend work both locally and behind the ALB: it uses relative URLs, with an optional `?api=` override.
