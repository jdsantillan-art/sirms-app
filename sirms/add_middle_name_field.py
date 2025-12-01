"""
Migration script to add middle_name field to CustomUser
Run: python add_middle_name_field.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.db import connection

def add_middle_name_field():
    """Add middle_name field to CustomUser table"""
    print("\n" + "="*60)
    print("🔧 ADDING MIDDLE NAME FIELD TO CUSTOMUSER")
    print("="*60)
    
    try:
        with connection.cursor() as cursor:
            # Check if column already exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='incidents_customuser' 
                AND column_name='middle_name';
            """)
            
            if cursor.fetchone():
                print("\n✅ middle_name field already exists")
                return
            
            # Add middle_name column
            cursor.execute("""
                ALTER TABLE incidents_customuser 
                ADD COLUMN middle_name VARCHAR(150) NULL;
            """)
            
            print("\n✅ Successfully added middle_name field to CustomUser")
            print("   - Field: middle_name")
            print("   - Type: VARCHAR(150)")
            print("   - Nullable: Yes (optional)")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: If using SQLite, this script won't work.")
        print("Please create a Django migration instead:")
        print("  python manage.py makemigrations")
        print("  python manage.py migrate")

if __name__ == '__main__':
    add_middle_name_field()
