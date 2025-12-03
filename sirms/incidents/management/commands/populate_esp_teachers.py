"""
Django management command to populate ESP Teachers
Usage: python manage.py populate_esp_teachers
"""
from django.core.management.base import BaseCommand
from incidents.models import Counselor


class Command(BaseCommand):
    help = 'Populate 5 ESP Teachers in the database'

    def handle(self, *args, **options):
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
        
        self.stdout.write(self.style.SUCCESS('Populating ESP Teachers...'))
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
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {teacher.name} - {teacher.email}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {teacher.name} - {teacher.email}')
                )
        
        total_active = Counselor.objects.filter(is_active=True).count()
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Done! Created: {created_count}, Updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total Active ESP Teachers: {total_active}'))
