# ⚙️ Advanced Usage

This section covers advanced developer workflows including testing, deployment, and performance optimization for **BiddyaPeeth (MindJunkies)**.

---

## Testing with `pytest`

The project uses **`pytest`** along with `model_bakery`, `pytest-django`, and `coverage` to ensure quality and stability.

### Run All Tests

```bash
uv run pytest -n auto
```

### Generate Coverage Report

```bash
uv run coverage run -m pytest
uv run coverage report -m
uv run coverage html  # view report in htmlcov/index.html
```

> Tip: Add `--disable-warnings` to suppress noisy logs.

---

## Deployment to DigitalOcean Kubernetes

The app is deployed on a **DigitalOcean Kubernetes Cluster** with full CI/CD integration.

### 🧱 CI/CD with GitHub Actions

- Auto-deployment on push to `main` or `deployment-*`
- Docker image built and pushed to **DO Container Registry**
- Kubernetes deployment via `kubectl apply`
- Uses `.env.prod` injected into cluster secrets

### Manual Deployment Commands

```bash
# Authenticate with DigitalOcean
doctl kubernetes cluster kubeconfig save django-mindjunkies

# Apply Kubernetes manifests
kubectl apply -f k8s/apps/django-mindjunkies-web.yml
kubectl apply -f k8s/apps/elasticsearch.yml
kubectl apply -f k8s/apps/redis.yml

# Run post-deploy jobs
kubectl apply -f k8s/jobs/django-migrate-job.yml
kubectl wait --for=condition=complete job/django-migrate-job

kubectl apply -f k8s/jobs/django-collectstatic-job.yml
kubectl wait --for=condition=complete job/django-collectstatic-job
```

---

## 🌐 Ingress & HTTPS

- Ingress is managed with Nginx and Cert-Manager
- TLS issued by Let’s Encrypt
- Ingress routes traffic securely to Django containers

---

## 🔍 Debugging Tips

```bash
kuberctl get pods # List all pods

# Enter the running container
kubectl exec -it <pod-name> -- /bin/bash # Enter a pod

# Tail logs
kubectl logs -f deployment/django-mindjunkies-web-deployment
```