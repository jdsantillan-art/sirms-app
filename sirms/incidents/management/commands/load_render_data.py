"""
Management command to load data for Render
Can be run separately after deployment
"""
from django.core.management.base import BaseCommand
from incidents.models import CustomUser, Curriculum, IncidentType, TeacherAssignment

class Command(BaseCommand):
    help = 'Load initial data for Render deployment'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("🚀 LOADING RENDER DATA")
        self.stdout.write("="*80)
        
        # Check if data already exists
        existing_violations = IncidentType.objects.count()
        existing_teachers = TeacherAssignment.objects.count()
        
        if existing_violations >= 40 and existing_teachers >= 30:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Data already loaded ({existing_violations} violations, {existing_teachers} teachers)"
            ))
            return
        
        # Import and run setup scripts
        try:
            from setup_initial_data import main as setup_initial
            from load_violations import main as load_violations
            from load_teacher_assignments import create_teacher_assignments
            
            self.stdout.write("\n📦 Loading initial data...")
            setup_initial()
            
            self.stdout.write("\n📦 Loading violations...")
            load_violations()
            
            self.stdout.write("\n📦 Loading teacher assignments...")
            create_teacher_assignments()
            
            # Create Ms. Mercado's account
            self.stdout.write("\n👩‍🏫 Creating Ms. Stephanie Mercado's account...")
            try:
                # Delete if exists
                CustomUser.objects.filter(username='stephanie.mercado').delete()
                
                # Create user
                user = CustomUser.objects.create_user(
                    username='stephanie.mercado',
                    password='Teacher2024!',
                    email='stephanie.mercado@school.edu',
                    first_name='Stephanie',
                    last_name='Mercado',
                    role='teacher',
                    employee_id='TCH-2024-008',
                    grade_level='Grade 8',
                    section='Section 2',
                    is_active=True
                )
                
                # Create teacher assignment
                TeacherAssignment.objects.get_or_create(
                    teacher_name='Ms. Stephanie Mercado',
                    grade_level='8',
                    section_name='Section 2',
                    track_code='ICT',
                    defaults={'curriculum': None}
                )
                
                self.stdout.write(self.style.SUCCESS(
                    f"✅ Ms. Mercado's account created!"
                ))
                self.stdout.write(f"   Username: stephanie.mercado")
                self.stdout.write(f"   Password: Teacher2024!")
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️  Could not create Ms. Mercado's account: {e}"))
            
            self.stdout.write(self.style.SUCCESS("\n✅ All data loaded successfully!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error: {e}"))
            raise
