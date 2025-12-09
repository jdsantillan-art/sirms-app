from django.core.management.base import BaseCommand
from incidents.models import CustomUser, TeacherAssignment

class Command(BaseCommand):
    help = 'Create Ms. Stephanie Mercado teacher account'

    def handle(self, *args, **options):
        username = 'stephanie.mercado'
        password = 'Teacher2024!'
        
        # Delete existing user if any
        CustomUser.objects.filter(username=username).delete()
        
        # Create new user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email='stephanie.mercado@school.edu',
            first_name='Stephanie',
            last_name='Mercado',
            role='teacher',
            employee_id='TCH-2024-008',
            grade_level='Grade 8',
            section='Section 2',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        
        # Create teacher assignment
        TeacherAssignment.objects.get_or_create(
            teacher_name='Ms. Stephanie Mercado',
            grade_level='8',
            section_name='Section 2',
            track_code='ICT',
            defaults={'curriculum': None}
        )
        
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('ACCOUNT CREATED SUCCESSFULLY'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Name: {user.get_full_name()}')
        self.stdout.write(f'Role: {user.get_role_display()}')
        self.stdout.write(f'Assignment: Grade 8 Section 2 (ICT)')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nYou can now login with these credentials!')
