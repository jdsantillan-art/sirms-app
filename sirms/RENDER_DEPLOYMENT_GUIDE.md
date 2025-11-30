# SIRMS Render Deployment Guide

This guide will walk you through deploying your SIRMS Django application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Step 1: Prepare Your Repository

Make sure all the deployment files are committed to your GitHub repository:
- `build.sh` - Build script for Render
- `runtime.txt` - Python version specification
- `render.yaml` - Render service configuration
- `requirements.txt` - Updated with gunicorn, whitenoise, and dj-database-url

## Step 2: Push to GitHub

```bash
cd sirms
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 3: Create a New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select your SIRMS repository

## Step 4: Configure Your Web Service

### Basic Settings:
- **Name**: `sirms` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `sirms`
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn sirms_project.wsgi:application`

### Environment Variables:
Add these in the "Environment" section:

```
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=<generate-a-strong-random-key>
USE_POSTGRESQL=true
ALLOWED_HOSTS=your-app-name.onrender.com
```

To generate a secure SECRET_KEY, run this in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 5: Create PostgreSQL Database

1. In Render dashboard, click "New +" and select "PostgreSQL"
2. **Name**: `sirms-db`
3. **Database**: `sirms_db`
4. **User**: `sirms_user`
5. Click "Create Database"

## Step 6: Link Database to Web Service

1. Go back to your web service settings
2. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Select "Add from Database" → Choose your `sirms-db`

## Step 7: Configure Google OAuth (Optional)

If you're using Google OAuth, add these environment variables:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_REDIRECT_URI=https://your-app-name.onrender.com/auth/callback/
```

Update your Google OAuth settings:
1. Go to Google Cloud Console
2. Add your Render URL to authorized redirect URIs
3. Add your Render domain to authorized JavaScript origins

## Step 8: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application

## Step 9: Create Superuser

After deployment, you need to create an admin user:

1. Go to your web service in Render dashboard
2. Click "Shell" tab
3. Run:
```bash
python manage.py createsuperuser
```

## Step 10: Verify Deployment

Visit your app at: `https://your-app-name.onrender.com`

## Important Notes

### Free Tier Limitations:
- Free web services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Free PostgreSQL databases have 90-day expiration

### Production Checklist:
- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Set up proper email backend
- [ ] Configure CSRF_TRUSTED_ORIGINS if needed
- [ ] Set up media file storage (consider AWS S3)
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up monitoring and logging

## Troubleshooting

### Build Fails:
- Check build logs in Render dashboard
- Verify all dependencies in requirements.txt
- Ensure build.sh has execute permissions

### Database Connection Issues:
- Verify DATABASE_URL is set correctly
- Check PostgreSQL database is running
- Ensure USE_POSTGRESQL=true

### Static Files Not Loading:
- Verify STATIC_ROOT and STATIC_URL settings
- Check whitenoise is in MIDDLEWARE
- Run `python manage.py collectstatic` manually in shell

### Application Errors:
- Check logs in Render dashboard
- Enable DEBUG temporarily to see detailed errors
- Verify all environment variables are set

## Updating Your Application

To deploy updates:
1. Push changes to GitHub
2. Render automatically detects and deploys changes
3. Or manually trigger deploy in Render dashboard

## Custom Domain (Optional)

1. Go to your web service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed
5. Update ALLOWED_HOSTS environment variable

## Monitoring

- View logs: Render Dashboard → Your Service → Logs
- Monitor metrics: Dashboard shows CPU, memory, and bandwidth
- Set up alerts for downtime or errors

## Cost Optimization

For production use, consider:
- Upgrading to paid tier ($7/month) for always-on service
- Using managed PostgreSQL ($7/month) for persistence
- Implementing caching (Redis) for better performance

## Support

- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Community: Render Community Forum

---

Your SIRMS application is now deployed and accessible worldwide!
