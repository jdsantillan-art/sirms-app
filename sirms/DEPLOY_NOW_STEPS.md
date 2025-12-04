# 🚀 Deploy to Render - Step by Step Instructions

## ✅ GitHub Status: READY
Your code is already pushed to GitHub: `https://github.com/jdsantillan-art/sirms-app.git`

---

## 📋 Step-by-Step Render Deployment

### Step 1: Go to Render Dashboard
👉 **Open:** https://dashboard.render.com

### Step 2: Sign In or Create Account
- If you don't have an account, click "Get Started for Free"
- Sign in with GitHub (recommended for easy repository access)

### Step 3: Create Blueprint (Easiest Method)

1. **Click "New +"** button (top right)
2. **Select "Blueprint"**
3. **Connect GitHub** (if not already connected):
   - Click "Connect GitHub"
   - Authorize Render to access your repositories
4. **Select Repository:**
   - Find and select: `jdsantillan-art/sirms-app`
5. **Review Configuration:**
   - Render will automatically detect `render.yaml`
   - **Name:** `sirms` (or your preferred name)
   - **Root Directory:** `sirms` (important - your code is in the sirms subdirectory)
6. **Click "Apply"**

### Step 4: Wait for Deployment
⏱️ **First deployment takes 5-10 minutes**

Render will automatically:
- ✅ Create PostgreSQL database (`sirms-db`)
- ✅ Install dependencies from `requirements.txt`
- ✅ Run `build.sh` script:
  - Collect static files
  - Run database migrations
  - Load initial data
  - Create staff accounts
- ✅ Start your web service

### Step 5: Monitor Deployment

1. **Watch the Logs:**
   - Click on your service name
   - Go to "Logs" tab
   - Monitor for any errors

2. **Check Build Status:**
   - Green checkmark = Success
   - Red X = Error (check logs)

### Step 6: Access Your Application

Once deployment is complete:
- **Your App URL:** `https://sirms.onrender.com` (or your chosen name)
- **Health Check:** `https://sirms.onrender.com/health/`

---

## 🔐 Default Login Credentials

After deployment, these accounts are automatically created:

### Guidance Counselor
- **Email:** `dmlmhs.guidance@gmail.com`
- **Password:** `dmlmhsguidance000`

### Discipline Officer
- **Email:** `dmlmhs.do@gmail.com`
- **Password:** `dmlmhsdo000`

### ESP Teachers
- **Email:** `garcia.espteacher@gmail.com` (and 4 others)
- **Password:** `dmlmhsesp000`

---

## ⚙️ Environment Variables (Auto-Configured)

The `render.yaml` file automatically sets:
- ✅ `PYTHON_VERSION=3.11.0`
- ✅ `USE_POSTGRESQL=true`
- ✅ `DATABASE_URL` (from database)
- ✅ `SECRET_KEY` (auto-generated)
- ✅ `DEBUG=false`
- ✅ `ALLOWED_HOSTS` (auto-set)

---

## 🔧 Optional: Add Email Configuration

If you want email notifications, add these in Render Dashboard → Your Service → Environment:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <noreply@dmlmhs.edu.ph>
SITE_URL=https://sirms.onrender.com
```

---

## 🐛 Troubleshooting

### Build Fails
1. Check "Logs" tab in Render dashboard
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Build script error → Check `build.sh`
   - Database connection → Verify `DATABASE_URL`

### Application Won't Start
1. Check runtime logs
2. Verify:
   - Database is running
   - `DATABASE_URL` is set
   - `SECRET_KEY` is set

### Static Files Not Loading
1. Verify `collectstatic` ran successfully
2. Check WhiteNoise configuration in settings

---

## 📊 Post-Deployment Checklist

- [ ] Application is accessible
- [ ] Health check returns: `{"status": "ok", "service": "sirms"}`
- [ ] Can log in with default credentials
- [ ] VRF cases route to ESP Teacher dashboard
- [ ] "For Vrf" sidebar shows VRF cases
- [ ] Counseling Schedule shows non-VRF cases
- [ ] Case evaluation works correctly

---

## 🎉 Success!

Once deployed, your SIRMS application will be live at:
**https://sirms.onrender.com**

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Render Support:** https://render.com/support
- **Check Logs:** Render Dashboard → Your Service → Logs

---

## 🔄 Updating Your Deployment

When you make changes:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Render automatically:**
   - Detects the push
   - Starts new deployment
   - Builds and deploys changes

3. **Monitor deployment** in Render dashboard

---

**Ready to deploy? Go to https://dashboard.render.com and follow Step 3 above!** 🚀

