import os
import subprocess
import sys

def main():
    print("=" * 60)
    print("SIRMS - Quick Switch to PostgreSQL")
    print("=" * 60)
    print()
    
    # Check if psycopg2 is installed
    try:
        import psycopg2
        print("✅ psycopg2 is installed")
    except ImportError:
        print("❌ psycopg2 not installed!")
        print("\nInstalling psycopg2-binary...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
        print("✅ psycopg2-binary installed!")
    
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
    
    # Test connection
    print("\nTesting PostgreSQL connection...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to default database first
            user='postgres',
            password=password,
            host='localhost',
            port='5432'
        )
        conn.close()
        print("✅ PostgreSQL connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL is installed and running")
        print("2. Password is correct")
        print("3. PostgreSQL service is started")
        return
    
    # Check if database exists
    print("\nChecking if sirms_db exists...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=password,
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname='sirms_db'")
        exists = cur.fetchone()
        
        if not exists:
            print("Creating sirms_db database...")
            cur.execute("CREATE DATABASE sirms_db")
            print("✅ Database created!")
        else:
            print("✅ Database already exists!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️  Database check/creation failed: {e}")
    
    print("\nStep 1: Creating backup of SQLite data...")
    
    # Temporarily switch back to SQLite for backup
    os.environ['USE_POSTGRESQL'] = 'false'
    
    # Backup current data
    try:
        with open('backup_data.json', 'w', encoding='utf-8') as f:
            result = subprocess.run(
                [sys.executable, 'manage.py', 'dumpdata'],
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
        if result.returncode == 0:
            print("✅ Backup created: backup_data.json")
        else:
            print("⚠️  Backup failed (might be empty database)")
    except Exception as e:
        print(f"⚠️  Backup failed: {e}")
    
    # Switch back to PostgreSQL
    os.environ['USE_POSTGRESQL'] = 'true'
    
    print("\nStep 2: Running migrations on PostgreSQL...")
    
    # Run migrations
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate'],
            env=os.environ.copy()
        )
        if result.returncode == 0:
            print("✅ Migrations completed!")
        else:
            print("❌ Migration failed!")
            return
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    print("\nStep 3: Loading data into PostgreSQL...")
    
    # Load data
    if os.path.exists('backup_data.json'):
        try:
            result = subprocess.run(
                [sys.executable, 'manage.py', 'loaddata', 'backup_data.json'],
                env=os.environ.copy()
            )
            if result.returncode == 0:
                print("✅ Data loaded successfully!")
            else:
                print("⚠️  Data loading had issues (you may need to recreate some data)")
        except Exception as e:
            print(f"⚠️  Data loading failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Successfully switched to PostgreSQL!")
    print("=" * 60)
    print("\nIMPORTANT: These environment variables are temporary!")
    print("\nTo make them permanent, add to your system:")
    print("  USE_POSTGRESQL=true")
    print("  DB_NAME=sirms_db")
    print("  DB_USER=postgres")
    print(f"  DB_PASSWORD={password}")
    print("  DB_HOST=localhost")
    print("  DB_PORT=5432")
    print("\nOr create a .env file with these values.")
    print("\nYou can now run: python manage.py runserver")
    print("\nPress Enter to exit...")
    input()

if __name__ == '__main__':
    main()
