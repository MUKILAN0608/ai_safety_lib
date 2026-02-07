# Deployment Guide

This guide covers various deployment scenarios for the AI Safety Library.

## Table of Contents
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring Setup](#monitoring-setup)

## Local Development

### Setup
```bash
# Clone repository
git clone https://github.com/MUKILAN0608/ai_safety_lib.git
cd ai_safety_lib

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[all,dev]"

# Run tests
pytest tests/ -v
```

### Run API Server
```bash
# Development mode with auto-reload
python api_server.py

# Or using uvicorn directly
uvicorn api_server:app --reload --port 8000
```

## Production Deployment

### Prerequisites
- Python 3.8+
- pip or conda
- Virtual environment (recommended)

### Installation
```bash
# Install production dependencies
pip install ai-safety-lib[api]

# Or from source
pip install -e ".[api]"
```

### Run with Uvicorn
```bash
# Single worker
uvicorn api_server:app --host 0.0.0.0 --port 8000

# Multiple workers for production
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4

# With SSL
uvicorn api_server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --ssl-keyfile=/path/to/key.pem \
  --ssl-certfile=/path/to/cert.pem \
  --workers 4
```

### Run with Gunicorn
```bash
pip install gunicorn

gunicorn api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t ai-safety-api:latest .
```

### Run Container
```bash
# Basic run
docker run -p 8000:8000 ai-safety-api:latest

# With environment variables
docker run -p 8000:8000 \
  -e SAFETY_CONFIDENCE_THRESHOLD=0.75 \
  -e SAFETY_DRIFT_THRESHOLD=0.25 \
  ai-safety-api:latest

# With volume for logs
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  ai-safety-api:latest
```

### Docker Compose
```bash
# Start all services (API + Monitoring)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Cloud Deployment

### AWS ECS/Fargate

1. **Build and Push Image**
```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t ai-safety-api .
docker tag ai-safety-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/ai-safety-api:latest

# Push
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/ai-safety-api:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "ai-safety-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "ai-safety-api",
      "image": "<account>.dkr.ecr.us-east-1.amazonaws.com/ai-safety-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SAFETY_CONFIDENCE_THRESHOLD",
          "value": "0.7"
        }
      ]
    }
  ]
}
```

### Azure Container Instances

```bash
# Create resource group
az group create --name ai-safety-rg --location eastus

# Deploy container
az container create \
  --resource-group ai-safety-rg \
  --name ai-safety-api \
  --image ai-safety-api:latest \
  --dns-name-label ai-safety-api \
  --ports 8000 \
  --environment-variables \
    SAFETY_CONFIDENCE_THRESHOLD=0.7 \
    SAFETY_DRIFT_THRESHOLD=0.3
```

### Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/<project-id>/ai-safety-api

# Deploy to Cloud Run
gcloud run deploy ai-safety-api \
  --image gcr.io/<project-id>/ai-safety-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars SAFETY_CONFIDENCE_THRESHOLD=0.7
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-safety-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-safety-api
  template:
    metadata:
      labels:
        app: ai-safety-api
    spec:
      containers:
      - name: ai-safety-api
        image: ai-safety-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: SAFETY_CONFIDENCE_THRESHOLD
          value: "0.7"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-safety-api-service
spec:
  selector:
    app: ai-safety-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

## Monitoring Setup

### Prometheus Configuration

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-safety-api'
    static_configs:
      - targets: ['api:8000']
```

### Grafana Dashboard

1. Access Grafana: http://localhost:3000
2. Default credentials: admin/admin
3. Add Prometheus data source: http://prometheus:9090
4. Import dashboard or create custom panels

### Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Readiness probe
curl http://localhost:8000/

# Liveness probe
curl http://localhost:8000/health
```

### Logging

```python
# Configure logging in production
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SAFETY_CONFIDENCE_THRESHOLD` | 0.7 | Minimum confidence threshold |
| `SAFETY_DRIFT_THRESHOLD` | 0.3 | Maximum drift threshold |
| `SAFETY_ALLOW_WARNING` | false | Allow deployment with warnings |
| `MONITORING_ENABLE_ALERTS` | true | Enable alerting system |

## Performance Tuning

### Uvicorn Workers
- Use `--workers N` where N = (2 x CPU cores) + 1
- Each worker uses ~200-300MB RAM

### Resource Requirements

| Deployment Size | CPU | Memory | Workers |
|----------------|-----|--------|---------|
| Small | 1 core | 512MB | 2 |
| Medium | 2 cores | 1GB | 4 |
| Large | 4 cores | 2GB | 8 |

## Security Considerations

1. **Use HTTPS in production**
2. **Set up authentication/authorization**
3. **Enable rate limiting**
4. **Regular security updates**
5. **Environment variable encryption**
6. **Network security (VPC, firewall)**

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Kill the process or use different port
uvicorn api_server:app --port 8001
```

**Import errors:**
```bash
# Reinstall package
pip install -e ".[all]" --force-reinstall
```

**Container won't start:**
```bash
# Check logs
docker logs <container-id>

# Run interactively
docker run -it ai-safety-api /bin/bash
```

## Backup and Recovery

### Database Backups (if applicable)
```bash
# Backup configuration
cp config.yaml config.yaml.backup

# Export audit logs
curl http://localhost:8000/audit-log > audit_backup.json
```

## Load Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test with 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/health

# Or use k6
k6 run load-test.js
```

## Scaling Strategy

1. **Horizontal Scaling**: Add more container instances
2. **Vertical Scaling**: Increase CPU/memory per instance
3. **Load Balancing**: Use nginx or cloud load balancers
4. **Caching**: Add Redis for frequently accessed data
5. **Database**: Consider PostgreSQL for persistent storage

---

For additional help, see the [documentation](../README.md) or [open an issue](https://github.com/MUKILAN0608/ai_safety_lib/issues).
