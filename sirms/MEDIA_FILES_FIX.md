# Media Files Not Found - Fix Guide

## Problem

Images and videos uploaded to Render are not accessible because:
- Render uses **ephemeral filesystem** (files are deleted on every deployment)
- Media files stored in `/media/` folder get wiped out
- This causes "Not Found" errors when trying to view evidence

## Solution: Use Cloud Storage

You need to store media files in cloud storage instead of local filesystem.

### Recommended: Cloudinary (Free Tier)

Cloudinary offers:
- Free tier: 25GB storage, 25GB bandwidth/month
- Easy Django integration
- Automatic image optimization
- Video support

## Implementation Steps

### 1. Sign up for Cloudinary

1. Go to: https://cloudinary.com/users/register/free
2. Sign up for free account
3. Get your credentials:
   - Cloud Name
   - API Key
   - API Secret

### 2. Install Cloudinary

Add to `requirements.txt`:
```
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
```

### 3. Update settings.py

Add to `INSTALLED_APPS` (before 'django.contrib.staticfiles'):
```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.staticfiles',
    # ...
]
```

Add Cloudinary configuration:
```python
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

# Use Cloudinary for media files
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### 4. Set Environment Variables in Render

In Render dashboard:
1. Go to your service
2. Click "Environment"
3. Add these variables:
   - `CLOUDINARY_CLOUD_NAME` = your_cloud_name
   - `CLOUDINARY_API_KEY` = your_api_key
   - `CLOUDINARY_API_SECRET` = your_api_secret

### 5. Deploy

```bash
git add requirements.txt sirms_project/settings.py
git commit -m "Add Cloudinary for media storage"
git push origin main
```

## Alternative: AWS S3

If you prefer AWS S3:

1. Install: `pip install django-storages boto3`
2. Configure in settings.py:
```python
INSTALLED_APPS = [
    # ...
    'storages',
]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## Temporary Workaround (Not Recommended)

If you need a quick fix for testing only:

1. Re-upload the evidence files after each deployment
2. Or use external image hosting (Imgur, etc.) and paste URLs

## Why This Happens

Render's filesystem is **ephemeral**:
- Files uploaded during runtime are stored temporarily
- On every deployment/restart, the filesystem resets
- All uploaded files are lost

This is why you need persistent cloud storage for production.

## Next Steps

1. Choose cloud storage provider (Cloudinary recommended)
2. Sign up and get credentials
3. Install required packages
4. Update settings.py
5. Set environment variables in Render
6. Deploy
7. Re-upload evidence files (they'll now persist)

---

**Status**: Requires cloud storage setup
**Recommended**: Cloudinary (free tier sufficient)
**Impact**: All future uploads will persist across deployments
