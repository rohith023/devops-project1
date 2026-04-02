# Deployment Guide

Complete guide for deploying the Cloud-Native Drug Recommendation System in different environments.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Deployment](#local-development-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [AWS Deployment with Terraform](#aws-deployment-with-terraform)
6. [Production Checklist](#production-checklist)
7. [Deployment Troubleshooting](#deployment-troubleshooting)
8. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### General Requirements
- Git 2.30+
- Python 3.11+
- pip or conda package manager

### Environment-Specific Requirements

**Local Development**:
- Python virtual environment
- 2GB RAM minimum

**Docker**:
- Docker 20.10+
- Docker Compose 2.0+ (optional)
- 2GB RAM minimum

**Kubernetes**:
- kubectl 1.28+
- Kubernetes cluster 1.28+
- 4GB RAM minimum

**AWS (Terraform)**:
- Terraform 1.0+
- AWS CLI configured
- AWS credentials with appropriate permissions
- 2+ vCPU, 4GB RAM for EC2

---

## Local Development Deployment

### Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd drug-recommendation-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train model
python train/train_model.py

# 5. Run application
python app.py

# 6. In another terminal, run tests
pytest test_app.py -v
```

### Detailed Steps

#### Step 1: Setup Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Verify
which python  # Should show venv path
python --version  # Should show 3.11+
```

#### Step 2: Install Dependencies

```bash
# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
pip check  # Should have no conflicts
```

#### Step 3: Train Machine Learning Model

```bash
# Run training
python train/train_model.py

# Expected output:
# Loading data from: .../data/drug200.csv
# Data shape: (45, 4)
# Model saved to: ./model.pkl
# Training accuracy: 0.9333
```

#### Step 4: Run Application

```bash
# Start Flask development server
python app.py

# Server starts on port 5000
# Output:
# * Running on http://0.0.0.0:5000
```

#### Step 5: Test APIs

**In another terminal**:

```bash
# Test home endpoint
curl http://localhost:5000/

# Test health check
curl http://localhost:5000/health

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 50,
    "bp": "HIGH",
    "cholesterol": "HIGH"
  }'

# Run full test suite
pytest test_app.py -v
```

### Shutdown

```bash
# Stop Flask server
Ctrl + C

# Deactivate virtual environment
deactivate
```

---

## Docker Deployment

### Build Docker Image

```bash
# Navigate to project root (where Dockerfile exists)
cd drug-recommendation-system

# Build image
docker build -t drug-recommendation:latest .

# Verify image
docker images | grep drug-recommendation

# Expected output:
# drug-recommendation  latest  abc123def456  2 minutes ago  456MB
```

### Run Docker Container

```bash
# Basic run
docker run -p 5000:5000 drug-recommendation:latest

# With name and background
docker run -d \
  --name drug-app \
  -p 5000:5000 \
  drug-recommendation:latest

# With environment variables
docker run -d \
  --name drug-app \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  drug-recommendation:latest

# With volume mount (for logs)
docker run -d \
  --name drug-app \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  drug-recommendation:latest

# With resource limits
docker run -d \
  --name drug-app \
  -p 5000:5000 \
  --memory=512m \
  --cpus=1 \
  drug-recommendation:latest
```

### Verify Container

```bash
# Check if running
docker ps | grep drug-app

# View logs
docker logs drug-app

# Follow logs (tail -f style)
docker logs -f drug-app

# Test from outside container
curl http://localhost:5000/health

# Access container shell
docker exec -it drug-app /bin/bash

# Check container resources
docker stats drug-app
```

### Push to Registry

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag drug-recommendation:latest \
  yourusername/drug-recommendation:latest

# Push
docker push yourusername/drug-recommendation:latest

# Or use GitHub Container Registry (GHCR)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

docker tag drug-recommendation:latest \
  ghcr.io/YOUR_ORG/devops:latest

docker push ghcr.io/YOUR_ORG/devops:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  drug-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run with compose:

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Cleanup

```bash
# Stop container
docker stop drug-app

# Remove container
docker rm drug-app

# Remove image
docker rmi drug-recommendation:latest

# Clean up everything (careful!)
docker system prune -a
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Minikube (for local testing)
curl -minikube https://github.com/kubernetes/minikube/releases/download/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin/

# Start Minikube cluster
minikube start --cpus=4 --memory=4096

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

### Deploy Application

```bash
# Navigate to project root
cd drug-recommendation-system

# Apply all Kubernetes manifests
kubectl apply -f k8s/

# Verify resources created
kubectl get all -n drug-recommendation

# Expected output:
# NAME                                   READY   STATUS    RESTARTS
# pod/drug-recommendation-app-xxxxx      1/1     Running   0
# pod/drug-recommendation-app-xxxxx      1/1     Running   0

# NAME                               TYPE        CLUSTER-IP      EXTERNAL-IP
# service/drug-recommendation-service NodePort    10.97.xxx.xxx   <pending>
```

### Access Application

```bash
# Port forward to local machine
kubectl port-forward -n drug-recommendation \
  svc/drug-recommendation-service 5000:5000

# Or get NodePort
kubectl get svc drug-recommendation-service -n drug-recommendation \
  -o jsonpath='{.spec.ports[0].nodePort}'

# For Minikube
minikube service drug-recommendation-service -n drug-recommendation

# Test API
curl http://localhost:5000/health
```

### Monitor Deployment

```bash
# View deployment status
kubectl get deployment drug-recommendation-app -n drug-recommendation

# Describe deployment
kubectl describe deployment drug-recommendation-app -n drug-recommendation

# View pod logs
kubectl logs -n drug-recommendation -l app=drug-recommendation -f

# View specific pod logs
kubectl logs -n drug-recommendation <pod-name>

# Get events
kubectl get events -n drug-recommendation --sort-by='.lastTimestamp'
```

### Scaling

```bash
# Manual scale
kubectl scale deployment drug-recommendation-app \
  -n drug-recommendation --replicas=5

# Auto scaling status
kubectl get hpa -n drug-recommendation

# Watch HPA in action
kubectl get hpa drug-recommendation-hpa \
  -n drug-recommendation --watch
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/drug-recommendation-app \
  -n drug-recommendation \
  drug-recommendation=ghcr.io/YOUR_ORG/devops:v1.1.0

# Verify rollout
kubectl rollout status deployment/drug-recommendation-app \
  -n drug-recommendation

# View rollout history
kubectl rollout history deployment/drug-recommendation-app \
  -n drug-recommendation

# Rollback to previous version
kubectl rollout undo deployment/drug-recommendation-app \
  -n drug-recommendation
```

### Cleanup

```bash
# Delete namespace (removes all resources)
kubectl delete namespace drug-recommendation

# Or delete specific resources
kubectl delete deployment drug-recommendation-app \
  -n drug-recommendation

# Delete service
kubectl delete service drug-recommendation-service \
  -n drug-recommendation
```

---

## AWS Deployment with Terraform

### Prerequisites

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Configure AWS credentials
aws configure
# Enter: Access Key, Secret Key, Region, Output format
```

### Deploy Infrastructure

```bash
# Navigate to Terraform directory
cd terraform/

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan

# Review plan output carefully

# Apply configuration
terraform apply tfplan

# Get outputs
terraform output
```

### Terraform Configuration

Update `terraform/terraform.tfvars`:

```hcl
aws_region          = "us-east-1"
environment         = "prod"
instance_type       = "t3.small"
create_ec2_instance = true
allowed_ssh_cidr    = ["YOUR.IP.ADDRESS/32"]
docker_image        = "ghcr.io/YOUR_ORG/devops:latest"
```

### Verify Deployment

```bash
# Get public IP
terraform output ec2_instance_public_ip

# SSH into instance
ssh -i ~/.ssh/aws-key.pem ubuntu@<PUBLIC_IP>

# Check Docker container
docker ps
docker logs drug-recommendation-app

# Test API
curl http://<PUBLIC_IP>:5000/health
```

### Update Infrastructure

```bash
# Make changes to .tf files

# Plan changes
terraform plan

# Apply changes
terraform apply

# Verify
terraform output
```

### Destroy Infrastructure

```bash
# Review what will be destroyed
terraform plan -destroy

# Destroy all resources
terraform destroy

# Or destroy specific resource
terraform destroy -target=aws_instance.drug_recommendation_instance
```

---

## Production Checklist

Before deploying to production:

### Code Quality
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] No security vulnerabilities
- [ ] Code reviewed by team
- [ ] CI/CD pipeline passing

### Application
- [ ] Error handling verified
- [ ] Logging configured
- [ ] Health checks implemented
- [ ] API documented
- [ ] Performance tested

### Infrastructure
- [ ] Load balancer configured
- [ ] Auto-scaling configured
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan tested
- [ ] Monitoring and alerts set up

### Security
- [ ] Secrets management configured
- [ ] SSL/TLS certificates installed
- [ ] IAM roles and policies reviewed
- [ ] Network security groups verified
- [ ] DDoS protection enabled

### Documentation
- [ ] Deployment guide completed
- [ ] Runbooks created
- [ ] Incident response plan created
- [ ] Architecture diagram updated
- [ ] Team trained

### Deployment
- [ ] Dry run completed successfully
- [ ] Rollback plan tested
- [ ] Monitoring dashboards ready
- [ ] On-call rotation scheduled
- [ ] Deployment window scheduled

---

## Deployment Troubleshooting

### Docker Issues

**Issue**: Build fails with dependency errors
```bash
# Solution: Clear cache and rebuild
docker build --no-cache -t drug-recommendation:latest .
```

**Issue**: Container exits immediately
```bash
# Solution: Check logs
docker logs <container-id>

# Check model file
docker exec <container-id> ls -la model.pkl
```

### Kubernetes Issues

**Issue**: Pod stays in Pending state
```bash
# Check events
kubectl describe pod <pod-name> -n drug-recommendation

# Check resources available
kubectl top nodes
kubectl top pods -n drug-recommendation
```

**Issue**: Pod crashes with CrashLoopBackOff
```bash
# View logs
kubectl logs <pod-name> -n drug-recommendation

# Run debug pod
kubectl run -it debug --image=ubuntu --restart=Never -n drug-recommendation -- /bin/bash
```

### Terraform Issues

**Issue**: "Access Denied" errors
```bash
# Verify credentials
aws sts get-caller-identity

# Re-configure
aws configure
```

**Issue**: Resource already exists
```bash
# Import existing resource
terraform import aws_vpc.drug_recommendation_vpc vpc-xxxxx
```

---

## Rollback Procedures

### Docker Rollback

```bash
# Keep previous image tags
docker tag drug-recommendation:v1.1.0 drug-recommendation:latest

# Redeploy previous version
docker run -d --name drug-app drug-recommendation:v1.0.0
```

### Kubernetes Rollback

```bash
# View rollout history
kubectl rollout history deployment/drug-recommendation-app \
  -n drug-recommendation

# Rollback to previous version
kubectl rollout undo deployment/drug-recommendation-app \
  -n drug-recommendation

# Rollback to specific revision
kubectl rollout undo deployment/drug-recommendation-app \
  -n drug-recommendation --to-revision=2

# Verify rollback
kubectl rollout status deployment/drug-recommendation-app \
  -n drug-recommendation
```

### Terraform Rollback

```bash
# View previous state
terraform state list

# Rollback by re-applying previous plan
terraform plan
terraform apply -target=aws_instance.drug_recommendation_instance

# Or recreate resources
terraform destroy -target=aws_instance.drug_recommendation_instance
terraform apply -target=aws_instance.drug_recommendation_instance
```

---

**Last Updated**: April 2, 2024
**Status**: Complete and Tested
