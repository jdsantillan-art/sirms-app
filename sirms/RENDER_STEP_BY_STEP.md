# Deploy SIRMS to Render - Simple Step-by-Step Guide

## What You'll Need
- GitHub account
- Render account (free at https://render.com)
- 15-20 minutes

---

## STEP 1: Push Your Code to GitHub

### 1.1 Create a new repository on GitHub
1. Go to https://github.com/new
2. Name it: `sirms-app` (or any name you prefer)
3. Keep it **Public** (required for free Render tier)
4. Don't initialize with README
5. Click "Create repository"

### 1.2 Push your code
Open your terminal in the `sirms` folder and run:

```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sirms-app.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## STEP 2: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with your GitHub account (easiest option)
4. Authorize Render to access your repositories

---

## STEP 3: Create PostgreSQL Database

**Do this FIRST before creating the web service!**

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Fill in:
   - **Name**: `sirms-db`
   - **Database**: `sirms_db`
   - **User**: `sirms_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait 2-3 minutes for database to be ready
6. **IMPORTANT**: Copy the **Internal Database URL** (you'll need this!)

---

## STEP 4: Create Web Service

1. Click **"New +"** again
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select your `sirms-app` repository
5. Click **"Connect"**

---

## STEP 5: Configure Web Service

Fill in these settings:

### Basic Info:
- **Name**: `sirms-app` (or your preferred name)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: `sirms` ← **IMPORTANT!**
- **Runtime**: `Python 3`

### Build & Deploy:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn sirms_project.wsgi:application`

### Instance Type:
- Select **"Free"** (or paid if you prefer)

---

## STEP 6: Add Environment Variables

Scroll down to **"Environment Variables"** section and add these:

Click **"Add Environment Variable"** for each:

1. **SECRET_KEY**
   - Value: Generate one using this Python command:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   - Copy the output and paste it here

2. **DEBUG**
   - Value: `False`

3. **USE_POSTGRESQL**
   - Value: `true`

4. **DATABASE_URL**
   - Click "Add from Database"
   - Select your `sirms-db` database
   - This automatically links your database!

5. **ALLOWED_HOSTS**
   - Value: `.onrender.com`

6. **PYTHON_VERSION**
   - Value: `3.11.0`

---

## STEP 7: Deploy!

1. Click **"Create Web Service"** at the bottom
2. Render will start building your app
3. Watch the logs - it will:
   - Install Python packages (2-3 minutes)
   - Collect static files
   - Run database migrations
   - Start your app

**First deployment takes 5-10 minutes. Be patient!**

---

## STEP 8: Create Admin User

Once deployment succeeds:

1. In your web service page, click the **"Shell"** tab
2. Type this command:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create username, email, and password
4. Press Enter when done

---

## STEP 9: Access Your App!

Your app is now live at:
```
https://sirms-app.onrender.com
```
(Replace `sirms-app` with your actual service name)

### Test it:
1. Visit the URL
2. Try logging in with your superuser account
3. Check if everything works!

---

## STEP 10: Update Google OAuth (If Using)

If you're using Google login:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to "Credentials"
4. Edit your OAuth 2.0 Client ID
5. Add to **Authorized redirect URIs**:
   ```
   https://sirms-app.onrender.com/auth/callback/
   ```
6. Add to **Authorized JavaScript origins**:
   ```
   https://sirms-app.onrender.com
   ```
7. Save changes

8. Update environment variables in Render:
   - Add `GOOGLE_OAUTH_REDIRECT_URI` = `https://sirms-app.onrender.com/auth/callback/`

---

## Common Issues & Solutions

### ❌ Build Failed
- Check the logs for specific error
- Make sure `Root Directory` is set to `sirms`
- Verify `build.sh` has correct permissions

### ❌ Database Connection Error
- Make sure DATABASE_URL is linked correctly
- Check that PostgreSQL database is running
- Verify USE_POSTGRESQL=true

### ❌ Static Files Not Loading
- Check if collectstatic ran in build logs
- Verify whitenoise is in requirements.txt
- Check STATIC_ROOT setting

### ❌ App is Slow
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Consider upgrading to paid tier ($7/month) for always-on

---

## Updating Your App

To deploy changes:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Render automatically detects and deploys!
4. Watch the deployment in Render dashboard

---

## Important Notes

### Free Tier Limitations:
- ⏰ Spins down after 15 minutes of inactivity
- 🗄️ Database expires after 90 days (backup your data!)
- 💾 750 hours/month of runtime
- 🌐 Shared IP address

### Security Checklist:
- ✅ DEBUG is False
- ✅ SECRET_KEY is random and secure
- ✅ ALLOWED_HOSTS is configured
- ✅ Using HTTPS (automatic on Render)
- ✅ Database credentials are secure

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Render Community**: https://community.render.com

---

## Congratulations! 🎉

Your SIRMS app is now live and accessible from anywhere in the world!

Share your URL: `https://sirms-app.onrender.com`
