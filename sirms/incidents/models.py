from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('do', 'Discipline Officer'),
        ('counselor', 'Guidance Counselor'),
        ('esp_teacher', 'ESP Teacher/VPF Coordinator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    middle_name = models.CharField(max_length=150, blank=True, null=True, help_text="Optional middle name")
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    grade_level = models.CharField(max_length=10, null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    
    def get_full_name_with_middle(self):
        """Return full name including middle name if available"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return self.get_full_name()
    
    def save(self, *args, **kwargs):
        """Auto-capitalize names before saving"""
        if self.first_name:
            self.first_name = self.first_name.title()
        if self.middle_name:
            self.middle_name = self.middle_name.title()
        if self.last_name:
            self.last_name = self.last_name.title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name_with_middle()} ({self.get_role_display()})"


class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=100)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    level = models.CharField(max_length=10)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Grade {self.level}"


class Section(models.Model):
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    adviser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'}, related_name='advised_sections')
    
    def __str__(self):
        return f"{self.grade} - {self.name}"


class TeacherAssignment(models.Model):
    """Model to store teacher assignments to specific grade/track/section combinations"""
    teacher_name = models.CharField(max_length=200)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True, blank=True)
    track_code = models.CharField(max_length=20)  # STE, SPA, ICT, RBEC, STVEP, STEM, etc.
    grade_level = models.CharField(max_length=10)
    section_name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['teacher_name', 'grade_level', 'section_name', 'track_code']
    
    def __str__(self):
        curriculum_name = self.curriculum.name if self.curriculum else 'N/A'
        return f"{self.teacher_name} - {curriculum_name} Grade {self.grade_level} {self.section_name} ({self.track_code})"


class IncidentType(models.Model):
    SEVERITY_CHOICES = [
        ('prohibited', 'Prohibited Acts'),
        ('school_policy', 'Other School Policies'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    legal_references = models.TextField(help_text="Legal references and documents")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['severity', 'name']


class LegalReference(models.Model):
    title = models.CharField(max_length=200)
    reference_number = models.CharField(max_length=50)
    description = models.TextField()
    incident_types = models.ManyToManyField(IncidentType)
    
    def __str__(self):
        return f"{self.reference_number} - {self.title}"


class IncidentReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('classified', 'Classified'),
        ('evaluated', 'Evaluated'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    case_id = models.CharField(max_length=50, unique=True)
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_filed')
    
    # Reporter details
    reporter_first_name = models.CharField(max_length=100)
    reporter_middle_name = models.CharField(max_length=100, blank=True)
    reporter_last_name = models.CharField(max_length=100)
    
    # Involved students
    involved_students = models.TextField(help_text="Names or IDs of involved students", blank=True)
    student_gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female')
    ], blank=True, help_text="Gender of the involved student")
    
    # Academic details
    curriculum = models.ForeignKey(Curriculum, on_delete=models.SET_NULL, null=True)
    grade_level = models.CharField(max_length=10)  # Store grade level directly (7, 8, 9, 10, 11, 12)
    section_name = models.CharField(max_length=100)  # Store section name directly
    teacher_name = models.CharField(max_length=200, blank=True)  # Store teacher name directly
    
    # Keep old fields for backward compatibility (can be removed later)
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='incidents_as_teacher', limit_choices_to={'role': 'teacher'})
    
    # Incident details
    incident_date = models.DateField()
    incident_time = models.TimeField()
    incident_type = models.ForeignKey(IncidentType, on_delete=models.SET_NULL, null=True)
    bullying_type = models.CharField(max_length=50, blank=True, null=True, 
                                    help_text="Type of bullying if incident_type is bullying")
    description = models.TextField(blank=True)
    evidence = models.FileField(upload_to='evidence/', null=True, blank=True)
    
    # System fields
    reported_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incident_reports', 
                                       limit_choices_to={'role': 'student'}, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    evidence_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Review'),
        ('clear', 'Clear - Sufficient Evidence'),
        ('insufficient', 'Needs More Evidence')
    ], default='pending', blank=True)
    evidence_notes = models.TextField(blank=True, help_text="Notes about evidence status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Proper Process System Fields
    reporter_is_victim = models.BooleanField(
        default=False,
        help_text="Check if reporter is also a victim/involved party"
    )
    is_confidential = models.BooleanField(
        default=False,
        help_text="Mark as confidential (recommended for teacher incidents)"
    )
    involved_parties = models.ManyToManyField(
        'InvolvedParty',
        related_name='incident_reports',
        blank=True,
        help_text="Students or teachers involved in this incident"
    )
    
    def __str__(self):
        return f"{self.case_id} - {self.reported_student}"
    
    def save(self, *args, **kwargs):
        if not self.case_id:
            year = timezone.now().year
            count = IncidentReport.objects.filter(created_at__year=year).count() + 1
            self.case_id = f"{year}-{count:04d}"
        super().save(*args, **kwargs)


class Classification(models.Model):
    ROUTING_CHOICES = [
        ('minor', 'Handle by DO'),
        ('major', 'Send to Guidance Counselor')
    ]
    
    report = models.OneToOneField(IncidentReport, on_delete=models.CASCADE, related_name='classification')
    classified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'do'})
    severity = models.CharField(max_length=10, choices=ROUTING_CHOICES, help_text="Routing decision: DO or Counselor")
    internal_notes = models.TextField(blank=True, help_text="Notes about routing decision")
    classified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.report.case_id} - {self.get_severity_display()}"
    
    def get_routing_destination(self):
        """Returns the destination for this case"""
        if self.severity == 'minor':
            return 'Discipline Office'
        else:
            return 'Guidance Counselor'


class CounselingSession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('referred_to_teacher', 'Referred to Teacher'),
    ]
    
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='counseling_sessions', null=True, blank=True)
    counselor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'counselor'})
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='counseling_sessions', limit_choices_to={'role': 'student'})
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Counseling - {self.student} ({self.scheduled_date})"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Notification Tracking Fields
    NOTIFICATION_TYPE_CHOICES = [
        ('report_submitted', 'Report Submitted'),
        ('party_confirmed', 'Party Confirmed'),
        ('do_classified', 'DO Classified'),
        ('guidance_evaluation', 'Guidance Evaluation'),
        ('vrf_assigned', 'VRF Assigned'),
        ('counseling_scheduled', 'Counseling Scheduled'),
        ('session_completed', 'Session Completed'),
        ('status_update', 'Status Update'),
    ]
    
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='status_update'
    )
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.user}"


class ViolationHistory(models.Model):
    """Track student violation history for pattern detection"""
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='violation_history', limit_choices_to={'role': 'student'})
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    violation_type = models.ForeignKey(IncidentType, on_delete=models.SET_NULL, null=True)
    severity = models.CharField(max_length=10, choices=[('minor', 'Minor'), ('major', 'Major')])
    date_occurred = models.DateField()
    status = models.CharField(max_length=20, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_occurred']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.violation_type} ({self.date_occurred})"


class CaseEvaluation(models.Model):
    """Guidance counselor evaluation of cases"""
    VERDICT_CHOICES = [
        ('pending', 'Pending Investigation'),
        ('guilty', 'Guilty'),
        ('not_guilty', 'Not Guilty'),
        ('insufficient_evidence', 'Insufficient Evidence'),
    ]
    
    report = models.OneToOneField(IncidentReport, on_delete=models.CASCADE, related_name='evaluation')
    evaluated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'counselor'})
    evaluation_notes = models.TextField(blank=True)
    recommendation = models.CharField(max_length=20, choices=[
        ('counseling', 'Counseling Only'),
        ('monitoring', 'Monitoring Required'),
        ('resolved', 'Case Resolved')
    ])
    verdict = models.CharField(max_length=30, choices=VERDICT_CHOICES, default='pending', help_text="Determination of guilt")
    verdict_notes = models.TextField(blank=True, help_text="Explanation for the verdict")
    is_repeat_offender = models.BooleanField(default=False)
    related_cases = models.ManyToManyField(IncidentReport, blank=True, related_name='related_evaluations')
    evaluated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evaluation - {self.report.case_id}"
    
    def get_verdict_badge_color(self):
        """Return color class for verdict badge"""
        colors = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'guilty': 'bg-red-100 text-red-800',
            'not_guilty': 'bg-green-100 text-green-800',
            'insufficient_evidence': 'bg-gray-100 text-gray-800',
        }
        return colors.get(self.verdict, 'bg-gray-100 text-gray-800')


class InternalNote(models.Model):
    """Internal notes for DO and staff"""
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='internal_notes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note = models.TextField()
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note by {self.author.get_full_name()} - {self.report.case_id}"


class Counselor(models.Model):
    """Counselor information for pre-counseling selection"""
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=200, blank=True, help_text="e.g., Academic, Behavioral, Career")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        """Auto-capitalize name before saving"""
        if self.name:
            self.name = self.name.title()
        if self.specialization:
            self.specialization = self.specialization.title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class SystemBackup(models.Model):
    """Track system backups"""
    backup_name = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=20, choices=[
        ('manual', 'Manual'),
        ('scheduled', 'Scheduled'),
        ('emergency', 'Emergency')
    ])
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'counselor'})
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Backup - {self.backup_name} ({self.created_at})"


class ReportAnalytics(models.Model):
    """Store analytics data for reports"""
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    total_reports = models.IntegerField(default=0)
    minor_violations = models.IntegerField(default=0)
    major_violations = models.IntegerField(default=0)
    resolved_cases = models.IntegerField(default=0)
    pending_cases = models.IntegerField(default=0)
    most_common_violation = models.CharField(max_length=200, blank=True)
    grade_with_most_violations = models.CharField(max_length=10, blank=True)
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analytics {self.date_range_start} to {self.date_range_end}"


class VPFCase(models.Model):
    """Values Reflective Formation cases assigned by counselors"""
    STATUS_CHOICES = [
        ('pending', 'Pending Schedule'),
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='vpf_cases')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vpf_assignments', limit_choices_to={'role': 'student'})
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='vpf_assigned', limit_choices_to={'role': 'counselor'})
    esp_teacher_assigned = models.ForeignKey('Counselor', on_delete=models.SET_NULL, null=True, blank=True, related_name='vpf_cases_assigned', help_text="ESP Teacher/VPF Counselor assigned to this case")
    commission_level = models.CharField(max_length=10, help_text="1st, 2nd, or 3rd Commission")
    intervention = models.CharField(max_length=200, help_text="Selected intervention type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"VPF - {self.student.get_full_name()} - {self.report.case_id}"


class VPFSchedule(models.Model):
    """VPF counseling schedule managed by ESP Teacher"""
    vpf_case = models.ForeignKey(VPFCase, on_delete=models.CASCADE, related_name='schedules')
    esp_teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='vpf_schedules_managed', limit_choices_to={'role': 'esp_teacher'})
    counselor_assigned = models.ForeignKey('Counselor', on_delete=models.SET_NULL, null=True, blank=True, help_text="VPF Counselor assigned")
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
    ], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"VPF Schedule - {self.vpf_case.student.get_full_name()} - {self.scheduled_date.strftime('%Y-%m-%d %H:%M')}"


class CounselingSchedule(models.Model):
    """Counseling schedule for non-VPF interventions"""
    evaluation = models.ForeignKey(CaseEvaluation, on_delete=models.CASCADE, related_name='counseling_schedules')
    counselor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='counseling_schedules_managed', limit_choices_to={'role': 'counselor'})
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='counseling_schedule_assignments', limit_choices_to={'role': 'student'})
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
    ], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"Counseling Schedule - {self.student.get_full_name()} - {self.scheduled_date.strftime('%Y-%m-%d %H:%M')}"


class DOSchedule(models.Model):
    """Schedule for Discipline Officer parent conferences and interviews"""
    SCHEDULE_TYPE_CHOICES = [
        ('parent_conference', 'Parent Conference'),
        ('interview', 'Interview'),
        ('follow_up', 'Follow-up Meeting'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    ]
    
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='do_schedules', null=True, blank=True)
    discipline_officer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='do_schedules_managed', limit_choices_to={'role': 'do'})
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='do_schedule_assignments', limit_choices_to={'role': 'student'}, null=True, blank=True)
    schedule_type = models.CharField(max_length=30, choices=SCHEDULE_TYPE_CHOICES, default='parent_conference')
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, default='Discipline Office')
    attendees = models.TextField(blank=True, help_text="Names of attendees (parents, guardians, etc.)")
    purpose = models.TextField(blank=True, help_text="Purpose of the meeting")
    notes = models.TextField(blank=True, help_text="Meeting notes or outcomes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        student_name = self.student.get_full_name() if self.student else 'No student'
        return f"DO Schedule - {self.get_schedule_type_display()} - {student_name} - {self.scheduled_date.strftime('%Y-%m-%d %H:%M')}"


class InvolvedParty(models.Model):
    """Model to track involved parties (students or teachers) in incident reports"""
    PARTY_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    party_type = models.CharField(max_length=20, choices=PARTY_TYPE_CHOICES)
    
    # For students
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'student'},
        related_name='student_involved_parties'
    )
    curriculum = models.ForeignKey('Curriculum', on_delete=models.SET_NULL, null=True, blank=True)
    grade_level = models.CharField(max_length=10, null=True, blank=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True)
    adviser = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='advised_involved_parties'
    )
    
    # For teachers
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='teacher_involved_parties'
    )
    department = models.CharField(max_length=100, null=True, blank=True)
    grade_level_taught = models.CharField(max_length=50, null=True, blank=True)
    
    # Common fields
    name_if_unknown = models.CharField(max_length=200, null=True, blank=True, help_text="Name if party not in system")
    is_confirmed = models.BooleanField(default=False, help_text="Confirmed by DO")
    confirmed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_parties'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Involved Party'
        verbose_name_plural = 'Involved Parties'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.party_type == 'student' and self.student:
            return f"Student: {self.student.get_full_name()}"
        elif self.party_type == 'teacher' and self.teacher:
            return f"Teacher: {self.teacher.get_full_name()}"
        elif self.name_if_unknown:
            return f"Unknown {self.party_type}: {self.name_if_unknown}"
        return f"Unknown {self.party_type}"
    
    def get_display_name(self):
        """Get display name for the involved party"""
        if self.party_type == 'student' and self.student:
            return self.student.get_full_name()
        elif self.party_type == 'teacher' and self.teacher:
            return self.teacher.get_full_name()
        return self.name_if_unknown or "Unknown"
    
    def get_academic_info(self):
        """Get academic info string for display"""
        if self.party_type == 'student':
            if self.section:
                adviser_name = self.adviser.get_full_name() if self.adviser else "No adviser"
                return f"G{self.grade_level} - {self.section.name}, {adviser_name}"
            elif self.grade_level:
                return f"Grade {self.grade_level}"
            return "Academic info pending"
        elif self.party_type == 'teacher':
            parts = []
            if self.department:
                parts.append(self.department)
            if self.grade_level_taught:
                parts.append(f"Grade {self.grade_level_taught}")
            return ", ".join(parts) if parts else "Department info pending"
        return ""


# Update IncidentReport model with proper process fields
# Add these fields to your IncidentReport model:
# reporter_is_victim = models.BooleanField(default=False, help_text="Check if reporter is also a victim/involved party")
# is_confidential = models.BooleanField(default=False, help_text="Mark as confidential (recommended for teacher incidents)")
# involved_parties = models.ManyToManyField('InvolvedParty', related_name='incident_reports', blank=True, help_text="Students or teachers involved in this incident")

# Update Notification model with tracking fields
# Add these fields to your Notification model:
# NOTIFICATION_TYPE_CHOICES = [
#     ('report_submitted', 'Report Submitted'),
#     ('party_confirmed', 'Party Confirmed'),
#     ('do_classified', 'DO Classified'),
#     ('guidance_evaluation', 'Guidance Evaluation'),
#     ('vrf_assigned', 'VRF Assigned'),
#     ('counseling_scheduled', 'Counseling Scheduled'),
#     ('session_completed', 'Session Completed'),
#     ('status_update', 'Status Update'),
# ]
# notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, default='status_update')
# email_sent = models.BooleanField(default=False)
# email_sent_at = models.DateTimeField(null=True, blank=True)
