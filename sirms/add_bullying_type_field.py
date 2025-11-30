"""
Add bullying_type field to IncidentReport model
Run this to add the field without creating a full migration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.db import connection

def add_bullying_type_field():
    """Add bullying_type field to incidents_incidentreport table"""
    with connection.cursor() as cursor:
        try:
            # Check if column already exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='incidents_incidentreport' 
                AND column_name='bullying_type'
            """)
            
            if cursor.fetchone():
                print("ℹ️  bullying_type field already exists")
                return
            
            # Add the column
            cursor.execute("""
                ALTER TABLE incidents_incidentreport 
                ADD COLUMN bullying_type VARCHAR(50) NULL
            """)
            print("✅ Added bullying_type field to IncidentReport model")
            
        except Exception as e:
            # For SQLite
            try:
                cursor.execute("""
                    ALTER TABLE incidents_incidentreport 
                    ADD COLUMN bullying_type VARCHAR(50)
                """)
                print("✅ Added bullying_type field to IncidentReport model (SQLite)")
            except Exception as e2:
                print(f"❌ Error: {e2}")

if __name__ == '__main__':
    print("\n🔧 Adding bullying_type field...")
    add_bullying_type_field()
    print("✅ Done!\n")
