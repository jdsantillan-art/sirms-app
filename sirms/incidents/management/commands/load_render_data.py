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
            
            self.stdout.write(self.style.SUCCESS("\n✅ All data loaded successfully!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error: {e}"))
            raise
