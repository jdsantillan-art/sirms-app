"""
PostgreSQL Setup Checker for SIRMS
Run this script to verify PostgreSQL connection before migration
"""

import os
import sys

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    try:
        import psycopg2
        print("✅ psycopg2 is installed")
        return True
    except ImportError:
        print("❌ psycopg2 is NOT installed")
        print("   Run: pip install psycopg2-binary")
        return False

def check_postgresql_connection():
    """Try to connect to PostgreSQL"""
    try:
        import psycopg2
        
        # Get credentials from environment or use defaults
        db_name = os.environ.get('DB_NAME', 'sirms_db')
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', '')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        
        if not db_password:
            print("⚠️  DB_PASSWORD environment variable not set")
            db_password = input("Enter PostgreSQL password: ")
        
        print(f"\n🔍 Attempting to connect to PostgreSQL...")
        print(f"   Host: {db_host}:{db_port}")
        print(f"   Database: {db_name}")
        print(f"   User: {db_user}")
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"\n✅ Successfully connected to PostgreSQL!")
        print(f"   Version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to connect to PostgreSQL")
        print(f"   Error: {str(e)}")
        print("\n📋 Troubleshooting:")
        print("   1. Is PostgreSQL installed and running?")
        print("   2. Does the database 'sirms_db' exist?")
        print("   3. Are the credentials correct?")
        print("   4. Is PostgreSQL service running?")
        return False

def check_environment_variables():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    vars_to_check = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'USE_POSTGRESQL']
    
    for var in vars_to_check:
        value = os.environ.get(var)
        if value:
            if var == 'DB_PASSWORD':
                print(f"   ✅ {var} = {'*' * len(value)}")
            else:
                print(f"   ✅ {var} = {value}")
        else:
            print(f"   ⚠️  {var} = (not set)")

def main():
    print("=" * 60)
    print("SIRMS - PostgreSQL Setup Checker")
    print("=" * 60)
    
    # Check 1: psycopg2 installed
    print("\n1️⃣  Checking psycopg2 installation...")
    if not check_postgresql_installed():
        sys.exit(1)
    
    # Check 2: Environment variables
    check_environment_variables()
    
    # Check 3: PostgreSQL connection
    print("\n2️⃣  Checking PostgreSQL connection...")
    if check_postgresql_connection():
        print("\n" + "=" * 60)
        print("✅ All checks passed! You're ready to migrate.")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Set USE_POSTGRESQL=true")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py loaddata backup_data.json")
        print("4. Run: python manage.py runserver")
    else:
        print("\n" + "=" * 60)
        print("❌ PostgreSQL connection failed")
        print("=" * 60)
        print("\nPlease install PostgreSQL first:")
        print("https://www.postgresql.org/download/windows/")
        print("\nThen create the database:")
        print("psql -U postgres")
        print("CREATE DATABASE sirms_db;")

if __name__ == "__main__":
    main()
