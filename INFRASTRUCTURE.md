# Infrastructure as Code - Complete Setup Guide

## Overview

This project uses **Terraform** for infrastructure provisioning, **Ansible** for configuration management, and **Kubernetes** for container orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   VPC (10.0.0.0/16)                  │    │
│  │  ┌──────────────────┐  ┌──────────────────┐       │    │
│  │  │   Public Subnet   │  │  Private Subnets │       │    │
│  │  │   (EKS Control)   │  │   (EKS Workers)  │       │    │
│  │  └──────────────────┘  └──────────────────┘       │    │
│  │         ▲                      ▲                    │    │
│  │         │                      │                    │    │
│  │  ┌──────┴──────────────────────┴──────┐             │    │
│  │  │         EKS Cluster               │             │    │
│  │  │  ┌─────────┐  ┌─────────┐         │             │    │
│  │  │  │  Pod 1  │  │  Pod 2  │  ...    │             │    │
│  │  │  │  drug-  │  │  drug-  │         │             │    │
│  │  │  │   app   │  │   app   │         │             │    │
│  │  │  └─────────┘  └─────────┘         │             │    │
│  │  └───────────────────────────────────┘             │    │
│  │                         │                           │    │
│  │                   Load Balancer                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 1. Terraform Setup (AWS Infrastructure)

### Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform >= 1.0 installed

### Configuration

Edit `terraform/terraform.tfvars`:
```hcl
aws_region       = "us-east-1"
environment      = "production"
project_name     = "drug-app"
instance_type    = "t3.medium"
min_nodes        = 2
max_nodes        = 5
desired_nodes    = 2
```

### Deploy Infrastructure

```bash
cd terraform

# Initialize Terraform
terraform init

# Plan the changes
terraform plan -out=tfplan

# Apply the configuration
terraform apply tfplan

# Get kubectl configuration
aws eks update-kubeconfig --region us-east-1 --name drug-app-eks
```

### Destroy Infrastructure

```bash
terraform destroy
```

## 2. Ansible Setup (Configuration Management)

### Prerequisites
- Ansible installed
- SSH access to servers

### Inventory Configuration

Edit `ansible/inventory.ini`:
```ini
[app]
app-server ansible_host=YOUR_IP ansible_user=ubuntu

[k8s]
k8s-master ansible_host=YOUR_IP ansible_user=ubuntu
k8s-node-1 ansible_host=YOUR_IP ansible_user=ubuntu
```

### Run Playbooks

```bash
cd ansible

# Setup Docker on all servers
ansible-playbook -i inventory.ini playbook-docker.yml

# Setup Kubernetes on all servers
ansible-playbook -i inventory.ini playbook-kubernetes.yml

# Deploy application
ansible-playbook -i inventory.ini playbook-deploy.yml

# Or run everything at once
ansible-playbook -i inventory.ini site.yml
```

## 3. Kubernetes Deployment

### Apply Manifests

```bash
# Create namespace and deploy
kubectl apply -f k8s/deployment.yaml

# Apply service
kubectl apply -f k8s/service.yaml

# Check deployment
kubectl get all -n drug-recommendation

# Watch pods
kubectl get pods -n drug-recommendation -w

# Get service info
kubectl get svc -n drug-recommendation
```

### Access the Application

```bash
# Port forward for local access
kubectl port-forward -n drug-recommendation svc/drug-recommendation-service 5000:5000

# Access the app
curl http://localhost:5000/health
```

## 4. Complete Workflow

### Option A: Full AWS EKS Deployment

```bash
# 1. Create infrastructure with Terraform
cd terraform
terraform init
terraform apply

# 2. Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name drug-app-eks

# 3. Deploy to Kubernetes
kubectl apply -f ../k8s/deployment.yaml
kubectl apply -f ../k8s/service.yaml

# 4. Check deployment
kubectl get all -n drug-recommendation
```

### Option B: Ansible with Docker

```bash
# 1. Setup servers
cd ansible
ansible-playbook -i inventory.ini playbook-docker.yml

# 2. Deploy app
ansible-playbook -i inventory.ini playbook-deploy.yml
```

## 5. GitHub Actions CI/CD

The CI/CD pipeline automatically:
1. Runs tests
2. Builds Docker image
3. Pushes to Docker Hub
4. Deploys to Kubernetes (on main branch)

### Required Secrets
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `KUBE_CONFIG` (for K8s deployment)

## File Structure

```
.
├── ansible/
│   ├── ansible.cfg
│   ├── inventory.ini
│   ├── site.yml
│   ├── playbook-docker.yml
│   ├── playbook-kubernetes.yml
│   └── playbook-deploy.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── .github/
    └── workflows/
        └── ci.yml
```
