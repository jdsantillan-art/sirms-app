# Database Status Check

## Date: November 30, 2025

## Current Database Configuration

### ✅ You are currently using **SQLite**

**Evidence:**
- Environment variable `USE_POSTGRESQL` is **Not Set**
- SQLite database file `db.sqlite3` exists in your project root
- Settings.py is configured to use SQLite by default when `USE_POSTGRESQL` is not set to 'true'

## Database Configuration Details

### Current Setup (SQLite)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Location:** `sirms/db.sqlite3`

### Available PostgreSQL Setup
Your project has PostgreSQL configuration ready but **not active**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'sirms_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## How to Switch to PostgreSQL

You have two convenient batch files ready:

### Option 1: Using Batch File (Recommended)
```cmd
# Switch to PostgreSQL
switch_to_postgresql.bat

# Switch back to SQLite
switch_to_sqlite.bat
```

### Option 2: Manual Environment Variable
```cmd
# PowerShell
$env:USE_POSTGRESQL = "true"

# CMD
set USE_POSTGRESQL=true
```

## Benefits of Each Database

### SQLite (Current)
✅ **Pros:**
- No installation required
- Simple setup
- Perfect for development
- Single file database
- Fast for small datasets
- Easy to backup (just copy db.sqlite3)

❌ **Cons:**
- Not suitable for production with multiple users
- Limited concurrent write operations
- No advanced features
- File-based (can be slower with large data)

### PostgreSQL
✅ **Pros:**
- Production-ready
- Handles multiple concurrent users
- Advanced features (JSON fields, full-text search)
- Better performance with large datasets
- ACID compliant
- Robust backup and recovery

❌ **Cons:**
- Requires installation and setup
- More complex configuration
- Needs separate server process
- Requires credentials management

## Migration Guide

If you want to switch to PostgreSQL, follow these steps:

### 1. Install PostgreSQL
- Download from: https://www.postgresql.org/download/
- Install with default settings
- Remember your postgres password

### 2. Create Database
```sql
-- Open pgAdmin or psql
CREATE DATABASE sirms_db;
CREATE USER sirms_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sirms_db TO sirms_user;
```

### 3. Set Environment Variables
```cmd
set USE_POSTGRESQL=true
set DB_NAME=sirms_db
set DB_USER=sirms_user
set DB_PASSWORD=your_password
set DB_HOST=localhost
set DB_PORT=5432
```

### 4. Run Migrations
```cmd
python manage.py migrate
```

### 5. Transfer Data (Optional)
```cmd
# Export from SQLite
python manage.py dumpdata > data.json

# Switch to PostgreSQL
set USE_POSTGRESQL=true

# Import to PostgreSQL
python manage.py loaddata data.json
```

## Recommendation

### For Development (Current Stage)
**Stick with SQLite** ✅
- You're currently developing and testing
- SQLite is perfect for this stage
- Easy to manage and backup
- No additional setup needed

### For Production Deployment
**Switch to PostgreSQL** 🚀
- When deploying to Hostinger VPS
- When expecting multiple concurrent users
- When data integrity is critical
- When you need better performance

## Quick Check Commands

### Check Current Database
```cmd
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES['default']['ENGINE'])
```

### Check Database Size
```cmd
# SQLite
dir db.sqlite3

# PostgreSQL
psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('sirms_db'));"
```

## Files Related to Database

### Configuration Files
- `sirms/sirms_project/settings.py` - Database configuration
- `sirms/switch_to_postgresql.bat` - Switch to PostgreSQL
- `sirms/switch_to_sqlite.bat` - Switch to SQLite
- `sirms/check_postgresql.py` - Check PostgreSQL connection

### Database Files
- `sirms/db.sqlite3` - SQLite database (current)
- `sirms/incidents/migrations/` - Database migrations

### Documentation
- `sirms/POSTGRESQL_MIGRATION_GUIDE.md` - Detailed migration guide
- `sirms/DATABASE_DOCUMENTATION.md` - Database schema documentation

## Summary

**Current Status:** ✅ Using SQLite (Development Mode)

**Action Required:** None - SQLite is perfect for your current development stage

**Future Action:** Switch to PostgreSQL when deploying to production

**Data Safety:** Your data is safe in `db.sqlite3` - make regular backups!

---

**Last Checked:** November 30, 2025
**Database:** SQLite (db.sqlite3)
**Status:** Active and Working
**Size:** Check with `dir db.sqlite3`
