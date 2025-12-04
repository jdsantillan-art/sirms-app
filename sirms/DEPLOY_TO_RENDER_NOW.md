# 🚀 Deploy SIRMS to Render - Step by Step Guide

## ✅ Prerequisites Checklist

- [x] All code changes committed
- [x] GitHub repository ready
- [x] Render account (sign up at https://render.com if needed)

---

## 📋 Step 1: Prepare Your Code

### 1.1 Ensure all files are committed to Git

```bash
cd sirms
git status
```

If you have uncommitted changes:

```bash
git add .
git commit -m "Ready for Render deployment - VRF and Counseling Schedule features"
```

### 1.2 Push to GitHub

```bash
git push origin main
```

---

## 🌐 Step 2: Create Render Account & Connect GitHub

1. Go to https://dashboard.render.com
2. Sign up or log in
3. Click "New +" → "Blueprint"
4. Connect your GitHub account if not already connected
5. Select your SIRMS repository

---

## 🗄️ Step 3: Create PostgreSQL Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `sirms-db`
   - **Database**: `sirms_db`
   - **User**: `sirms_user`
   - **Region**: Choose closest to your users
3. Click "Create Database"
4. **Wait for database to be ready** (takes 1-2 minutes)
5. Copy the **Internal Database URL** (you'll need it)

---

## ⚙️ Step 4: Create Web Service

### Option A: Using Blueprint (Recommended - Automatic)

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repository
3. Select the repository containing your SIRMS code
4. Render will detect `render.yaml` automatically
5. Review the configuration:
   - **Name**: `sirms`
   - **Root Directory**: `sirms` (if your code is in a subdirectory)
   - **Build Command**: `./build.sh`
   - **Start Command**: Already set in render.yaml
6. Click "Apply"

### Option B: Manual Setup

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `sirms`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `sirms`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn sirms_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 --graceful-timeout 600 --worker-class sync --max-requests 1000`

---

## 🔐 Step 5: Configure Environment Variables

In your Web Service settings, go to "Environment" and add:

### Required Variables:

```
PYTHON_VERSION=3.11.0
DEBUG=False
USE_POSTGRESQL=true
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Database Connection:

- **Key**: `DATABASE_URL`
- **Value**: Click "Add from Database" → Select `sirms-db`

### Secret Key:

- **Key**: `SECRET_KEY`
- **Value**: Generate using:
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
  Or let Render auto-generate it (already configured in render.yaml)

### Optional: Email Configuration (if using email notifications):

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <noreply@dmlmhs.edu.ph>
SITE_URL=https://your-app-name.onrender.com
```

### Optional: Google OAuth (if using):

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_REDIRECT_URI=https://your-app-name.onrender.com/auth/callback/
```

---

## 🚀 Step 6: Deploy

1. Click "Create Web Service" or "Apply" (if using Blueprint)
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run `build.sh` script:
     - Collect static files
     - Run database migrations
     - Load initial data
     - Create staff accounts
3. **First deployment takes 5-10 minutes**
4. Monitor the logs for any errors

---

## ✅ Step 7: Verify Deployment

### 7.1 Check Health Endpoint

Visit: `https://your-app-name.onrender.com/health/`

Should return: `{"status": "ok", "service": "sirms"}`

### 7.2 Access Your Application

Visit: `https://your-app-name.onrender.com/`

### 7.3 Test Login

Use the pre-created staff accounts:

**Guidance Counselor:**
- Email: `dmlmhs.guidance@gmail.com`
- Password: `dmlmhsguidance000`

**Discipline Officer:**
- Email: `dmlmhs.do@gmail.com`
- Password: `dmlmhsdo000`

**ESP Teachers:**
- Email: `garcia.espteacher@gmail.com` (or other ESP teachers)
- Password: `dmlmhsesp000`

---

## 🔧 Step 8: Post-Deployment Tasks

### 8.1 Create Superuser (Admin)

1. Go to Render dashboard → Your Web Service → "Shell"
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin account

### 8.2 Verify Features

- [ ] VRF cases routing to ESP Teacher dashboard
- [ ] "For Vrf" sidebar showing VRF cases
- [ ] Counseling Schedule sidebar showing non-VRF cases
- [ ] Case evaluation working correctly
- [ ] All user roles can access their dashboards

---

## 🐛 Troubleshooting

### Build Fails

1. Check build logs in Render dashboard
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Build script errors
   - Database connection issues

### Application Won't Start

1. Check runtime logs
2. Verify:
   - `DATABASE_URL` is set correctly
   - `SECRET_KEY` is set
   - `ALLOWED_HOSTS` includes your Render URL

### Database Connection Errors

1. Verify database is running
2. Check `DATABASE_URL` environment variable
3. Ensure database user has proper permissions

### Static Files Not Loading

1. Verify `collectstatic` ran successfully
2. Check `STATIC_ROOT` in settings.py
3. Ensure WhiteNoise is configured

---

## 📊 Monitoring

### View Logs

1. Go to Render dashboard → Your Web Service
2. Click "Logs" tab
3. Monitor for errors or warnings

### Check Metrics

- CPU usage
- Memory usage
- Response times
- Request counts

---

## 🔄 Updating Your Deployment

When you make changes:

1. Commit changes to Git:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. Render will automatically:
   - Detect the push
   - Start a new deployment
   - Build and deploy your changes

3. Monitor the deployment in Render dashboard

---

## 📝 Important Notes

1. **Free Tier Limitations:**
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - Consider upgrading for production use

2. **Database Backups:**
   - Enable automatic backups in Render dashboard
   - Database → Settings → Backups

3. **Environment Variables:**
   - Never commit secrets to Git
   - Always use environment variables for sensitive data

4. **Static Files:**
   - WhiteNoise handles static files
   - No need for separate CDN on free tier

---

## 🎉 Success!

Your SIRMS application should now be live on Render!

**Your Application URL:** `https://your-app-name.onrender.com`

**Next Steps:**
- Share the URL with your team
- Test all features
- Monitor performance
- Set up custom domain (optional)

---

## 📞 Need Help?

- Render Documentation: https://render.com/docs
- Render Support: https://render.com/support
- Check deployment logs for specific errors
