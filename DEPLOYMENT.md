# Deployment Guide

This guide covers deploying the GJ Terminal application to various platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [Production with Gunicorn](#production-with-gunicorn)
3. [Docker Deployment](#docker-deployment)
4. [Heroku](#heroku)
5. [AWS EC2](#aws-ec2)
6. [Google Cloud Run](#google-cloud-run)
7. [Railway/Render](#railwayrender)
8. [Nginx Configuration](#nginx-configuration)

---

## Local Development

### Quick Start

```bash
# Clone and setup
git clone https://github.com/anacondy/GJ-Terminal-csv-.git
cd GJ-Terminal-csv-

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database_setup.py

# Run development server
python app.py
```

Visit: `http://localhost:5000`

---

## Production with Gunicorn

### Prerequisites
- Linux/Unix server
- Python 3.8+
- Port 5000 available

### Installation

```bash
# Install gunicorn
pip install gunicorn

# Test run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Systemd Service (Recommended)

Create `/etc/systemd/system/gj-terminal.service`:

```ini
[Unit]
Description=GJ Terminal Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gj-terminal
Environment="PATH=/var/www/gj-terminal/venv/bin"
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=your-secret-key-here"
ExecStart=/var/www/gj-terminal/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable gj-terminal
sudo systemctl start gj-terminal
sudo systemctl status gj-terminal
```

---

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t gj-terminal .

# Run container
docker run -d -p 5000:5000 --name gj-terminal gj-terminal
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables

```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  --name gj-terminal \
  gj-terminal
```

---

## Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create gj-terminal-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Deploy
git push heroku main

# Open app
heroku open
```

### Post-deployment

```bash
# View logs
heroku logs --tail

# Scale dynos
heroku ps:scale web=1

# Restart app
heroku restart
```

---

## AWS EC2

### Launch EC2 Instance

1. Choose Ubuntu 22.04 LTS
2. Instance type: t2.micro (free tier)
3. Configure security group:
   - SSH (22): Your IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0

### Setup Script

```bash
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Create app directory
sudo mkdir -p /var/www/gj-terminal
sudo chown -R ubuntu:ubuntu /var/www/gj-terminal
cd /var/www/gj-terminal

# Clone repository
git clone https://github.com/anacondy/GJ-Terminal-csv-.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database_setup.py

# Install and configure Gunicorn
pip install gunicorn

# Create systemd service (see Production section)
# Configure Nginx (see Nginx section)
```

---

## Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Deployment

```bash
# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy gj-terminal \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SECRET_KEY=your-secret-key

# Get URL
gcloud run services describe gj-terminal --region us-central1 --format 'value(status.url)'
```

---

## Railway/Render

### Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
5. Deploy automatically detects Procfile

### Render

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect your repository
4. Settings:
   - Build Command: `pip install -r requirements.txt && python database_setup.py`
   - Start Command: `gunicorn app:app`
5. Add environment variables
6. Deploy

---

## Nginx Configuration

### Reverse Proxy Setup

Create `/etc/nginx/sites-available/gj-terminal`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/gj-terminal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

---

## Environment Variables

Set these for production:

```bash
# Required
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Optional
export PORT=5000
export DATABASE_URL=sqlite:///jobs.db
```

---

## Performance Optimization

### Gunicorn Workers

Calculate workers: `(2 * CPU_CORES) + 1`

```bash
# For 2 CPU cores:
gunicorn -w 5 -b 0.0.0.0:5000 app:app

# With threads:
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 app:app
```

### Database Optimization

For production, consider:
- Migrating to PostgreSQL
- Adding database indexes
- Implementing connection pooling

---

## Monitoring

### Health Check Endpoint

Add to `app.py`:

```python
@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '1.0.0'}, 200
```

### Logging

Configure production logging:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
```

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Permission denied:**
```bash
sudo chown -R $USER:$USER /var/www/gj-terminal
```

**Database locked:**
```bash
# SQLite doesn't handle concurrent writes well
# Consider PostgreSQL for production
```

**502 Bad Gateway:**
```bash
# Check if Gunicorn is running
systemctl status gj-terminal

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## Backup Strategy

### Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/gj-terminal"

mkdir -p $BACKUP_DIR
cp /var/www/gj-terminal/jobs.db $BACKUP_DIR/jobs_$DATE.db

# Keep only last 7 days
find $BACKUP_DIR -name "jobs_*.db" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

---

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Migrate to PostgreSQL
- Implement Redis for caching
- Use CDN for static assets

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Enable gzip compression
- Implement caching headers

---

## Support

For deployment issues:
- Check logs: `journalctl -u gj-terminal -f`
- Verify permissions: `ls -la /var/www/gj-terminal`
- Test connectivity: `curl -I http://localhost:5000`
- Check firewall: `sudo ufw status`

For platform-specific issues, consult:
- [Heroku Docs](https://devcenter.heroku.com/)
- [AWS EC2 Docs](https://docs.aws.amazon.com/ec2/)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
