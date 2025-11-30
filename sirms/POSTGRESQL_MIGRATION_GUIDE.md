# PostgreSQL Migration Guide for SIRMS

## Current Status
✅ **psycopg2-binary** installed  
✅ **Data backup created** (backup_data.json)  
⏳ **PostgreSQL installation needed**

---

## Step 1: Install PostgreSQL

### Option A: Download from Official Website
1. Visit: https://www.postgresql.org/download/windows/
2. Download PostgreSQL installer (version 15 or 16 recommended)
3. Run installer and follow these settings:
   - **Password**: Set a strong password for postgres user (remember this!)
   - **Port**: 5432 (default)
   - **Locale**: Default
4. Install pgAdmin 4 (included in installer) for database management

### Option B: Using Chocolatey (if installed)
```powershell
choco install postgresql
```

---

## Step 2: Create Database

After PostgreSQL is installed, open **pgAdmin 4** or use command line:

### Using pgAdmin 4:
1. Open pgAdmin 4
2. Connect to PostgreSQL server (use password you set)
3. Right-click "Databases" → Create → Database
4. Database name: `sirms_db`
5. Owner: `postgres`
6. Click Save

### Using Command Line:
```cmd
psql -U postgres
CREATE DATABASE sirms_db;
\q
```

---

## Step 3: Update Django Settings

Your settings have been updated to use PostgreSQL. The configuration uses environment variables for security.

### Set Environment Variables (Windows):

**Option A: Set temporarily (for testing):**
```cmd
set DB_NAME=sirms_db
set DB_USER=postgres
set DB_PASSWORD=your_postgres_password
set DB_HOST=localhost
set DB_PORT=5432
```

**Option B: Set permanently (recommended):**
1. Open System Properties → Environment Variables
2. Add these User Variables:
   - `DB_NAME` = `sirms_db`
   - `DB_USER` = `postgres`
   - `DB_PASSWORD` = `your_postgres_password`
   - `DB_HOST` = `localhost`
   - `DB_PORT` = `5432`

**Option C: Create .env file (best for development):**
Create a file named `.env` in the sirms folder:
```
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

---

## Step 4: Run Migrations

```cmd
cd sirms
python manage.py migrate
```

This will create all 23 tables in PostgreSQL.

---

## Step 5: Restore Data

```cmd
python manage.py loaddata backup_data.json
```

---

## Step 6: Create Superuser (if needed)

If you need to create a new admin user:
```cmd
python manage.py createsuperuser
```

---

## Step 7: Test the Application

```cmd
python manage.py runserver
```

Visit http://127.0.0.1:8000 and verify everything works.

---

## Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `sirms_db` created
- [ ] Environment variables set
- [ ] Migrations completed successfully
- [ ] Data restored from backup
- [ ] Application runs without errors
- [ ] Can login and access all features
- [ ] All 23 tables exist in PostgreSQL

---

## Check Tables in PostgreSQL

### Using pgAdmin 4:
Navigate to: Servers → PostgreSQL → Databases → sirms_db → Schemas → public → Tables

### Using Command Line:
```cmd
psql -U postgres -d sirms_db
\dt
```

You should see all 23 tables listed.

---

## Rollback to SQLite (if needed)

If you encounter issues and need to rollback:

1. Stop the server
2. Restore the original settings.py (backup created as settings.py.backup)
3. Your SQLite database (db.sqlite3) is still intact
4. Restart the server

---

## Performance Benefits of PostgreSQL

- **Better concurrency**: Multiple users can access simultaneously
- **Advanced features**: Full-text search, JSON support, complex queries
- **Scalability**: Handles larger datasets efficiently
- **Data integrity**: Better transaction support
- **Production-ready**: Suitable for deployment

---

## Troubleshooting

### Error: "psycopg2.OperationalError: could not connect"
- Check if PostgreSQL service is running
- Verify database credentials
- Check if port 5432 is open

### Error: "FATAL: database does not exist"
- Create the database using pgAdmin or psql

### Error: "FATAL: password authentication failed"
- Verify DB_PASSWORD environment variable
- Check PostgreSQL user password

### Error: "relation does not exist"
- Run migrations: `python manage.py migrate`

---

## Next Steps After Migration

1. **Update deployment documentation** with PostgreSQL setup
2. **Configure automated backups** for PostgreSQL
3. **Set up connection pooling** for better performance
4. **Enable PostgreSQL logging** for monitoring
5. **Consider using pgBouncer** for connection management in production

---

## Database Backup Commands (PostgreSQL)

### Backup:
```cmd
pg_dump -U postgres -d sirms_db -F c -f sirms_backup.dump
```

### Restore:
```cmd
pg_restore -U postgres -d sirms_db sirms_backup.dump
```

---

## Contact & Support

If you encounter any issues during migration, check:
- PostgreSQL logs: `C:\Program Files\PostgreSQL\15\data\log\`
- Django error messages in console
- pgAdmin 4 for database connection issues

---

**Migration prepared on:** November 30, 2025  
**Current database:** SQLite3 → PostgreSQL  
**Data backup:** backup_data.json (✅ Created)
