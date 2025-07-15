# Deployment Guide

This guide covers various deployment options for StrategySim AI, from local development to production environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (or other LLM provider)
- Git

### Local Installation

```bash
# Clone repository
git clone https://github.com/zhengshui/strategy-sim.git
cd strategy-sim

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run application
chainlit run app.py
```

Access the application at `http://localhost:8000`

## Local Development

### Development Environment Setup

1. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Configure environment variables**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   
   # Required variables
   OPENAI_API_KEY=sk-your-api-key-here
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```

4. **Run tests**:
   ```bash
   python run_tests.py
   ```

5. **Start development server**:
   ```bash
   chainlit run app.py --auto-reload
   ```

### Development Commands

```bash
# Run tests with coverage
python run_tests.py --coverage

# Format code
black .

# Lint code
ruff check .

# Type checking
mypy src/

# Run specific test suite
python run_tests.py --unit
python run_tests.py --integration
```

## Production Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database configured (if using persistence)
- [ ] HTTPS enabled
- [ ] Authentication configured
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Log rotation configured
- [ ] Resource limits set

### Environment Configuration

Create a production `.env` file:

```env
# Model Configuration
OPENAI_API_KEY=sk-your-production-api-key
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=production

# Chainlit Configuration
CHAINLIT_HOST=0.0.0.0
CHAINLIT_PORT=8000
CHAINLIT_AUTH_SECRET=your-secure-secret-key

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/strategysim

# Security
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=your-domain.com,api.your-domain.com

# Monitoring
SENTRY_DSN=your-sentry-dsn
ANALYTICS_ENABLED=true
```

### Production Installation

```bash
# Install production dependencies
pip install -e .

# Set up systemd service (Linux)
sudo cp deployment/strategysim.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable strategysim
sudo systemctl start strategysim

# Or use process manager
pm2 start ecosystem.config.js
```

### Systemd Service Configuration

Create `/etc/systemd/system/strategysim.service`:

```ini
[Unit]
Description=StrategySim AI Multi-Agent Decision System
After=network.target

[Service]
Type=simple
User=strategysim
Group=strategysim
WorkingDirectory=/opt/strategysim
Environment=PATH=/opt/strategysim/venv/bin
ExecStart=/opt/strategysim/venv/bin/chainlit run app.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Docker Deployment

### Docker Images

#### Production Dockerfile

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install application
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 strategysim
USER strategysim

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
```

#### Development Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy application code
COPY . .

# Install application in development mode
RUN pip install -e ".[dev]"

# Expose port
EXPOSE 8000

# Development command with auto-reload
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000", "--auto-reload"]
```

### Docker Compose

#### Production docker-compose.yml

```yaml
version: '3.8'

services:
  strategysim:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://strategysim:password@db:5432/strategysim
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=strategysim
      - POSTGRES_USER=strategysim
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - strategysim
    restart: unless-stopped

volumes:
  postgres_data:
```

#### Development docker-compose.dev.yml

```yaml
version: '3.8'

services:
  strategysim:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    volumes:
      - .:/app
      - /app/venv
    command: chainlit run app.py --host 0.0.0.0 --port 8000 --auto-reload
```

### Docker Commands

```bash
# Build and run production
docker-compose up -d

# Build and run development
docker-compose -f docker-compose.dev.yml up

# View logs
docker-compose logs -f strategysim

# Scale service
docker-compose up -d --scale strategysim=3

# Update service
docker-compose pull
docker-compose up -d

# Backup database
docker-compose exec db pg_dump -U strategysim strategysim > backup.sql
```

## Cloud Deployment

### AWS Deployment

#### EC2 Deployment

1. **Launch EC2 instance**:
   ```bash
   # Amazon Linux 2
   sudo yum update -y
   sudo yum install -y python3 python3-pip git
   ```

2. **Install application**:
   ```bash
   git clone https://github.com/zhengshui/strategy-sim.git
   cd strategy-sim
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. **Configure nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

#### ECS Deployment

1. **Create task definition**:
   ```json
   {
     "family": "strategysim",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "strategysim",
         "image": "your-account.dkr.ecr.region.amazonaws.com/strategysim:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "OPENAI_API_KEY",
             "value": "your-api-key"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/strategysim",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

2. **Create service**:
   ```bash
   aws ecs create-service \
     --cluster your-cluster \
     --service-name strategysim \
     --task-definition strategysim:1 \
     --desired-count 2 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
   ```

### Google Cloud Deployment

#### Cloud Run Deployment

1. **Build and push image**:
   ```bash
   gcloud builds submit --tag gcr.io/your-project/strategysim
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy strategysim \
     --image gcr.io/your-project/strategysim \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-api-key
   ```

#### GKE Deployment

1. **Create deployment**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: strategysim
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: strategysim
     template:
       metadata:
         labels:
           app: strategysim
       spec:
         containers:
         - name: strategysim
           image: gcr.io/your-project/strategysim:latest
           ports:
           - containerPort: 8000
           env:
           - name: OPENAI_API_KEY
             valueFrom:
               secretKeyRef:
                 name: strategysim-secrets
                 key: openai-api-key
   ```

2. **Create service**:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: strategysim-service
   spec:
     selector:
       app: strategysim
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer
   ```

### Azure Deployment

#### Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name strategysim \
  --image your-registry.azurecr.io/strategysim:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your-api-key \
  --dns-name-label strategysim-app
```

#### App Service

```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name strategysim-app \
  --deployment-container-image-name your-registry.azurecr.io/strategysim:latest

az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name strategysim-app \
  --settings OPENAI_API_KEY=your-api-key
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | None | Yes |
| `MODEL_PROVIDER` | Model provider | `openai` | No |
| `MODEL_NAME` | Model name | `gpt-4` | No |
| `DEBUG` | Debug mode | `false` | No |
| `LOG_LEVEL` | Log level | `INFO` | No |
| `CHAINLIT_HOST` | Host address | `0.0.0.0` | No |
| `CHAINLIT_PORT` | Port number | `8000` | No |
| `DATABASE_URL` | Database URL | None | No |
| `REDIS_URL` | Redis URL | None | No |

### Model Configuration

Create `model_config.yaml`:

```yaml
model_type: "openai"
model: "gpt-4"
api_key: "${OPENAI_API_KEY}"
base_url: "https://api.openai.com/v1"
temperature: 0.7
max_tokens: 4000
timeout: 30
retry_attempts: 3
```

### Database Configuration

For production deployments with persistence:

```python
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/strategysim

# MongoDB
DATABASE_URL=mongodb://user:password@localhost:27017/strategysim

# SQLite (development)
DATABASE_URL=sqlite:///./strategysim.db
```

## Monitoring

### Health Checks

The application provides health check endpoints:

```python
# Health check endpoint
GET /health

# Response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "0.1.0",
  "components": {
    "database": "healthy",
    "model_api": "healthy",
    "agents": "healthy"
  }
}
```

### Logging

Configure structured logging:

```python
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### Metrics

Key metrics to monitor:

- **Request Rate**: Requests per second
- **Response Time**: Average response time
- **Error Rate**: Error percentage
- **Agent Performance**: Analysis completion time
- **Model Usage**: Token consumption
- **Memory Usage**: Application memory usage
- **CPU Usage**: CPU utilization

### Alerting

Set up alerts for:

- High error rates (>5%)
- Slow response times (>30s)
- High memory usage (>80%)
- API key quota exceeded
- Model API errors

## Security

### Authentication

Configure authentication:

```python
# Environment variables
CHAINLIT_AUTH_SECRET=your-secret-key
ENABLE_AUTHENTICATION=true
AUTH_PROVIDER=oauth2

# OAuth2 configuration
OAUTH2_CLIENT_ID=your-client-id
OAUTH2_CLIENT_SECRET=your-client-secret
OAUTH2_REDIRECT_URI=https://your-domain.com/auth/callback
```

### HTTPS Configuration

Nginx SSL configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Headers

Add security headers:

```python
# Security middleware
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
}
```

### API Key Security

Secure API key management:

```bash
# Use environment variables
export OPENAI_API_KEY=sk-your-api-key

# Or use secret management
kubectl create secret generic strategysim-secrets \
  --from-literal=openai-api-key=sk-your-api-key

# AWS Secrets Manager
aws secretsmanager create-secret \
  --name strategysim/openai-api-key \
  --secret-string sk-your-api-key
```

## Troubleshooting

### Common Issues

#### 1. API Key Errors

```
Error: OpenAI API key not found
```

**Solution**:
```bash
# Check environment variable
echo $OPENAI_API_KEY

# Set environment variable
export OPENAI_API_KEY=sk-your-api-key

# Or add to .env file
echo "OPENAI_API_KEY=sk-your-api-key" >> .env
```

#### 2. Port Already in Use

```
Error: Port 8000 already in use
```

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
chainlit run app.py --port 8001
```

#### 3. Memory Issues

```
Error: Out of memory
```

**Solution**:
```bash
# Increase memory limit
docker run -m 4g strategysim

# Or optimize model parameters
MODEL_MAX_TOKENS=2000
MODEL_TEMPERATURE=0.5
```

#### 4. Database Connection Issues

```
Error: Could not connect to database
```

**Solution**:
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check database service
docker-compose logs db
```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Set environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run with debug
chainlit run app.py --debug
```

### Log Analysis

Common log patterns:

```bash
# Filter error logs
grep "ERROR" logs/app.log

# Check agent performance
grep "analysis_duration" logs/app.log

# Monitor API calls
grep "openai" logs/app.log
```

### Performance Tuning

Optimize performance:

```python
# Reduce model parameters
MODEL_MAX_TOKENS=2000
MODEL_TEMPERATURE=0.3

# Enable caching
ENABLE_CACHE=true
CACHE_TTL=3600

# Optimize agent turns
MAX_AGENT_TURNS=15
```

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump $DATABASE_URL > backup.sql

# MongoDB backup
mongodump --uri $DATABASE_URL --out backup/

# Restore
psql $DATABASE_URL < backup.sql
mongorestore --uri $DATABASE_URL backup/
```

### Application Backup

```bash
# Backup configuration
tar -czf config-backup.tar.gz .env model_config.yaml

# Backup reports
tar -czf reports-backup.tar.gz reports/

# Backup logs
tar -czf logs-backup.tar.gz logs/
```

## Scaling

### Horizontal Scaling

```yaml
# Kubernetes scaling
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strategysim
spec:
  replicas: 5
  
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: strategysim-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: strategysim
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing

```nginx
upstream strategysim {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://strategysim;
    }
}
```

This deployment guide provides comprehensive instructions for deploying StrategySim AI in various environments. For specific deployment questions, please refer to the [API documentation](API.md) or open an issue on GitHub.