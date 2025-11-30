"""
White-box testing for SIRMS Models
Tests internal logic, data validation, and model methods
Run with: pytest tests/test_models.py -v
"""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from incidents.models import (
    CustomUser, Curriculum, Track, Grade, Section, IncidentType,
    IncidentReport, Classification, CounselingSession, Sanction,
    Notification, ViolationHistory, CaseEvaluation, InternalNote,
    Counselor, TeacherAssignment
)


@pytest.mark.django_db
class TestCustomUserModel:
    """Test CustomUser model logic and validation"""
    
    def test_user_creation_with_valid_data(self):
        """Test creating user with valid data"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='john',
            last_name='doe',
            role='student'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.first_name == 'John'  # Should be capitalized
        assert user.last_name == 'Doe'  # Should be capitalized
        assert user.role == 'student'
    
    def test_user_name_auto_capitalization(self):
        """Test that names are automatically capitalized"""
        user = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='mary jane',
            last_name='smith',
            role='teacher'
        )
        assert user.first_name == 'Mary Jane'
        assert user.last_name == 'Smith'
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = CustomUser.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='counselor'
        )
        expected = "Test User (Guidance Counselor)"
        assert str(user) == expected
    
    def test_unique_employee_id_constraint(self):
        """Test that employee_id must be unique"""
        CustomUser.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='testpass123',
            role='teacher',
            employee_id='T001'
        )
        
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                username='teacher2',
                email='teacher2@example.com',
                password='testpass123',
                role='teacher',
                employee_id='T001'  # Duplicate
            )
    
    def test_role_choices_validation(self):
        """Test that only valid roles are accepted"""
        valid_roles = ['student', 'teacher', 'do', 'counselor', 'principal']
        for role in valid_roles:
            user = CustomUser.objects.create_user(
                username=f'user_{role}',
                email=f'{role}@example.com',
                password='testpass123',
                role=role
            )
            assert user.role == role


@pytest.mark.django_db
class TestIncidentReportModel:
    """Test IncidentReport model logic"""
    
    def test_case_id_auto_generation(self, teacher_user, incident_type, curriculum):
        """Test that case_id is automatically generated"""
        report = IncidentReport.objects.create(
            reporter=teacher_user,
            reporter_first_name='Test',
            reporter_last_name='Teacher',
            curriculum=curriculum,
            grade_level='10',
            section_name='Section 1',
            incident_date=timezone.now().date(),
            incident_time=timezone.now().time(),
            incident_type=incident_type
        )
        
        assert report.case_id is not None
        assert report.case_id.startswith(str(timezone.now().year))
        assert '-' in report.case_id
    
    def test_case_id_uniqueness(self, teacher_user, incident_type, curriculum):
        """Test that each report gets a unique case_id"""
        report1 = IncidentReport.objects.create(
            reporter=teacher_user,
            reporter_first_name='Test',
            reporter_last_name='Teacher',
            curriculum=curriculum,
            grade_level='10',
            section_name='Section 1',
            incident_date=timezone.now().date(),
            incident_time=timezone.now().time(),
            incident_type=incident_type
        )
        
        report2 = IncidentReport.objects.create(
            reporter=teacher_user,
            reporter_first_name='Test',
            reporter_last_name='Teacher',
            curriculum=curriculum,
            grade_level='10',
            section_name='Section 1',
            incident_date=timezone.now().date(),
            incident_time=timezone.now().time(),
            incident_type=incident_type
        )
        
        assert report1.case_id != report2.case_id
    
    def test_default_status_is_pending(self, teacher_user, incident_type, curriculum):
        """Test that new reports have pending status"""
        report = IncidentReport.objects.create(
            reporter=teacher_user,
            reporter_first_name='Test',
            reporter_last_name='Teacher',
            curriculum=curriculum,
            grade_level='10',
            section_name='Section 1',
            incident_date=timezone.now().date(),
            incident_time=timezone.now().time(),
            incident_type=incident_type
        )
        
        assert report.status == 'pending'
    
    def test_report_str_representation(self, incident_report):
        """Test report string representation"""
        result = str(incident_report)
        assert incident_report.case_id in result


@pytest.mark.django_db
class TestClassificationModel:
    """Test Classification model logic"""
    
    def test_classification_creation(self, incident_report, do_user):
        """Test creating a classification"""
        classification = Classification.objects.create(
            report=incident_report,
            classified_by=do_user,
            severity='minor',
            internal_notes='Test notes'
        )
        
        assert classification.report == incident_report
        assert classification.classified_by == do_user
        assert classification.severity == 'minor'
    
    def test_one_to_one_relationship(self, incident_report, do_user):
        """Test that a report can only have one classification"""
        Classification.objects.create(
            report=incident_report,
            classified_by=do_user,
            severity='minor'
        )
        
        with pytest.raises(IntegrityError):
            Classification.objects.create(
                report=incident_report,
                classified_by=do_user,
                severity='major'
            )
    
    def test_severity_choices(self, incident_report, do_user):
        """Test severity choices validation"""
        valid_severities = ['minor', 'major']
        for severity in valid_severities:
            classification = Classification.objects.create(
                report=incident_report,
                classified_by=do_user,
                severity=severity
            )
            assert classification.severity == severity
            classification.delete()


@pytest.mark.django_db
class TestCounselingSessionModel:
    """Test CounselingSession model logic"""
    
    def test_counseling_session_creation(self, counselor_user, student_user):
        """Test creating a counseling session"""
        scheduled_date = timezone.now() + timedelta(days=1)
        session = CounselingSession.objects.create(
            counselor=counselor_user,
            student=student_user,
            scheduled_date=scheduled_date,
            status='scheduled'
        )
        
        assert session.counselor == counselor_user
        assert session.student == student_user
        assert session.status == 'scheduled'
    
    def test_default_status_is_scheduled(self, counselor_user, student_user):
        """Test default status"""
        session = CounselingSession.objects.create(
            counselor=counselor_user,
            student=student_user,
            scheduled_date=timezone.now() + timedelta(days=1)
        )
        
        assert session.status == 'scheduled'
    
    def test_session_str_representation(self, counseling_session):
        """Test session string representation"""
        result = str(counseling_session)
        assert 'Counseling' in result


@pytest.mark.django_db
class TestIncidentTypeModel:
    """Test IncidentType model logic"""
    
    def test_incident_type_creation(self):
        """Test creating an incident type"""
        incident_type = IncidentType.objects.create(
            name='Vandalism',
            description='Destruction of school property',
            severity='grave',
            legal_references='School Code Section 5'
        )
        
        assert incident_type.name == 'Vandalism'
        assert incident_type.severity == 'grave'
    
    def test_severity_choices(self):
        """Test severity choices"""
        valid_severities = ['grave', 'prohibited']
        for severity in valid_severities:
            incident_type = IncidentType.objects.create(
                name=f'Test {severity}',
                description='Test description',
                severity=severity,
                legal_references='Test ref'
            )
            assert incident_type.severity == severity


@pytest.mark.django_db
class TestNotificationModel:
    """Test Notification model logic"""
    
    def test_notification_creation(self, student_user, incident_report):
        """Test creating a notification"""
        notification = Notification.objects.create(
            user=student_user,
            title='Test Notification',
            message='This is a test message',
            report=incident_report,
            is_read=False
        )
        
        assert notification.user == student_user
        assert notification.title == 'Test Notification'
        assert notification.is_read is False
    
    def test_default_is_read_false(self, student_user):
        """Test default is_read value"""
        notification = Notification.objects.create(
            user=student_user,
            title='Test',
            message='Test message'
        )
        
        assert notification.is_read is False


@pytest.mark.django_db
class TestCounselorModel:
    """Test Counselor model logic"""
    
    def test_counselor_creation(self):
        """Test creating a counselor"""
        counselor = Counselor.objects.create(
            name='john doe',
            email='john.doe@example.com',
            phone='1234567890',
            specialization='academic counseling'
        )
        
        assert counselor.name == 'John Doe'  # Auto-capitalized
        assert counselor.specialization == 'Academic Counseling'  # Auto-capitalized
        assert counselor.is_active is True
    
    def test_counselor_name_capitalization(self):
        """Test name auto-capitalization"""
        counselor = Counselor.objects.create(
            name='mary jane smith',
            email='mary@example.com'
        )
        
        assert counselor.name == 'Mary Jane Smith'


@pytest.mark.django_db
class TestCaseEvaluationModel:
    """Test CaseEvaluation model logic"""
    
    def test_case_evaluation_creation(self, incident_report, counselor_user):
        """Test creating a case evaluation"""
        evaluation = CaseEvaluation.objects.create(
            report=incident_report,
            evaluated_by=counselor_user,
            evaluation_notes='Test evaluation',
            recommendation='counseling',
            verdict='guilty',
            verdict_notes='Clear evidence'
        )
        
        assert evaluation.report == incident_report
        assert evaluation.verdict == 'guilty'
        assert evaluation.recommendation == 'counseling'
    
    def test_verdict_badge_color_method(self, incident_report, counselor_user):
        """Test get_verdict_badge_color method"""
        evaluation = CaseEvaluation.objects.create(
            report=incident_report,
            evaluated_by=counselor_user,
            evaluation_notes='Test',
            recommendation='counseling',
            verdict='guilty'
        )
        
        color = evaluation.get_verdict_badge_color()
        assert 'bg-red-100' in color
        assert 'text-red-800' in color


@pytest.mark.django_db
class TestViolationHistoryModel:
    """Test ViolationHistory model logic"""
    
    def test_violation_history_creation(self, student_user, incident_report, incident_type):
        """Test creating violation history"""
        history = ViolationHistory.objects.create(
            student=student_user,
            report=incident_report,
            violation_type=incident_type,
            severity='major',
            date_occurred=timezone.now().date()
        )
        
        assert history.student == student_user
        assert history.severity == 'major'
        assert history.status == 'active'


@pytest.mark.django_db
class TestTeacherAssignmentModel:
    """Test TeacherAssignment model logic"""
    
    def test_teacher_assignment_creation(self, curriculum):
        """Test creating teacher assignment"""
        assignment = TeacherAssignment.objects.create(
            teacher_name='John Doe',
            curriculum=curriculum,
            track_code='STE',
            grade_level='10',
            section_name='Section 1'
        )
        
        assert assignment.teacher_name == 'John Doe'
        assert assignment.track_code == 'STE'
        assert assignment.grade_level == '10'
    
    def test_unique_together_constraint(self, curriculum):
        """Test unique_together constraint"""
        TeacherAssignment.objects.create(
            teacher_name='John Doe',
            curriculum=curriculum,
            track_code='STE',
            grade_level='10',
            section_name='Section 1'
        )
        
        with pytest.raises(IntegrityError):
            TeacherAssignment.objects.create(
                teacher_name='John Doe',
                curriculum=curriculum,
                track_code='STE',
                grade_level='10',
                section_name='Section 1'
            )
