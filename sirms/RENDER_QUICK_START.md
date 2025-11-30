# Render Deployment - Quick Start Checklist

## ✅ Pre-Deployment Checklist

- [ ] All code committed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render

## 🚀 Deployment Steps

### 1. Create PostgreSQL Database
```
Name: sirms-db
Database: sirms_db
User: sirms_user
```

### 2. Create Web Service
```
Name: sirms
Root Directory: sirms
Build Command: ./build.sh
Start Command: gunicorn sirms_project.wsgi:application
```

### 3. Set Environment Variables
```
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=<generate-random-key>
USE_POSTGRESQL=true
DATABASE_URL=<from-database>
ALLOWED_HOSTS=your-app.onrender.com
```

### 4. Deploy & Create Admin
```bash
# After deployment, in Render Shell:
python manage.py createsuperuser
```

## 🔑 Generate SECRET_KEY

Run in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 📝 Files Created for Deployment

- `build.sh` - Build script
- `runtime.txt` - Python version
- `render.yaml` - Service configuration
- `requirements.txt` - Updated with gunicorn, whitenoise, dj-database-url
- `settings.py` - Updated for production

## 🌐 Your App URL

After deployment: `https://your-app-name.onrender.com`

## ⚠️ Important Notes

- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Free PostgreSQL expires after 90 days
- Always use DEBUG=False in production

## 📚 Full Guide

See `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions.
