"""
Setup initial data for SIRMS
Run this script to populate the database with initial data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser, Curriculum, Track, Grade, Section

def create_superuser():
    """Create admin superuser"""
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='principal',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Superuser created: username='admin', password='admin123'")
    else:
        print("ℹ️  Superuser already exists")

def create_curriculums_and_structure():
    """Create curriculum, tracks, grades, and sections"""
    
    # K-12 Curriculum
    k12, _ = Curriculum.objects.get_or_create(
        name='K-12',
        defaults={'description': 'K-12 Basic Education Curriculum'}
    )
    print(f"✅ Curriculum: {k12.name}")
    
    # K-12 Track
    k12_track, _ = Track.objects.get_or_create(
        name='Junior High School',
        curriculum=k12
    )
    print(f"  ✅ Track: {k12_track.name}")
    
    # Grades 7-10
    grades = ['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10']
    for grade_name in grades:
        grade, _ = Grade.objects.get_or_create(
            level=grade_name,
            track=k12_track
        )
        print(f"    ✅ Grade: {grade.level}")
        
        # Sections A-D for each grade
        for section_letter in ['A', 'B', 'C', 'D']:
            section, _ = Section.objects.get_or_create(
                name=f'Section {section_letter}',
                grade=grade
            )
            print(f"      ✅ Section: {section.name}")
    
    # Senior High School Curriculum
    shs, _ = Curriculum.objects.get_or_create(
        name='Senior High School',
        defaults={'description': 'Senior High School Program'}
    )
    print(f"\n✅ Curriculum: {shs.name}")
    
    # SHS Tracks
    tracks = ['STEM', 'ABM', 'HUMSS', 'GAS']
    for track_name in tracks:
        track, _ = Track.objects.get_or_create(
            name=track_name,
            curriculum=shs
        )
        print(f"  ✅ Track: {track.name}")
        
        # Grades 11-12
        for grade_level in ['Grade 11', 'Grade 12']:
            grade, _ = Grade.objects.get_or_create(
                level=grade_level,
                track=track
            )
            print(f"    ✅ Grade: {grade.level}")
            
            # Sections A-B for each grade
            for section_letter in ['A', 'B']:
                section, _ = Section.objects.get_or_create(
                    name=f'{track_name} {section_letter}',
                    grade=grade
                )
                print(f"      ✅ Section: {section.name}")

def create_sample_users():
    """Create sample users for testing"""
    
    # Sample student
    if not CustomUser.objects.filter(username='student1').exists():
        CustomUser.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student123',
            role='student',
            first_name='Juan',
            last_name='Dela Cruz'
        )
        print("✅ Sample student created: username='student1', password='student123'")
    
    # Sample teacher
    if not CustomUser.objects.filter(username='teacher1').exists():
        CustomUser.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='teacher123',
            role='teacher',
            first_name='Maria',
            last_name='Santos'
        )
        print("✅ Sample teacher created: username='teacher1', password='teacher123'")
    
    # Sample counselor
    if not CustomUser.objects.filter(username='counselor1').exists():
        CustomUser.objects.create_user(
            username='counselor1',
            email='counselor1@example.com',
            password='counselor123',
            role='counselor',
            first_name='Pedro',
            last_name='Reyes'
        )
        print("✅ Sample counselor created: username='counselor1', password='counselor123'")
    
    # Sample DO accounts
    if not CustomUser.objects.filter(username='do1').exists():
        CustomUser.objects.create_user(
            username='do1',
            email='do1@example.com',
            password='do123',
            role='do',
            first_name='Ana',
            last_name='Garcia'
        )
        print("✅ Sample DO created: username='do1', password='do123'")
    
    # Additional DO account for easy access
    if not CustomUser.objects.filter(username='do_admin').exists():
        CustomUser.objects.create_user(
            username='do_admin',
            email='do.admin@school.edu',
            password='do123',
            role='do',
            first_name='Discipline',
            last_name='Officer'
        )
        print("✅ DO Admin created: username='do_admin', password='do123'")

def main():
    print("\n🚀 Setting up initial data for SIRMS...\n")
    
    print("=" * 60)
    print("1️⃣  Creating superuser...")
    print("=" * 60)
    create_superuser()
    
    print("\n" + "=" * 60)
    print("2️⃣  Creating curriculum structure...")
    print("=" * 60)
    create_curriculums_and_structure()
    
    print("\n" + "=" * 60)
    print("3️⃣  Creating sample users...")
    print("=" * 60)
    create_sample_users()
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\n📝 Login credentials:")
    print("   Admin:     username='admin'      password='admin123'")
    print("   Student:   username='student1'   password='student123'")
    print("   Teacher:   username='teacher1'   password='teacher123'")
    print("   Counselor: username='counselor1' password='counselor123'")
    print("   DO:        username='do1'        password='do123'")
    print("   DO Admin:  username='do_admin'   password='do123'")
    print("\n🌐 Access your app at: http://127.0.0.1:8000")
    print("🔧 Access admin panel at: http://127.0.0.1:8000/admin")
    print("\n")

if __name__ == '__main__':
    main()
