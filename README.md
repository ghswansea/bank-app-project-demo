# **Secure Bank App CI/CD Pipeline Demo** ✅

## ✨ Completed Components

### **1️⃣ Application** ✅
- [x] Flask banking web app with:
  - REST API: login, balance check, transfer endpoints
  - JWT-like token authentication
  - In-memory user store (demo)
- [x] API endpoints fully tested
- **Location**: `app/` directory, `wsgi.py` entrypoint

### **2️⃣ CI Pipeline** ✅
- [x] Unit tests with pytest
- [x] Static code analysis:
  - flake8 (PEP8 style)
  - black (code formatting)
  - isort (import sorting)
- [x] Security scanning:
  - Trivy (filesystem vulnerability scan)
  - gitleaks (secret detection)
- [x] Docker image build & push to GHCR
- [x] Image signing with cosign (keyless OIDC)
- **Location**: `.github/workflows/ci.yml` (GitHub Actions)

### **3️⃣ CD Pipeline** 🚧 (Next Phase)
- [ ] Kubernetes deployment manifests
- [ ] Helm charts for app, Prometheus, Grafana, ELK
- [ ] ArgoCD GitOps setup
- [ ] Blue/green or canary deployment strategies

### **4️⃣ Infrastructure-as-Code** 🚧 (Next Phase)
- [ ] Terraform modules:
  - VPC & security groups
  - EKS or Kind cluster setup
  - IAM roles
  - RDS database (optional)

### **5️⃣ Observability** 🚧 (Next Phase)
- [ ] Prometheus & Grafana (Helm charts)
- [ ] ELK stack (Elasticsearch, Logstash, Kibana)

---

## 🚀 Quick Start

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest -v

# Run linters
flake8 app tests wsgi.py --max-line-length=127

# Run app locally
FLASK_APP=wsgi:app flask run --host=0.0.0.0 --port=5000
```

**See README-FULL.md for detailed setup, API docs, and deployment instructions.**
