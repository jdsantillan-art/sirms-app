# Django SIRMS Deployment Guide

## 🚀 Deploying to Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)
- Your Django project pushed to GitHub

### Step 1: Prepare Your Project

#### 1.1 Create `requirements.txt`
```bash
pip freeze > requirements.txt
```

#### 1.2 Create `runtime.txt` (optional)
```
python-3.11.0
```

#### 1.3 Update `settings.py` for Production

Add to the end of `sirms_project/settings.py`:

```python
import os
import dj_database_url

# Production settings
if os.environ.get('RAILWAY_ENVIRONMENT'):
    DEBUG = False
    ALLOWED_HOSTS = ['.railway.app', 'localhost', '127.0.0.1']
    
    # Database
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
    
    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'
    
    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

#### 1.4 Install Required Packages
```bash
pip install gunicorn dj-database-url psycopg2-binary whitenoise
pip freeze > requirements.txt
```

#### 1.5 Create `Procfile`
```
web: gunicorn sirms_project.wsgi --log-file -
```

#### 1.6 Create `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn sirms_project.wsgi",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 1.7 Update `settings.py` for Static Files
Add after STATIC_URL:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Step 2: Deploy to Railway

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to Railway**
   - Visit https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your SIRMS repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set DATABASE_URL

4. **Set Environment Variables**
   - Go to your project → Variables
   - Add:
     ```
     RAILWAY_ENVIRONMENT=production
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ```

5. **Deploy**
   - Railway will automatically deploy
   - Wait for build to complete
   - Click on the generated URL

6. **Create Superuser**
   - Go to project → Settings → Terminal
   - Run: `python manage.py createsuperuser`

---

## 🌐 Deploying to PythonAnywhere (Free Option)

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free account

### Step 2: Upload Your Code
1. Open a Bash console
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/sirms.git
   cd sirms
   ```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 sirms-env
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10

### Step 5: Configure WSGI File
Edit the WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/sirms/sirms'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sirms_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Set Up Static Files
In Web tab, set:
- URL: `/static/`
- Directory: `/home/yourusername/sirms/sirms/staticfiles`

### Step 7: Run Migrations
In Bash console:
```bash
cd sirms/sirms
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Step 8: Reload Web App
Click "Reload" button in Web tab

---

## 🔒 Security Checklist Before Deployment

- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for SECRET_KEY
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Set up HTTPS/SSL
- [ ] Use strong database passwords
- [ ] Enable CSRF protection
- [ ] Set secure cookie flags
- [ ] Configure CORS if needed
- [ ] Set up proper logging
- [ ] Use PostgreSQL (not SQLite) in production

---

## 📊 Database Migration

### From SQLite to PostgreSQL

1. **Dump existing data**
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **Update settings for PostgreSQL**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'sirms_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Load data**
   ```bash
   python manage.py loaddata data.json
   ```

---

## 🎯 Post-Deployment Tasks

1. **Test all features**
   - Login/logout
   - Report submission
   - Dashboard analytics
   - File uploads
   - Email notifications

2. **Set up monitoring**
   - Error tracking (Sentry)
   - Uptime monitoring
   - Performance monitoring

3. **Configure backups**
   - Database backups
   - Media files backups
   - Regular backup schedule

4. **Set up domain (optional)**
   - Purchase domain
   - Configure DNS
   - Set up SSL certificate

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Database | Best For |
|----------|-----------|-----------|----------|----------|
| PythonAnywhere | ✅ Limited | $5/mo | MySQL/PostgreSQL | Beginners |
| Railway | $5 credit | ~$5-10/mo | PostgreSQL | Modern apps |
| Render | ✅ (sleeps) | $7/mo | PostgreSQL | Production |
| Heroku | ❌ | $5-7/mo | PostgreSQL | Enterprise |
| DigitalOcean | ❌ | $5/mo | Managed DB | Scalable |

---

## 🆘 Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
python manage.py collectstatic --noinput
```

**2. Database connection error**
- Check DATABASE_URL environment variable
- Verify database credentials
- Ensure database is running

**3. 500 Internal Server Error**
- Check logs: `heroku logs --tail` or Railway logs
- Verify DEBUG=False
- Check ALLOWED_HOSTS

**4. Migration errors**
```bash
python manage.py migrate --run-syncdb
```

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Railway Django Guide](https://docs.railway.app/guides/django)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Render Django Guide](https://render.com/docs/deploy-django)

---

## 🎓 Recommended for School Project

**Best Choice: Railway**
- Easy setup
- Good free tier
- Professional features
- Great for portfolios

**Budget Choice: PythonAnywhere**
- Completely free to start
- Good for learning
- Can upgrade later

**Production Choice: Render or DigitalOcean**
- Reliable
- Scalable
- Professional support
