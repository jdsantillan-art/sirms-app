"""
Signals for automatic repeat offender detection
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import IncidentReport, CaseEvaluation, ViolationHistory


@receiver(post_save, sender=IncidentReport)
def create_violation_history(sender, instance, created, **kwargs):
    """
    Automatically create violation history entry when a report is created
    """
    if created and instance.reported_student and instance.incident_type:
        # Determine severity based on classification if available
        severity = 'minor'
        if hasattr(instance, 'classification') and instance.classification:
            severity = instance.classification.severity
        
        # Create violation history entry
        ViolationHistory.objects.create(
            student=instance.reported_student,
            report=instance,
            violation_type=instance.incident_type,
            severity=severity,
            date_occurred=instance.incident_date,
            status='active',
            notes=f"Auto-created from report {instance.case_id}"
        )


@receiver(pre_save, sender=CaseEvaluation)
def auto_detect_repeat_offender(sender, instance, **kwargs):
    """
    Automatically detect if student is a repeat offender when evaluation is created/updated
    """
    if instance.report and instance.report.reported_student:
        student = instance.report.reported_student
        
        # Count previous violations (excluding current report)
        previous_violations = IncidentReport.objects.filter(
            reported_student=student,
            created_at__lt=instance.report.created_at
        ).count()
        
        # Automatically mark as repeat offender if they have previous violations
        if previous_violations > 0:
            instance.is_repeat_offender = True
            
            # Find related cases (previous reports by same student)
            related_reports = IncidentReport.objects.filter(
                reported_student=student,
                created_at__lt=instance.report.created_at
            ).order_by('-created_at')[:5]  # Get last 5 previous reports
            
            # Save the evaluation first if it's new
            if not instance.pk:
                # We'll add related cases after save
                pass
        else:
            instance.is_repeat_offender = False


@receiver(post_save, sender=CaseEvaluation)
def link_related_cases(sender, instance, created, **kwargs):
    """
    Link related cases after evaluation is saved
    """
    if instance.is_repeat_offender and instance.report and instance.report.reported_student:
        student = instance.report.reported_student
        
        # Find related cases (previous reports by same student)
        related_reports = IncidentReport.objects.filter(
            reported_student=student,
            created_at__lt=instance.report.created_at
        ).order_by('-created_at')[:5]  # Get last 5 previous reports
        
        # Add related cases
        instance.related_cases.set(related_reports)


@receiver(post_save, sender=IncidentReport)
def update_existing_evaluations(sender, instance, created, **kwargs):
    """
    When a new report is created, check if this student has other evaluations
    that should be marked as repeat offender
    """
    if created and instance.reported_student:
        student = instance.reported_student
        
        # Find all evaluations for this student
        evaluations = CaseEvaluation.objects.filter(
            report__reported_student=student
        )
        
        # Update each evaluation's repeat offender status
        for evaluation in evaluations:
            # Count violations before this evaluation's report
            previous_violations = IncidentReport.objects.filter(
                reported_student=student,
                created_at__lt=evaluation.report.created_at
            ).count()
            
            if previous_violations > 0 and not evaluation.is_repeat_offender:
                evaluation.is_repeat_offender = True
                evaluation.save(update_fields=['is_repeat_offender'])
                
                # Update related cases
                related_reports = IncidentReport.objects.filter(
                    reported_student=student,
                    created_at__lt=evaluation.report.created_at
                ).order_by('-created_at')[:5]
                evaluation.related_cases.set(related_reports)
