# Architecture

```mermaid
flowchart LR
    U[User browser] -->|HTTP :80| ALB[Application Load Balancer<br/>public subnets]
    subgraph VPC[AWS VPC 10.0.0.0/16]
        ALB -->|:8000| BE[ECS Fargate: backend<br/>FastAPI + frontend]
        BE -->|enqueue / read result| R[(ElastiCache Redis<br/>private subnets)]
        W[ECS Fargate: worker<br/>Celery] -->|consume / store result| R
        NAT[NAT Gateway] --- BE
        NAT --- W
    end
    GH[GitHub Actions] -->|OIDC| IAM[AWS IAM role]
    GH -->|push images| ECR[ECR: backend + worker]
    GH -->|terraform apply| VPC
    ECR -.->|pull image| BE
    ECR -.->|pull image| W
    BE -->|logs| CW[CloudWatch Logs + Alarm]
    W -->|logs| CW
```

Request flow: the browser calls `POST /notify/`, the backend enqueues a Celery task in Redis, the worker runs it and stores the result in Redis, and the browser polls `GET /task_status/{task_id}` until it is SUCCESS.
