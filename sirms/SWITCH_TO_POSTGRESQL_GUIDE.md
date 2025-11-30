# Switch to PostgreSQL - Complete Guide

## Prerequisites Check

### 1. Check if PostgreSQL is Installed
Open PowerShell and run:
```powershell
psql --version
```

**If you see a version number:** PostgreSQL is installed ✅
**If you see an error:** You need to install PostgreSQL first ❌

## Installation Steps (If Not Installed)

### Download and Install PostgreSQL
1. Go to: https://www.postgresql.org/download/windows/
2. Download the installer (latest version)
3. Run the installer
4. **Important:** Remember the password you set for the `postgres` user!
5. Keep default port: 5432
6. Install all components (including pgAdmin)

## Step-by-Step Migration Process

### Step 1: Backup Your Current SQLite Data
```cmd
cd sirms
python manage.py dumpdata > backup_data.json
```

This creates a backup of all your data.

### Step 2: Create PostgreSQL Database

#### Option A: Using pgAdmin (GUI)
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to PostgreSQL server (use your postgres password)
3. Right-click "Databases" → Create → Database
4. Name: `sirms_db`
5. Click Save

#### Option B: Using Command Line
```cmd
psql -U postgres
# Enter your postgres password when prompted

# Then run these SQL commands:
CREATE DATABASE sirms_db;
\q
```

### Step 3: Set Environment Variables

#### Option A: Using PowerShell (Temporary - Current Session Only)
```powershell
$env:USE_POSTGRESQL = "true"
$env:DB_NAME = "sirms_db"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_postgres_password"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
```

#### Option B: Using CMD (Temporary - Current Session Only)
```cmd
set USE_POSTGRESQL=true
set DB_NAME=sirms_db
set DB_USER=postgres
set DB_PASSWORD=your_postgres_password
set DB_HOST=localhost
set DB_PORT=5432
```

#### Option C: Create .env File (Recommended - Permanent)
Create a file named `.env` in your `sirms` folder:
```env
USE_POSTGRESQL=true
DB_NAME=sirms_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Then install python-decouple:
```cmd
pip install python-decouple
```

And update your settings.py to use it (I can help with this).

### Step 4: Run Migrations
```cmd
cd sirms
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, incidents, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 5: Load Your Data (Optional)
```cmd
python manage.py loaddata backup_data.json
```

### Step 6: Create Superuser (If Needed)
```cmd
python manage.py createsuperuser
```

### Step 7: Test the Connection
```cmd
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Quick Switch Script

I'll create an automated script for you. Save this as `quick_switch_postgresql.py`:

```python
import os
import subprocess
import sys

def main():
    print("=" * 60)
    print("SIRMS - Quick Switch to PostgreSQL")
    print("=" * 60)
    print()
    
    # Get password
    password = input("Enter your PostgreSQL password: ")
    
    # Set environment variables
    os.environ['USE_POSTGRESQL'] = 'true'
    os.environ['DB_NAME'] = 'sirms_db'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = password
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    
    print("\n✅ Environment variables set!")
    print("\nStep 1: Creating backup...")
    
    # Backup current data
    try:
        subprocess.run(['python', 'manage.py', 'dumpdata'], 
                      stdout=open('backup_data.json', 'w'),
                      check=True)
        print("✅ Backup created: backup_data.json")
    except:
        print("⚠️  Backup failed (might be empty database)")
    
    print("\nStep 2: Running migrations...")
    
    # Run migrations
    try:
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    print("\nStep 3: Loading data...")
    
    # Load data
    if os.path.exists('backup_data.json'):
        try:
            subprocess.run(['python', 'manage.py', 'loaddata', 'backup_data.json'], 
                          check=True)
            print("✅ Data loaded successfully!")
        except:
            print("⚠️  Data loading failed (you may need to recreate users)")
    
    print("\n" + "=" * 60)
    print("✅ Successfully switched to PostgreSQL!")
    print("=" * 60)
    print("\nYou can now run: python manage.py runserver")
    print("\nNote: These environment variables are temporary.")
    print("To make them permanent, create a .env file.")

if __name__ == '__main__':
    main()
```

## Troubleshooting

### Error: "psycopg2 not installed"
```cmd
pip install psycopg2-binary
```

### Error: "FATAL: password authentication failed"
- Check your postgres password
- Make sure DB_PASSWORD environment variable is correct

### Error: "could not connect to server"
- Make sure PostgreSQL service is running
- Check Windows Services → PostgreSQL should be "Running"
- Or restart it: `net start postgresql-x64-XX` (check service name)

### Error: "database does not exist"
- Create the database first using pgAdmin or psql
- Database name should be: `sirms_db`

### Error: "relation does not exist"
- Run migrations: `python manage.py migrate`

## Verification Commands

### Check Current Database
```cmd
python manage.py shell
```
Then:
```python
from django.conf import settings
print(settings.DATABASES['default']['ENGINE'])
# Should show: django.db.backends.postgresql
```

### Check Database Connection
```cmd
python manage.py dbshell
```
This should open PostgreSQL prompt if connected.

### Check Tables
```cmd
python manage.py dbshell
```
Then:
```sql
\dt
```
You should see all your tables listed.

## Switch Back to SQLite

If you need to switch back:
```cmd
set USE_POSTGRESQL=false
# or
$env:USE_POSTGRESQL = "false"
```

Then restart your server.

## Performance Tips

### After Migration
```sql
-- Connect to database
psql -U postgres -d sirms_db

-- Analyze tables for better performance
ANALYZE;

-- Vacuum to reclaim space
VACUUM;
```

## Next Steps

1. ✅ Backup your data
2. ✅ Install PostgreSQL (if needed)
3. ✅ Create database
4. ✅ Set environment variables
5. ✅ Run migrations
6. ✅ Load data
7. ✅ Test application

## Need Help?

If you encounter any issues:
1. Check the error message carefully
2. Verify PostgreSQL is running
3. Check your password
4. Ensure database exists
5. Run migrations again

---

**Ready to switch?** Follow the steps above or run the quick switch script!
