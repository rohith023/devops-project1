# Docker Hub Auto-Build Setup

## Step 1: Create Docker Hub Repository

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click **Create Repository**
3. Name: `drug-app`
4. Visibility: Public (or Private)
5. Click **Create**

## Step 2: Link GitHub to Docker Hub

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click your profile → **Account Settings** → **Linked Accounts**
3. Click **Link GitHub**
4. Authorize Docker Hub to access your GitHub repositories
5. Select your organization/user and repo

## Step 3: Configure Auto-Build

1. Go to your Docker Hub repository
2. Click **Builds** tab
3. Click **Configure Automated Builds**
4. Under **Build Sources**, click **Link to GitHub**
5. Select:
   - **Repository**: `rohith023/devops-project1`
   - **GitHub Organization**: `rohith023`
6. Configure build rules:
   ```
   Type: Branch
   Name: main
   Docker Tag: latest
   
   Type: Branch  
   Name: develop
   Docker Tag: develop
   ```
7. Set **Dockerfile Location**: `/`
8. Set **Build Context**: `/`
9. Click **Save**

## Step 4: Add Secrets to GitHub

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (create at hub.docker.com/settings/security) |
| `KUBE_CONFIG` | Base64 encoded kubeconfig (optional, for K8s deploy) |

### Create Docker Hub Access Token:
1. Go to [Docker Hub](https://hub.docker.com/settings/security)
2. Click **New Access Token**
3. Name: `github-actions`
4. Copy the token and add as `DOCKERHUB_TOKEN` secret

## How It Works

### GitHub Actions Flow:
1. Push to `main/develop` triggers workflow
2. Runs tests
3. Builds Docker image
4. Pushes to Docker Hub

### Docker Hub Auto-Build Flow:
1. Push to GitHub triggers webhook
2. Docker Hub pulls code
3. Builds image from Dockerfile
4. Tags with branch name
5. Pushes to your repository

## Verify Setup

```bash
# Pull your image
docker pull YOUR_USERNAME/drug-app:latest

# Run it
docker run -p 5000:5000 YOUR_USERNAME/drug-app:latest
```
