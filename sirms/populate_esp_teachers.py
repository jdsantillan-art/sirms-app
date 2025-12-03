"""
Script to populate 5 ESP Teachers in the database
Run this after migrations: python populate_esp_teachers.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import Counselor

def populate_esp_teachers():
    """Create 5 ESP teachers with sample data"""
    
    esp_teachers_data = [
        {
            'name': 'Maria Santos',
            'email': 'lastname1espteacher@gmail.com',
            'phone': '09XX XXX XXXX',
            'specialization': 'Values Education',
        },
        {
            'name': 'Juan Dela Cruz',
            'email': 'lastname2espteacher@gmail.com',
            'phone': '09XX XXX XXXX',
            'specialization': 'Behavioral Counseling',
        },
        {
            'name': 'Ana Reyes',
            'email': 'lastname3espteacher@gmail.com',
            'phone': '09XX XXX XXXX',
            'specialization': 'Character Formation',
        },
        {
            'name': 'Pedro Garcia',
            'email': 'lastname4espteacher@gmail.com',
            'phone': '09XX XXX XXXX',
            'specialization': 'Moral Development',
        },
        {
            'name': 'Rosa Martinez',
            'email': 'lastname5espteacher@gmail.com',
            'phone': '09XX XXX XXXX',
            'specialization': 'Student Guidance',
        },
    ]
    
    print("Populating ESP Teachers...")
    created_count = 0
    updated_count = 0
    
    for teacher_data in esp_teachers_data:
        teacher, created = Counselor.objects.update_or_create(
            email=teacher_data['email'],
            defaults={
                'name': teacher_data['name'],
                'phone': teacher_data['phone'],
                'specialization': teacher_data['specialization'],
                'is_active': True,
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {teacher.name} - {teacher.email}")
        else:
            updated_count += 1
            print(f"↻ Updated: {teacher.name} - {teacher.email}")
    
    print(f"\n✅ Done! Created: {created_count}, Updated: {updated_count}")
    print(f"Total ESP Teachers: {Counselor.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    populate_esp_teachers()
