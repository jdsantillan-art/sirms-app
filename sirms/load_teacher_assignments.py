"""
Load sample teacher assignments for auto-fill functionality
Run this to populate teacher assignments
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import TeacherAssignment

def create_teacher_assignments():
    """Create sample teacher assignments"""
    
    print("\n" + "="*60)
    print("👨‍🏫 LOADING TEACHER ASSIGNMENTS")
    print("="*60)
    
    # Sample teacher assignments for K-12 (Grades 7-10)
    k12_assignments = [
        # Grade 7
        {'grade_level': '7', 'section_name': 'Section A', 'teacher_name': 'Ms. Maria Santos'},
        {'grade_level': '7', 'section_name': 'Section B', 'teacher_name': 'Mr. Juan Dela Cruz'},
        {'grade_level': '7', 'section_name': 'Section C', 'teacher_name': 'Ms. Ana Garcia'},
        {'grade_level': '7', 'section_name': 'Section D', 'teacher_name': 'Mr. Pedro Reyes'},
        
        # Grade 8
        {'grade_level': '8', 'section_name': 'Section A', 'teacher_name': 'Ms. Rosa Martinez'},
        {'grade_level': '8', 'section_name': 'Section B', 'teacher_name': 'Mr. Carlos Lopez'},
        {'grade_level': '8', 'section_name': 'Section C', 'teacher_name': 'Ms. Linda Torres'},
        {'grade_level': '8', 'section_name': 'Section D', 'teacher_name': 'Mr. Miguel Ramos'},
        
        # Grade 9
        {'grade_level': '9', 'section_name': 'Section A', 'teacher_name': 'Ms. Sofia Fernandez'},
        {'grade_level': '9', 'section_name': 'Section B', 'teacher_name': 'Mr. Diego Morales'},
        {'grade_level': '9', 'section_name': 'Section C', 'teacher_name': 'Ms. Carmen Diaz'},
        {'grade_level': '9', 'section_name': 'Section D', 'teacher_name': 'Mr. Rafael Cruz'},
        
        # Grade 10
        {'grade_level': '10', 'section_name': 'Section A', 'teacher_name': 'Ms. Isabel Gomez'},
        {'grade_level': '10', 'section_name': 'Section B', 'teacher_name': 'Mr. Antonio Silva'},
        {'grade_level': '10', 'section_name': 'Section C', 'teacher_name': 'Ms. Patricia Mendoza'},
        {'grade_level': '10', 'section_name': 'Section D', 'teacher_name': 'Mr. Roberto Castillo'},
    ]
    
    # Sample teacher assignments for Senior High School (Grades 11-12)
    shs_assignments = [
        # Grade 11 STEM
        {'grade_level': '11', 'section_name': 'STEM A', 'teacher_name': 'Ms. Dr. Elena Rodriguez'},
        {'grade_level': '11', 'section_name': 'STEM B', 'teacher_name': 'Mr. Dr. Jose Hernandez'},
        
        # Grade 12 STEM
        {'grade_level': '12', 'section_name': 'STEM A', 'teacher_name': 'Ms. Dr. Gloria Sanchez'},
        {'grade_level': '12', 'section_name': 'STEM B', 'teacher_name': 'Mr. Dr. Luis Ramirez'},
        
        # Grade 11 ABM
        {'grade_level': '11', 'section_name': 'ABM A', 'teacher_name': 'Ms. Angela Flores'},
        {'grade_level': '11', 'section_name': 'ABM B', 'teacher_name': 'Mr. Ricardo Vargas'},
        
        # Grade 12 ABM
        {'grade_level': '12', 'section_name': 'ABM A', 'teacher_name': 'Ms. Teresa Ortiz'},
        {'grade_level': '12', 'section_name': 'ABM B', 'teacher_name': 'Mr. Fernando Castro'},
        
        # Grade 11 HUMSS
        {'grade_level': '11', 'section_name': 'HUMSS A', 'teacher_name': 'Ms. Beatriz Navarro'},
        {'grade_level': '11', 'section_name': 'HUMSS B', 'teacher_name': 'Mr. Alejandro Ruiz'},
        
        # Grade 12 HUMSS
        {'grade_level': '12', 'section_name': 'HUMSS A', 'teacher_name': 'Ms. Cristina Jimenez'},
        {'grade_level': '12', 'section_name': 'HUMSS B', 'teacher_name': 'Mr. Eduardo Moreno'},
        
        # Grade 11 GAS
        {'grade_level': '11', 'section_name': 'GAS A', 'teacher_name': 'Ms. Margarita Romero'},
        {'grade_level': '11', 'section_name': 'GAS B', 'teacher_name': 'Mr. Francisco Gutierrez'},
        
        # Grade 12 GAS
        {'grade_level': '12', 'section_name': 'GAS A', 'teacher_name': 'Ms. Victoria Alvarez'},
        {'grade_level': '12', 'section_name': 'GAS B', 'teacher_name': 'Mr. Sergio Mendez'},
    ]
    
    all_assignments = k12_assignments + shs_assignments
    
    created_count = 0
    updated_count = 0
    
    for assignment_data in all_assignments:
        assignment, created = TeacherAssignment.objects.update_or_create(
            grade_level=assignment_data['grade_level'],
            section_name=assignment_data['section_name'],
            defaults={'teacher_name': assignment_data['teacher_name']}
        )
        
        if created:
            created_count += 1
            print(f"✅ Created: Grade {assignment.grade_level} - {assignment.section_name} → {assignment.teacher_name}")
        else:
            updated_count += 1
            print(f"♻️  Updated: Grade {assignment.grade_level} - {assignment.section_name} → {assignment.teacher_name}")
    
    print("\n" + "="*60)
    print("✅ TEACHER ASSIGNMENTS LOADED!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count}")
    print(f"   Updated: {updated_count}")
    print(f"   Total: {TeacherAssignment.objects.count()}")
    print(f"\n💡 Teacher names will now auto-fill when selecting:")
    print(f"   Curriculum → Grade → Section")
    print()

if __name__ == '__main__':
    create_teacher_assignments()
