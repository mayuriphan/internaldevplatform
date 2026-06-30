
```
InternalDeveloperPlatformOROpenServiceBroker
├─ README.md
└─ services
   └─ api-python
      ├─ alembic
      ├─ app
      │  ├─ api
      │  │  ├─ auth.py
      │  │  ├─ deps
      │  │  │  └─ broker.py
      │  │  ├─ health.py
      │  │  ├─ jobs.py
      │  │  ├─ provision.py
      │  │  └─ status.py
      │  ├─ config
      │  │  └─ settings.py
      │  ├─ db
      │  │  ├─ database.py
      │  │  └─ models.py
      │  ├─ dependencies.py
      │  ├─ jobs
      │  │  ├─ base.py
      │  │  ├─ deployment_job.py
      │  │  ├─ factory.py
      │  │  └─ payment_job.py
      │  ├─ main.py
      │  ├─ middleware
      │  │  ├─ correlation_id.py
      │  │  ├─ idempotency.py
      │  │  ├─ ratelimit.py
      │  │  └─ request_looger.py
      │  ├─ providers
      │  │  ├─ aws_provider.py
      │  │  ├─ base.py
      │  │  ├─ factory.py
      │  │  ├─ k8_provider.py
      │  │  └─ postgres_provider.py
      │  ├─ repositories
      │  │  ├─ job_repository.py
      │  │  └─ service_repository.py
      │  ├─ schemas
      │  │  ├─ jobs.py
      │  │  └─ service.py
      │  ├─ services
      │  │  ├─ broker_service.py
      │  │  ├─ idempotency_service.py
      │  │  └─ job_service.py
      │  ├─ utils
      │  │  ├─ exceptions.py
      │  │  └─ logger.py
      │  └─ worker-python
      │     ├─ jobs
      │     │  └─ executer.py
      │     ├─ main.py
      │     ├─ services
      │     │  └─ worker_service.py
      │     └─ worker
      │        └─ provision_worker.py
      ├─ commands.txt
      ├─ infra
      │  ├─ argocd
      │  │  └─ applications
      │  │     └─ idp.yaml
      │  ├─ docker
      │  │  ├─ Dockerfile
      │  │  └─ worker.dockerfile
      │  ├─ k8s
      │  │  ├─ api-deployment.yaml
      │  │  ├─ api-service.yaml
      │  │  ├─ configmap.yaml
      │  │  ├─ hpa.yaml
      │  │  ├─ ingres.yaml
      │  │  ├─ monitoring
      │  │  │  ├─ grafana.yaml
      │  │  │  └─ prometheus.yaml
      │  │  ├─ secret.yaml
      │  │  └─ workerr-deployment.yaml
      |  └─ ansible
      |  |  │
      |  |  ├── ansible.cfg
      |  |  ├── inventory.ini
            ├── requirements.yml
            │
            ├── playbooks/
            │   ├── bootstrap.yml
            │   ├── cluster.yml
            │   └── site.yml
            │
            └── roles/
               ├── bootstrap/
               │   └── tasks/
               │       └── main.yml
               │
               ├── k3s/
               │   ├── defaults/
               │   │   └── main.yml
               │   └── tasks/
               │       └── main.yml
               │
               └── helm/
                  └── tasks/
      |  |              └── main.yml
      |  |
      │  └─ terraform
      │     ├─ .terraform.lock.hcl
      │     ├─ ecr
      │     │  ├─ main.tf
      │     │  └─ outputs.tf
      │     ├─ eks
      │     │  ├─ main.tf
      │     │  └─ variables.tf
      │     ├─ iam
      │     │  └─ main.tf
      │     ├─ main.tf
      │     ├─ outputs.tf
      │     ├─ providers.tf
      │     ├─ rds
      │     │  ├─ main.tf
      │     │  └─ variables.tf
      │     ├─ redis
      │     │  ├─ main.tf
      │     │  └─ varibales.tf
      │     ├─ sqs
      │     │  └─ main.tf
      │     ├─ terraform.tfstate
      │     ├─ terraform.tfstate.backup
      │     ├─ variables.tf
      │     └─ vpc
      │        ├─ main.tf
      │        └─ outputs.tf
      ├─ requirements.txt
      └─ tests

```