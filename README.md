# Cloud-Native Drug Recommendation System with DevOps

![DevOps Badge](https://img.shields.io/badge/DevOps-Ready-brightgreen)
![Python Badge](https://img.shields.io/badge/Python-3.11-blue)
![Flask Badge](https://img.shields.io/badge/Flask-3.0-red)
![Docker Badge](https://img.shields.io/badge/Docker-Latest-blue)
![Kubernetes Badge](https://img.shields.io/badge/Kubernetes-1.28-blue)
![Terraform Badge](https://img.shields.io/badge/Terraform-1.0+-green)

## Table of Contents

1. [Overview](#overview)
2. [Project Architecture](#project-architecture)
3. [Requirements](#requirements)
4. [Project Structure](#project-structure)
5. [Quick Start](#quick-start)
6. [Running Locally](#running-locally)
7. [Running with Docker](#running-with-docker)
8. [Running with Kubernetes](#running-with-kubernetes)
9. [Infrastructure with Terraform](#infrastructure-with-terraform)
10. [CI/CD Pipeline](#cicd-pipeline)
11. [API Documentation](#api-documentation)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)

---

## Overview

This project demonstrates a complete **cloud-native drug recommendation system** built with **DevOps best practices**. It showcases:

- **Machine Learning**: Decision Tree Classifier for drug recommendation
- **Web Framework**: Flask REST API with production-ready configuration
- **Containerization**: Docker with multi-stage builds and security hardening
- **Orchestration**: Kubernetes deployment with auto-scaling and networking policies
- **Infrastructure as Code**: Terraform for AWS infrastructure provisioning
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Version Control**: Git with branching strategy (main, develop, feature branches)
- **Testing**: Comprehensive pytest test suite
- **Monitoring**: Health checks and logging

### Key Components

```
Application Flow:
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Training  │ --> │  ML Model    │ --> │  Flask API  │
│   Script    │     │  (Decision   │     │  (REST)     │
└─────────────┘     │   Tree)      │     └─────────────┘
                    └──────────────┘
```

---

## Project Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Repository                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  GitHub Actions - CI/CD Pipeline                      │ │
│  │  - Code Checkout → Dependencies → Tests → Build       │ │
│  └────────────────────────────────────────────────────────┘ │
└────────┬────────────────────────────────────────────────────┘
         │
    ┌────┴────────────────────────────────┐
    │                                     │
┌───┴─────────────────┐     ┌────────────┴──────────┐
│  Docker Registry    │     │  Kubernetes Cluster  │
│  (Container Image)  │     │  - 2+ Replicas       │
│                     │     │  - Auto-scaling      │
│  ghcr.io/...        │     │  - Service (NodePort)│
└─────────────────────┘     └──────────────────────┘
                                      │
                            ┌─────────┴──────────┐
                            │                    │
                    ┌───────┴────────┐  ┌───────┴─────────┐
                    │  Pod 1         │  │  Pod 2          │
                    │  - Flask App   │  │  - Flask App    │
                    │  - Port 5000   │  │  - Port 5000    │
                    └────────────────┘  └─────────────────┘
```

### Infrastructure Architecture (AWS with Terraform)

```
┌────────────────────────────────────────────────┐
│              AWS VPC (10.0.0.0/16)             │
│  ┌──────────────────────────────────────────┐ │
│  │         Internet Gateway                 │ │
│  └────────────────────┬─────────────────────┘ │
│                       │                       │
│  ┌────────────────────┴─────────────────────┐ │
│  │    Public Subnet (10.0.1.0/24)          │ │
│  │  ┌────────────────────────────────────┐ │ │
│  │  │   EC2 Instance (t3.small)         │ │ │
│  │  │  - Docker Container               │ │ │
│  │  │  - Elastic IP                     │ │ │
│  │  │  - Security Group                 │ │ │
│  │  └────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────┘ │
│                                               │
│  ┌──────────────────────────────────────────┐ │
│  │    Private Subnet (10.0.2.0/24)         │ │
│  │  (Reserved for future use)              │ │
│  └──────────────────────────────────────────┘ │
│                                               │
│  ┌──────────────────────────────────────────┐ │
│  │   CloudWatch Logs                        │ │
│  │   - Application logs                     │ │
│  │   - 7-day retention                      │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

---

## Requirements

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2)
- **Memory**: 2GB minimum (4GB recommended)
- **Disk Space**: 5GB minimum

### Software Requirements

- **Python**: 3.11+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Kubernetes**: 1.28+ (for K8s deployment)
- **kubectl**: 1.28+
- **Terraform**: 1.0+
- **Git**: 2.30+

### Python Dependencies

See [requirements.txt](requirements.txt)

---

## Project Structure

```
drug-recommendation-system/
├── app.py                          # Flask application (main entry point)
├── requirements.txt                # Python dependencies
├── model.pkl                       # Trained ML model (generated)
├── test_app.py                     # Pytest test suite
├── Dockerfile                      # Docker containerization
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── data/
│   └── drug200.csv                # Training dataset
│
├── train/
│   └── train_model.py             # ML model training script
│
├── k8s/
│   ├── deployment.yaml            # Kubernetes deployment config
│   └── service.yaml               # Kubernetes service & networking
│
├── terraform/
│   ├── main.tf                    # Terraform main configuration
│   ├── variables.tf               # Terraform variables
│   ├── outputs.tf                 # Terraform outputs
│   ├── terraform.tfvars           # Terraform values
│   ├── user_data.sh              # EC2 initialization script
│   └── terraform.tfstate          # Terraform state (generated)
│
└── .github/
    └── workflows/
        └── ci.yml                 # GitHub Actions CI/CD pipeline
```

---

## Quick Start

### Prerequisites

```bash
# Clone the repository
git clone <repository-url>
cd drug-recommendation-system

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 1. Train the ML Model

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python train/train_model.py

# Expected output:
# Model saved to: model.pkl
# Sample prediction: Age=45, BP=LOW, Cholesterol=NORMAL -> drugX
# ✓ Model training completed successfully!
```

### 2. Run Locally

```bash
# Start Flask application
python app.py

# Output:
# * Running on http://0.0.0.0:5000
# WARNING: This is a development server...
```

### 3. Test the API

```bash
# In a new terminal:

# Health check
curl http://localhost:5000/health

# Get model info
curl http://localhost:5000/info

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "bp": "HIGH",
    "cholesterol": "NORMAL"
  }'
```

---

## Running Locally

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model
python train/train_model.py

# Run tests
pytest test_app.py -v

# Start application
python app.py
```

### API Endpoints

#### 1. Home Endpoint
```bash
curl http://localhost:5000/
```

**Response:**
```json
{
  "status": "success",
  "message": "Cloud-Native Drug Recommendation System is running",
  "version": "1.0.0",
  "timestamp": "2024-04-02T12:00:00"
}
```

#### 2. Health Check
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "timestamp": "2024-04-02T12:00:00"
}
```

#### 3. Predict Drug (Main Endpoint)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "bp": "HIGH",
    "cholesterol": "HIGH"
  }'
```

**Response:**
```json
{
  "status": "success",
  "prediction": {
    "drug": "drugY",
    "confidence": 0.95
  },
  "input": {
    "age": 45,
    "bp": "HIGH",
    "cholesterol": "HIGH"
  },
  "timestamp": "2024-04-02T12:00:00"
}
```

#### 4. Model Information
```bash
curl http://localhost:5000/info
```

**Response:**
```json
{
  "status": "success",
  "model_info": {
    "type": "DecisionTreeClassifier",
    "max_depth": 5,
    "n_leaves": 12,
    "n_features": 3
  },
  "features": ["Age", "BP", "Cholesterol"],
  "drugs": ["drugA", "drugB", "drugC", "drugX", "drugY"],
  "timestamp": "2024-04-02T12:00:00"
}
```

### Input Validation

- **age**: Number between 0-150 (required)
- **bp**: "LOW", "NORMAL", or "HIGH" (case-insensitive, required)
- **cholesterol**: "LOW", "NORMAL", or "HIGH" (case-insensitive, required)

---

## Running with Docker

### Build Docker Image

```bash
# Build locally
docker build -t drug-recommendation:latest .

# Verify image
docker images | grep drug-recommendation
```

### Run Docker Container

```bash
# Run container
docker run -d \
  --name drug-app \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  drug-recommendation:latest

# Check logs
docker logs drug-app

# Test API
curl http://localhost:5000/health

# Stop and remove container
docker stop drug-app
docker rm drug-app
```

### Docker Compose (Optional)

```bash
# Create docker-compose.yml if needed
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Push to Container Registry

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag image
docker tag drug-recommendation:latest ghcr.io/YOUR_ORG/devops:latest

# Push image
docker push ghcr.io/YOUR_ORG/devops:latest
```

---

## Running with Kubernetes

### Prerequisites

```bash
# Install kubectl
# macOS: brew install kubectl
# Linux: curl -O https://dl.k8s.io/release/stable.txt

# Start Kubernetes cluster
# Option 1: Docker Desktop - Enable Kubernetes in settings
# Option 2: Minikube - minikube start --cpus=4 --memory=4096
# Option 3: Kind - kind create cluster

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

### Deploy to Kubernetes

```bash
# Create namespace and deploy
kubectl apply -f k8s/

# Verify deployment
kubectl get all -n drug-recommendation

# Check deployment status
kubectl describe deployment drug-recommendation-app -n drug-recommendation

# View pod logs
kubectl logs -n drug-recommendation -l app=drug-recommendation

# Port forward to local machine
kubectl port-forward -n drug-recommendation svc/drug-recommendation-service 5000:5000

# Test API
curl http://localhost:5000/health
```

### Kubernetes Features Included

- **Deployment**: 2 replicas with rolling updates
- **Service**: NodePort service on port 30080
- **Health Checks**: Liveness and readiness probes
- **Auto-scaling**: HorizontalPodAutoscaler (2-5 replicas)
- **Resource Limits**: CPU and memory constraints
- **Security**: Non-root user, network policies
- **RBAC**: ServiceAccount and role bindings
- **Networking**: Network policies for pod communication

### Access Kubernetes Application

```bash
# Get service information
kubectl get svc -n drug-recommendation

# Get external port (if using NodePort)
kubectl get svc drug-recommendation-service -n drug-recommendation -o jsonpath='{.spec.ports[0].nodePort}'

# Access via node IP:port (for Minikube)
minikube service drug-recommendation-service -n drug-recommendation

# Or use port-forward
kubectl port-forward -n drug-recommendation svc/drug-recommendation-service 5000:5000
curl http://localhost:5000/health
```

### Scale Deployment

```bash
# Manual scaling
kubectl scale deployment drug-recommendation-app -n drug-recommendation --replicas=5

# Check HPA status
kubectl get hpa -n drug-recommendation
```

### Clean Up

```bash
# Delete deployment
kubectl delete namespace drug-recommendation

# Or delete specific resources
kubectl delete deployment drug-recommendation-app -n drug-recommendation
```

---

## Infrastructure with Terraform

### Terraform Structure

```
terraform/
├── main.tf           # VPC, Subnets, EC2, IAM, Security Groups
├── variables.tf      # Variable definitions
├── outputs.tf        # Output values
├── terraform.tfvars  # Variable values
├── user_data.sh      # EC2 initialization script
└── terraform.tfstate # State file (generated)
```

### AWS Resources Provisioned

- VPC with public and private subnets
- Internet Gateway
- Route tables and associations
- Security groups with ingress/egress rules
- EC2 instance (t3.small)
- IAM roles and policies
- Elastic IP
- CloudWatch log group

### Initialize and Deploy

```bash
# Navigate to Terraform directory
cd terraform/

# Initialize Terraform
terraform init

# Environment setup
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"

# Validate configuration
terraform validate

# Plan infrastructure
terraform plan -out=tfplan

# Review the plan and apply
terraform apply tfplan

# Get outputs
terraform output

# Example output:
# vpc_id = vpc-xxxxx
# ec2_instance_public_ip = 54.xxx.xxx.xxx
# app_url = http://54.xxx.xxx.xxx:5000
```

### Terraform Variables (terraform.tfvars)

```hcl
aws_region          = "us-east-1"
environment         = "dev"
project_name        = "drug-recommendation"
instance_type       = "t3.small"
create_ec2_instance = true
allowed_ssh_cidr    = ["YOUR_IP/32"]  # Restrict SSH access
```

### Access EC2 Instance

```bash
# Get public IP
terraform output -json

# SSH into instance
ssh -i your-key.pem ubuntu@PUBLIC_IP

# Check Docker container
docker ps
docker logs drug-recommendation-app
```

### Destroy Infrastructure

```bash
# Destroy all AWS resources
terraform destroy

# Or destroy specific resource
terraform destroy -target=aws_instance.drug_recommendation_instance
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

Location: `.github/workflows/ci.yml`

#### Pipeline Stages

1. **Code Checkout** - Clone repository
2. **Dependency Installation** - Install Python packages
3. **Test Execution** - Run pytest suite
4. **Docker Image Build** - Build and push to registry
5. **Security Scanning** - Trivy vulnerability scanning

#### Workflow Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

#### Running Pipeline

The pipeline automatically runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

#### View Pipeline Status

```bash
# In GitHub repository:
# 1. Go to Actions tab
# 2. Select workflow "CI/CD Pipeline"
# 3. View build status and logs
```

#### Manual Workflow Trigger

```bash
# Using GitHub CLI
gh workflow run ci.yml --ref main
```

#### Pipeline Configuration

```yaml
jobs:
  checkout:           # Code checkout
  install-dependencies:  # Dependency installation
  test:              # Unit tests
  build-docker:      # Docker image build
  security-scan:     # Security scanning
  summary:           # Pipeline summary
```

---

## Testing

### Test Structure

```python
# test_app.py contains:
- Health endpoint tests
- Info endpoint tests
- Prediction endpoint tests
- Error handling tests
- Input validation tests
```

### Run Tests Locally

```bash
# Run all tests
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestHealthEndpoints -v

# Run specific test
pytest test_app.py::TestPredictEndpoint::test_predict_with_valid_input -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html

# Run tests in parallel
pytest test_app.py -n auto
```

### Test Coverage

```bash
# Generate coverage report
pytest test_app.py --cov=app --cov-report=term-missing

# Generate HTML report
pytest test_app.py --cov=app --cov-report=html
# Open: htmlcov/index.html
```

### Test Output Example

```
test_app.py::TestHealthEndpoints::test_home_endpoint PASSED
test_app.py::TestHealthEndpoints::test_health_endpoint PASSED
test_app.py::TestPredictEndpoint::test_predict_with_valid_input PASSED
test_app.py::TestErrorHandling::test_404_not_found PASSED

=================== 4 passed in 0.23s ===================
```

---

## API Documentation

### Request/Response Format

All requests use JSON format:
```
Content-Type: application/json
```

### Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 500 | Server Error |
| 503 | Service Unavailable |

### Error Handling

**Validation Error Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": -5, "bp": "HIGH", "cholesterol": "NORMAL"}'

# Response:
{
  "status": "error",
  "message": "Age must be a valid number between 0 and 150",
  "timestamp": "2024-04-02T12:00:00"
}
```

**Model Not Loaded Error:**
```json
{
  "status": "error",
  "message": "Model not loaded. Please train the model first.",
  "timestamp": "2024-04-02T12:00:00"
}
```

---

## Troubleshooting

### Problem: Model.pkl Not Found

**Cause**: Model hasn't been trained yet

**Solution**:
```bash
python train/train_model.py
```

### Problem: Flask App Won't Start

**Cause**: Port 5000 already in use

**Solution**:
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or run on different port
flask run --port 5001
```

### Problem: Docker Build Fails

**Cause**: Missing dependencies or corrupted cache

**Solution**:
```bash
# Clear Docker cache and rebuild
docker build --no-cache -t drug-recommendation:latest .
```

### Problem: Kubernetes Pod Crashes

**Cause**: Model file missing or permission issues

**Solution**:
```bash
# Check pod logs
kubectl logs -n drug-recommendation <pod-name>

# Verify model exists
kubectl exec -it -n drug-recommendation <pod-name> -- ls -la model.pkl

# Recreate deployment
kubectl rollout restart deployment drug-recommendation-app -n drug-recommendation
```

### Problem: Tests Fail in CI/CD

**Cause**: Model not available in CI environment

**Solution**: Tests automatically skip if model is not loaded:
```python
if model_status == 'not_loaded':
    pytest.skip("Model not loaded")
```

### Problem: Terraform Apply Fails

**Cause**: AWS credentials not configured

**Solution**:
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
terraform apply
```

### Problem: Out of Memory

**Cause**: Application consuming too much memory

**Solution**:
```bash
# Increase container memory limit in k8s/deployment.yaml
# Or increase Docker memory:
docker run -m 1024m drug-recommendation:latest
```

---

## Git Branching Strategy

### Branch Types

```
main           - Production-ready code (stable)
develop        - Development branch (integration)
feature/*      - Feature branches (new features)
bugfix/*       - Bug fix branches
hotfix/*       - Production hotfixes
```

### Workflow Example

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/new-endpoint

# Make changes and commit
git add .
git commit -m "feat: Add new prediction endpoint"

# Push to remote
git push origin feature/new-endpoint

# Create Pull Request on GitHub
# After review and approval, merge to develop

# When ready for release, merge develop to main
git checkout main
git pull origin main
git merge develop
git tag v1.0.0
git push origin main --tags
```

---

## Monitoring and Logging

### Application Logs

**Local**:
```bash
# Flask development logs
python app.py

# Check logs
tail -f app.log
```

**Docker**:
```bash
# View container logs
docker logs -f drug-app

# Tail specific lines
docker logs --tail 100 drug-app
```

**Kubernetes**:
```bash
# View pod logs
kubectl logs -n drug-recommendation <pod-name>

# Stream logs from multiple pods
kubectl logs -n drug-recommendation -l app=drug-recommendation -f
```

**AWS CloudWatch**:
```bash
# View logs in CloudWatch
aws logs tail /aws/ec2/drug-recommendation --follow
```

### Health Checks

```bash
# Application health status
curl http://localhost:5000/health

# Check model status
curl http://localhost:5000/info
```

---

## Performance Considerations

### Optimization Tips

1. **Model Caching**: Model is loaded once at startup
2. **Connection Pooling**: Implemented in Flask
3. **Concurrency**: Use gunicorn with workers
4. **Resource Limits**: Kubernetes resource quotas
5. **Auto-scaling**: HPA scales based on CPU/memory

### Scaling

```bash
# Horizontal scaling in Kubernetes
kubectl scale deployment drug-recommendation-app --replicas 10

# Vertical scaling (EC2)
# Update Terraform instance_type variable to larger instance
```

---

## Security Best Practices

### Implemented Security Measures

- Non-root user in Docker container
- Network policies in Kubernetes
- RBAC (Role-Based Access Control)
- Security groups in AWS
- Health checks and monitoring
- Input validation and error handling
- Secure logging

### Additional Recommendations

1. **Use secrets management** (HashiCorp Vault, AWS Secrets Manager)
2. **Enable SSL/TLS** for HTTPS
3. **Implement rate limiting** for API
4. **Use private container registry**
5. **Regularly update dependencies**
6. **Enable audit logging**
7. **Use service mesh** (Istio, Linkerd) for production

---

## Contributing

### Development Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -m "feat: your message"`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

### Code Standards

- PEP 8 Python style guide
- Clear commit messages
- Comprehensive test coverage
- Documentation for new features

---

## Common Commands Reference

### Setup & Installation
```bash
pip install -r requirements.txt
python train/train_model.py
```

### Local Development
```bash
python app.py
pytest test_app.py -v
```

### Docker
```bash
docker build -t drug-recommendation:latest .
docker run -p 5000:5000 drug-recommendation:latest
```

### Kubernetes
```bash
kubectl apply -f k8s/
kubectl get all -n drug-recommendation
kubectl logs -n drug-recommendation -l app=drug-recommendation
```

### Terraform
```bash
cd terraform/
terraform init
terraform plan
terraform apply
terraform destroy
```

### Git
```bash
git checkout -b feature/name
git add .
git commit -m "message"
git push origin feature/name
```

---

## License

This project is provided as-is for educational and demonstration purposes.

---

## Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review application logs
3. Check test suite for examples
4. Consult documentation in respective tools

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Apr 2, 2024 | Initial release with full DevOps stack |

---

## Acknowledgments

This project demonstrates:
- Cloud-native application development
- DevOps best practices
- Infrastructure as Code principles
- Automated testing and deployment
- Kubernetes orchestration
- Machine learning integration

Perfect for **DevOps engineers, Cloud architects, and software engineers** learning production-grade deployment practices.

---

**Last Updated**: April 2, 2024
**Status**: Production Ready ✓
