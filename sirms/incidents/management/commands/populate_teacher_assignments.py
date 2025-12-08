"""
Django management command to populate teacher assignments
Run: python manage.py populate_teacher_assignments
"""
from django.core.management.base import BaseCommand
from incidents.models import TeacherAssignment, Curriculum


class Command(BaseCommand):
    help = 'Populates teacher assignments for all grades (JHS 7-10, SHS 11-12)'

    def handle(self, *args, **kwargs):
        # Get or create curricula
        jhs_curriculum, _ = Curriculum.objects.get_or_create(
            name='Junior High School',
            defaults={'description': 'Junior High School Curriculum (Grades 7-10)'}
        )
        shs_curriculum, _ = Curriculum.objects.get_or_create(
            name='Senior High School',
            defaults={'description': 'Senior High School Curriculum (Grades 11-12)'}
        )

        assignments_created = 0
        assignments_existing = 0

        # Grade 7 Assignments
        grade_7_assignments = [
            ('Mr. Juan Dela Cruz', 'Section 1', 'STE'),
            ('Ms. Maria Santos', 'Section 2', 'STE'),
            ('Mr. Jose Ramirez', 'Section 1', 'SPA'),
            ('Ms. Angelica Reyes', 'Section 2', 'SPA'),
            ('Mr. Mark Bautista', 'Section 1', 'ICT'),
            ('Ms. Teresa Gonzales', 'Section 2', 'ICT'),
            ('Mrs. Cristina Villanueva', 'Section 1', 'RBEC'),
            ('Mr. Daniel Fernandez', 'Section 2', 'RBEC'),
            ('Ms. Patricia Lopez', 'Section 3', 'RBEC'),
            ('Mr. Carlo Mendoza', 'Section 1', 'STVEP'),
            ('Ms. Andrea Gutierrez', 'Section 2', 'STVEP'),
            ('Mr. Roberto Flores', 'Section 3', 'STVEP'),
            ('Ms. Victoria Ramos', 'Section 4', 'STVEP'),
            ('Mr. Luis Navarro', 'Section 5', 'STVEP'),
            ('Ms. Michelle Castillo', 'Section 6', 'STVEP'),
            ('Mr. Richard Aquino', 'Section 7', 'STVEP'),
            ('Ms. Clarissa Dominguez', 'Section 8', 'STVEP'),
            ('Mr. Samuel Torres', 'Section 9', 'STVEP'),
            ('Ms. Katrina Ramos', 'Section 10', 'STVEP'),
        ]

        # Grade 8 Assignments
        grade_8_assignments = [
            ('Mr. Emmanuel Santos', 'Section 1', 'STE'),
            ('Ms. Karen Morales', 'Section 2', 'STE'),
            ('Mr. Gabriel De Guzman', 'Section 1', 'SPA'),
            ('Ms. Rosalie Pineda', 'Section 2', 'SPA'),
            ('Mr. Victor Alvarado', 'Section 1', 'ICT'),
            ('Ms. Stephanie Mercado', 'Section 2', 'ICT'),
            ('Mr. Adrian Hernandez', 'Section 1', 'RBEC'),
            ('Ms. Bianca Salvador', 'Section 2', 'RBEC'),
            ('Mr. Christian Ortega', 'Section 3', 'RBEC'),
            ('Ms. Camille Estrada', 'Section 1', 'STVEP'),
            ('Mr. Patrick Villanueva', 'Section 2', 'STVEP'),
            ('Ms. Aileen Mendoza', 'Section 3', 'STVEP'),
            ('Mr. Raymond Javier', 'Section 4', 'STVEP'),
            ('Ms. Lourdes Castillo', 'Section 5', 'STVEP'),
            ('Mr. Francis Torres', 'Section 6', 'STVEP'),
            ('Ms. Katrina Ramos', 'Section 7', 'STVEP'),
            ('Mr. Edwin Marquez', 'Section 8', 'STVEP'),
            ('Ms. Jessica Bautista', 'Section 9', 'STVEP'),
            ('Mr. Jerome Cruz', 'Section 10', 'STVEP'),
        ]

        # Grade 9 Assignments
        grade_9_assignments = [
            ('Mr. Ernesto Reyes', 'Section 1', 'STE'),
            ('Ms. Felicia Navarro', 'Section 2', 'STE'),
            ('Mr. Carlo Dominguez', 'Section 1', 'SPA'),
            ('Ms. Maricel Gutierrez', 'Section 2', 'SPA'),
            ('Mr. Arnold Castillo', 'Section 1', 'ICT'),
            ('Ms. Janelle Cruz', 'Section 2', 'ICT'),
            ('Mr. Nicolas Santos', 'Section 1', 'RBEC'),
            ('Ms. Rowena Aquino', 'Section 2', 'RBEC'),
            ('Mr. Paulo Hernandez', 'Section 3', 'RBEC'),
            ('Ms. Lorna Mendoza', 'Section 1', 'STVEP'),
            ('Mr. Benjamin Torres', 'Section 2', 'STVEP'),
            ('Ms. Clara Lopez', 'Section 3', 'STVEP'),
            ('Mr. Eric Bautista', 'Section 4', 'STVEP'),
            ('Ms. Danica Ramirez', 'Section 5', 'STVEP'),
            ('Mr. Julio Fernandez', 'Section 6', 'STVEP'),
            ('Ms. Ivy Manalo', 'Section 7', 'STVEP'),
            ('Mr. Joel Villanueva', 'Section 8', 'STVEP'),
            ('Ms. Arlene Ramos', 'Section 9', 'STVEP'),
            ('Mr. Lester Gonzales', 'Section 10', 'STVEP'),
        ]

        # Grade 10 Assignments
        grade_10_assignments = [
            ('Mr. Harold Garcia', 'Section 1', 'STE'),
            ('Ms. Thea Santos', 'Section 2', 'STE'),
            ('Mr. Alvin Dela Rosa', 'Section 1', 'SPA'),
            ('Ms. Diana Navarro', 'Section 4', 'SPA'),
            ('Mr. Orlando Cruz', 'Section 1', 'ICT'),
            ('Ms. Melissa Javier', 'Section 6', 'ICT'),
            ('Mr. Gregorio Ramos', 'Section 1', 'RBEC'),
            ('Ms. Monica Flores', 'Section 8', 'RBEC'),
            ('Mr. Anthony Villanueva', 'Section 9', 'RBEC'),
            ('Ms. Rhodora Castillo', 'Section 1', 'STVEP'),
            ('Mr. Marvin Torres', 'Section 2', 'STVEP'),
            ('Ms. Sheila Gutierrez', 'Section 3', 'STVEP'),
            ('Mr. Fernando Cruz', 'Section 4', 'STVEP'),
            ('Ms. Beverly Ramirez', 'Section 5', 'STVEP'),
            ('Mr. Jonathan Santos', 'Section 6', 'STVEP'),
            ('Ms. Kristine Lopez', 'Section 7', 'STVEP'),
            ('Mr. Allan Dominguez', 'Section 8', 'STVEP'),
            ('Ms. Noriel Bautista', 'Section 9', 'STVEP'),
            ('Mr. Gilbert Mendoza', 'Section 10', 'STVEP'),
        ]

        # Grade 11 Assignments (Senior High)
        grade_11_assignments = [
            ('Dr. Jennifer Garcia', 'Section 1', 'STEM'),
            ('Ms. Liza Manalo', 'Section 1', 'Arts & Design'),
            ('Mr. Carlo Mendoza', 'Section 1', 'TVL – ICT'),
            ('Mr. Roberto Flores', 'Section 1', 'TVL – SMAW'),
            ('Mr. Daniel Santiago', 'Section 1', 'TVL – EIM'),
            ('Ms. Andrea Gutierrez', 'Section 1', 'TVL – Dressmaking'),
            ('Ms. Teresa Ramos', 'Section 1', 'TVL – FBS'),
            ('Mr. Francis Javier', 'Section 1', 'TVL – Bread & Pastry'),
            ('Ms. Katrina Lopez', 'Section 1', 'TVL – CSS'),
        ]

        # Grade 12 Assignments (Senior High)
        grade_12_assignments = [
            ('Mr. Emmanuel Torres', 'Section 1', 'STEM'),
            ('Ms. Angelica Cruz', 'Section 1', 'Arts & Design'),
            ('Mr. Mark Bautista', 'Section 1', 'TVL – ICT'),
            ('Mr. Raymond Navarro', 'Section 1', 'TVL – SMAW'),
            ('Ms. Bianca Salvador', 'Section 1', 'TVL – EIM'),
            ('Ms. Clarissa Dominguez', 'Section 1', 'TVL – Dressmaking'),
            ('Ms. Jessica Ramirez', 'Section 1', 'TVL – FBS'),
            ('Mr. Adrian Hernandez', 'Section 1', 'TVL – Bread & Pastry'),
            ('Ms. Patricia Villanueva', 'Section 1', 'TVL – CSS'),
        ]

        # Process Junior High School assignments
        jhs_assignments = {
            '7': grade_7_assignments,
            '8': grade_8_assignments,
            '9': grade_9_assignments,
            '10': grade_10_assignments,
        }

        for grade, assignments in jhs_assignments.items():
            for teacher_name, section_name, track_code in assignments:
                assignment, created = TeacherAssignment.objects.get_or_create(
                    teacher_name=teacher_name,
                    curriculum=jhs_curriculum,
                    track_code=track_code,
                    grade_level=grade,
                    section_name=section_name,
                    defaults={}
                )
                if created:
                    assignments_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Created: {teacher_name} - JHS Grade {grade} {section_name} ({track_code})'
                        )
                    )
                else:
                    assignments_existing += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Exists: {teacher_name} - JHS Grade {grade} {section_name} ({track_code})'
                        )
                    )

        # Process Senior High School assignments
        shs_assignments = {
            '11': grade_11_assignments,
            '12': grade_12_assignments,
        }

        for grade, assignments in shs_assignments.items():
            for teacher_name, section_name, track_code in assignments:
                assignment, created = TeacherAssignment.objects.get_or_create(
                    teacher_name=teacher_name,
                    curriculum=shs_curriculum,
                    track_code=track_code,
                    grade_level=grade,
                    section_name=section_name,
                    defaults={}
                )
                if created:
                    assignments_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Created: {teacher_name} - SHS Grade {grade} {section_name} ({track_code})'
                        )
                    )
                else:
                    assignments_existing += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Exists: {teacher_name} - SHS Grade {grade} {section_name} ({track_code})'
                        )
                    )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('SUMMARY:'))
        self.stdout.write(self.style.SUCCESS(f'✅ Created: {assignments_created} assignments'))
        self.stdout.write(self.style.WARNING(f'⚠️  Already existed: {assignments_existing} assignments'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total: {assignments_created + assignments_existing} assignments'))
        self.stdout.write(self.style.SUCCESS('='*60))

