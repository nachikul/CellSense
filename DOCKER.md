# CellSense Docker Deployment Guide

## 🐳 Quick Start with Docker

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 1.29+)

### Running with Docker Compose (Recommended)

1. **Build and start all services:**
```bash
docker-compose up -d
```

2. **Access the application:**
- Frontend: http://localhost
- Backend API: http://localhost:8000

3. **View logs:**
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

4. **Stop the application:**
```bash
docker-compose down
```

5. **Rebuild after changes:**
```bash
docker-compose up -d --build
```

### Running Individual Containers

**Backend:**
```bash
cd backend
docker build -t cellsense-backend .
docker run -d -p 8000:8000 --name cellsense-backend cellsense-backend
```

**Frontend:**
```bash
cd frontend
docker build -t cellsense-frontend .
docker run -d -p 80:80 --name cellsense-frontend --link cellsense-backend:backend cellsense-frontend
```

## 🌐 Production Deployment

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
BACKEND_PORT=8000
PYTHONUNBUFFERED=1

# Frontend
FRONTEND_PORT=80

# Optional: AI API Configuration
HUGGINGFACE_API_KEY=your_api_key_here
```

### Using Custom Ports

Modify `docker-compose.yml` ports section:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to your desired port
  
  frontend:
    ports:
      - "8080:80"    # Change 8080 to your desired port
```

### Production Best Practices

1. **Use a reverse proxy (nginx/traefik) for SSL/TLS**
2. **Set up persistent volumes for uploads:**
```yaml
volumes:
  - ./data/uploads:/app/uploads
```

3. **Configure resource limits:**
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

4. **Use Docker secrets for sensitive data**
5. **Enable automatic restarts:** `restart: always`

## 🔒 Security Considerations

- Change default ports in production
- Use environment variables for secrets
- Enable HTTPS with Let's Encrypt
- Limit file upload sizes
- Implement rate limiting
- Regular security updates: `docker-compose pull && docker-compose up -d`

## 📊 Monitoring

**Check container health:**
```bash
docker-compose ps
```

**View resource usage:**
```bash
docker stats
```

## 🛠️ Troubleshooting

**Container won't start:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Clear and rebuild:**
```bash
docker-compose down -v
docker-compose up -d --build --force-recreate
```

**Access container shell:**
```bash
docker exec -it cellsense-backend /bin/bash
docker exec -it cellsense-frontend /bin/sh
```

## 🚀 Cloud Deployment

### Deploy to Cloud Platforms

**AWS (ECS/EC2):**
- Use AWS ECR for container registry
- Deploy with ECS or EC2 with Docker installed

**Google Cloud (Cloud Run):**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/cellsense-backend
gcloud run deploy --image gcr.io/PROJECT-ID/cellsense-backend
```

**Azure (Container Instances):**
```bash
az container create --resource-group myResourceGroup \
  --name cellsense --image cellsense:latest
```

**DigitalOcean (App Platform):**
- Push to GitHub/GitLab
- Connect repository to App Platform
- Auto-deploy from Dockerfile

## 📝 Maintenance

**Update to latest version:**
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

**Backup data:**
```bash
docker run --rm -v cellsense_uploads:/data -v $(pwd):/backup ubuntu tar czf /backup/uploads-backup.tar.gz /data
```

**Restore data:**
```bash
docker run --rm -v cellsense_uploads:/data -v $(pwd):/backup ubuntu tar xzf /backup/uploads-backup.tar.gz -C /
```
