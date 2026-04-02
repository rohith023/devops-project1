#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io docker-compose

# Start Docker service
systemctl start docker
systemctl enable docker

# Add Ubuntu user to docker group
usermod -aG docker ubuntu

# Create application directory
mkdir -p /opt/drug-recommendation
cd /opt/drug-recommendation

# Run Docker container
docker run -d \
  --name drug-recommendation-app \
  --restart unless-stopped \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  ${docker_image}

# Install CloudWatch agent (optional)
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb

echo "EC2 instance setup completed successfully!"
