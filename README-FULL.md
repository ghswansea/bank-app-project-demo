# Secure Bank App CI/CD Pipeline Demo

A complete demonstration of a secure banking application with enterprise-grade CI/CD pipeline, Kubernetes deployment, and observability stack.

## 📋 Project Structure

```
├── app/                          # Flask application package
│   ├── __init__.py              # App factory
│   ├── main.py                  # API routes (login, balance, transfer)
│   └── auth.py                  # Token creation and verification
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_api.py              # API endpoint tests
├── .github/workflows/           # GitHub Actions CI/CD pipelines
│   └── ci.yml                   # CI pipeline: test, lint, security scan, build, sign, push
├── Dockerfile                   # Multi-stage Flask/Gunicorn container
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Black, isort, pytest config
├── wsgi.py                      # WSGI entrypoint for gunicorn
├── .flake8                      # Flake8 linter config
├── .gitleaks.toml              # Secret scanning config
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip & venv
- Docker (for containerization)
- git (for GitHub Actions)

### Local Development

1. **Clone and setup**
   ```bash
   cd /home/hua/projects/bank-app-project-demo
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   FLASK_APP=wsgi:app flask run --host=0.0.0.0 --port=5000
   ```
   App runs at `http://localhost:5000`

3. **Run tests**
   ```bash
   pytest -v
   ```

4. **Run linters**
   ```bash
   flake8 app tests wsgi.py --max-line-length=127
   black --check app tests wsgi.py
   isort --check-only app tests wsgi.py
   ```

## 📱 API Endpoints

### Health Check
```bash
GET /health
```
Response:
```json
{"status": "ok"}
```

### Login
```bash
POST /login
Content-Type: application/json

{"username": "alice", "password": "password1"}
```
Response:
```json
{"token": "<JWT-like-token>"}
```

### Check Balance
```bash
GET /balance
Authorization: Bearer <token>
```
Response:
```json
{"user": "alice", "balance": 1000.0}
```

### Transfer Funds
```bash
POST /transfer
Authorization: Bearer <token>
Content-Type: application/json

{"to": "bob", "amount": 100.0}
```
Response:
```json
{"status": "success", "from": "alice", "to": "bob", "amount": 100.0}
```

## Demo Users
- **alice**: password `password1`, balance `1000.0`
- **bob**: password `password2`, balance `500.0`

## 🏗️ Docker Build & Run

1. **Build image**
   ```bash
   docker build -t bank-app:latest .
   ```

2. **Run container**
   ```bash
   docker run -p 5000:5000 -e SECRET_KEY=my-secret bank-app:latest
   ```

3. **Test in container**
   ```bash
   curl http://localhost:5000/health
   ```

## 🔄 CI/CD Pipeline (GitHub Actions)

The `.github/workflows/ci.yml` automates:

### 1. **Test** job
- Runs pytest on all PRs and pushes
- Runs on Python 3.11

### 2. **Lint** job
- **flake8**: Code style (PEP8)
- **black**: Code formatting
- **isort**: Import sorting
- Runs on all PRs and pushes

### 3. **Security** job
- **Trivy**: Filesystem vulnerability scanning
  - Scans all files for known CVEs
  - Results uploaded to GitHub Security tab
- **Gitleaks**: Secret detection
  - Scans for API keys, DB passwords, AWS credentials
  - Configured in `.gitleaks.toml`

### 4. **Build** job (runs after test, lint, security pass)
- **Docker Buildx**: Multi-platform builds
- **Push to GHCR** (GitHub Container Registry)
  - Only on main branch or when releasing
  - Skips on PRs to prevent accidental pushes
- **Cosign signing**: Image signing with keyless (OIDC)
  - Uses GitHub OIDC provider for trust
  - Continue-on-error to allow unsigned images in dev

## 🔐 Security Features

### Secret Scanning (.gitleaks.toml)
Detects:
- Generic API keys
- AWS access keys
- Database connection strings
- Custom patterns

Allowlist for dev secrets:
- `password1`, `password2`, `dev-secret`, `test-secret`

### Code Quality
- **Flake8**: Style & logic errors (F-codes)
- **Black**: Consistent formatting (max 127 chars)
- **isort**: Organized imports

### Container Scanning
- **Trivy**: Scans base image + application dependencies
- Results visible in GitHub Security/Code scanning tab

### Image Signing
- **Cosign**: Sign images with keyless OIDC (GitHub provider)
- Enables provenance and supply chain security
- (Optional: configure private key signing for prod)

## 📊 Observability (Next Phase)

- **Prometheus**: Metrics collection
- **Grafana**: Dashboard visualization
- **ELK Stack**: Centralized logging (Elasticsearch, Logstash, Kibana)

## ☸️ Kubernetes Deployment (Next Phase)

- **Helm Charts**: Templated K8s manifests
- **ArgoCD**: GitOps continuous deployment
- **Blue/Green or Canary**: Advanced deployment strategies

## 🏛️ Infrastructure-as-Code (Next Phase)

- **Terraform**: Provision VPC, EKS, IAM roles, security groups, RDS

## 📝 Configuration

### Environment Variables
- `SECRET_KEY`: JWT signing secret (default: `dev-secret`)
- `FLASK_ENV`: `production` or `development` (default: `production`)

### Build Configuration
- **Python**: 3.11 slim base image
- **App Server**: gunicorn (production-ready WSGI)
- **Port**: 5000 (container), configurable on host

## 🤝 Contributing

1. Create a feature branch
2. Commit changes (CI pipeline runs on PR)
3. Ensure all checks pass (tests, lint, security)
4. Merge to main (builds & pushes image)

## 📄 License

This is a demo project for educational purposes.

---

**Next steps:**
- Set up GitHub repository and enable Actions
- Configure Docker registry (GHCR, DockerHub, or ECR)
- Set up Kubernetes cluster (Kind, Minikube, or EKS)
- Deploy Helm charts for app, Prometheus, Grafana, ELK
- Configure Terraform for cloud infrastructure
