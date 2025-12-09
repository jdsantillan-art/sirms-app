"""
Management command to detect and mark repeat offenders in existing data
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from incidents.models import IncidentReport, CaseEvaluation, ViolationHistory, CustomUser


class Command(BaseCommand):
    help = 'Automatically detect and mark repeat offenders in existing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        self.stdout.write('Starting repeat offender detection...\n')
        
        # Step 1: Create missing violation history entries
        self.stdout.write('Step 1: Creating violation history entries...')
        reports_without_history = IncidentReport.objects.filter(
            reported_student__isnull=False,
            incident_type__isnull=False
        ).exclude(
            id__in=ViolationHistory.objects.values_list('report_id', flat=True)
        )
        
        history_created = 0
        for report in reports_without_history:
            if not dry_run:
                severity = 'minor'
                if hasattr(report, 'classification') and report.classification:
                    severity = report.classification.severity
                
                ViolationHistory.objects.create(
                    student=report.reported_student,
                    report=report,
                    violation_type=report.incident_type,
                    severity=severity,
                    date_occurred=report.incident_date,
                    status='active',
                    notes=f"Auto-created from report {report.case_id}"
                )
            history_created += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Created {history_created} violation history entries'
        ))
        
        # Step 2: Update evaluations with repeat offender status
        self.stdout.write('\nStep 2: Updating case evaluations...')
        evaluations = CaseEvaluation.objects.select_related('report', 'report__reported_student').all()
        
        evaluations_updated = 0
        repeat_offenders_found = 0
        
        for evaluation in evaluations:
            if evaluation.report and evaluation.report.reported_student:
                student = evaluation.report.reported_student
                
                # Count previous violations
                previous_violations = IncidentReport.objects.filter(
                    reported_student=student,
                    created_at__lt=evaluation.report.created_at
                ).count()
                
                is_repeat = previous_violations > 0
                
                # Update if status changed
                if evaluation.is_repeat_offender != is_repeat:
                    if not dry_run:
                        evaluation.is_repeat_offender = is_repeat
                        evaluation.save(update_fields=['is_repeat_offender'])
                        
                        # Link related cases
                        if is_repeat:
                            related_reports = IncidentReport.objects.filter(
                                reported_student=student,
                                created_at__lt=evaluation.report.created_at
                            ).order_by('-created_at')[:5]
                            evaluation.related_cases.set(related_reports)
                    
                    evaluations_updated += 1
                    if is_repeat:
                        repeat_offenders_found += 1
                        self.stdout.write(
                            f'  • {student.get_full_name()} - {previous_violations} previous violations'
                        )
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Updated {evaluations_updated} evaluations'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Found {repeat_offenders_found} repeat offenders'
        ))
        
        # Step 3: Generate statistics
        self.stdout.write('\nStep 3: Generating statistics...')
        
        # Students with multiple violations
        students_with_violations = IncidentReport.objects.filter(
            reported_student__isnull=False
        ).values('reported_student').annotate(
            violation_count=Count('id')
        ).filter(violation_count__gt=1).order_by('-violation_count')
        
        self.stdout.write(f'\n📊 Repeat Offender Statistics:')
        self.stdout.write(f'  • Total students with violations: {students_with_violations.count()}')
        
        if students_with_violations.exists():
            self.stdout.write(f'\n  Top Repeat Offenders:')
            for i, student_data in enumerate(students_with_violations[:10], 1):
                try:
                    student = CustomUser.objects.get(id=student_data['reported_student'])
                    count = student_data['violation_count']
                    self.stdout.write(
                        f'    {i}. {student.get_full_name()} - {count} violations'
                    )
                except CustomUser.DoesNotExist:
                    pass
        
        # Violation type breakdown
        self.stdout.write(f'\n  Violation Type Breakdown:')
        violation_types = ViolationHistory.objects.values(
            'violation_type__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        for vtype in violation_types:
            self.stdout.write(
                f'    • {vtype["violation_type__name"]}: {vtype["count"]} cases'
            )
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  DRY RUN COMPLETE - No changes were made'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                '\n✅ Repeat offender detection complete!'
            ))
