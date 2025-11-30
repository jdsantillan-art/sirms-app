"""
White-box testing for SIRMS Forms
Tests form validation, cleaning, and business logic
Run with: pytest tests/test_forms.py -v
"""
import pytest
from django.core.exceptions import ValidationError
from incidents.forms import (
    CustomUserCreationForm, IncidentReportForm, ClassificationForm,
    CounselingSessionForm, SanctionForm, CaseEvaluationForm,
    InternalNoteForm, IncidentTypeForm, TeacherAssignmentForm
)
from incidents.models import CustomUser
from django.utils import timezone


@pytest.mark.django_db
class TestCustomUserCreationForm:
    """Test user creation form validation"""
    
    def test_valid_user_creation_form(self):
        """Test form with valid data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
    
    def test_duplicate_email_validation(self, student_user):
        """Test that duplicate emails are rejected"""
        form_data = {
            'username': 'anotheruser',
            'email': 'test.student@example.com',  # Duplicate
            'first_name': 'Another',
            'last_name': 'User',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
    
    def test_password_mismatch_validation(self):
        """Test password mismatch validation"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors
    
    def test_first_name_required(self):
        """Test that first name is required"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': '',
            'last_name': 'User',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'first_name' in form.errors
    
    def test_last_name_required(self):
        """Test that last name is required"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': '',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'last_name' in form.errors
    
    def test_name_capitalization(self):
        """Test that names are capitalized"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'john',
            'last_name': 'doe',
            'role': 'student',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'


@pytest.mark.django_db
class TestIncidentReportForm:
    """Test incident report form validation"""
    
    def test_valid_incident_report_form(self, curriculum, incident_type):
        """Test form with valid data"""
        form_data = {
            'reporter_first_name': 'Test',
            'reporter_middle_name': '',
            'reporter_last_name': 'Reporter',
            'curriculum': curriculum.id,
            'grade_level': '10',
            'section_name': 'Section 1',
            'teacher_name': 'Test Teacher',
            'incident_date': timezone.now().date(),
            'incident_time': timezone.now().time(),
            'incident_type': incident_type.id,
            'description': 'Test incident description',
            'involved_students': 'Student 1, Student 2'
        }
        form = IncidentReportForm(data=form_data)
        assert form.is_valid()
    
    def test_reporter_first_name_required(self, curriculum, incident_type):
        """Test that reporter first name is required"""
        form_data = {
            'reporter_first_name': '',
            'reporter_last_name': 'Reporter',
            'curriculum': curriculum.id,
            'grade_level': '10',
            'section_name': 'Section 1',
            'incident_date': timezone.now().date(),
            'incident_time': timezone.now().time(),
            'incident_type': incident_type.id
        }
        form = IncidentReportForm(data=form_data)
        assert not form.is_valid()
    
    def test_na_value_rejection(self, curriculum, incident_type):
        """Test that N/A values are rejected"""
        form_data = {
            'reporter_first_name': 'Test',
            'reporter_last_name': 'n/a',  # Should be rejected
            'curriculum': curriculum.id,
            'grade_level': '10',
            'section_name': 'Section 1',
            'incident_date': timezone.now().date(),
            'incident_time': timezone.now().time(),
            'incident_type': incident_type.id
        }
        form = IncidentReportForm(data=form_data)
        assert not form.is_valid()
    
    def test_incident_date_required(self, curriculum, incident_type):
        """Test that incident date is required"""
        form_data = {
            'reporter_first_name': 'Test',
            'reporter_last_name': 'Reporter',
            'curriculum': curriculum.id,
            'grade_level': '10',
            'section_name': 'Section 1',
            'incident_time': timezone.now().time(),
            'incident_type': incident_type.id
        }
        form = IncidentReportForm(data=form_data)
        assert not form.is_valid()
        assert 'incident_date' in form.errors


@pytest.mark.django_db
class TestClassificationForm:
    """Test classification form validation"""
    
    def test_valid_classification_form(self):
        """Test form with valid data"""
        form_data = {
            'severity': 'minor',
            'internal_notes': 'Test classification notes'
        }
        form = ClassificationForm(data=form_data)
        assert form.is_valid()
    
    def test_severity_required(self):
        """Test that severity is required"""
        form_data = {
            'internal_notes': 'Test notes'
        }
        form = ClassificationForm(data=form_data)
        assert not form.is_valid()
        assert 'severity' in form.errors
    
    def test_severity_choices(self):
        """Test valid severity choices"""
        valid_severities = ['minor', 'major']
        for severity in valid_severities:
            form_data = {
                'severity': severity,
                'internal_notes': 'Test'
            }
            form = ClassificationForm(data=form_data)
            assert form.is_valid()


@pytest.mark.django_db
class TestCounselingSessionForm:
    """Test counseling session form validation"""
    
    def test_valid_counseling_session_form(self, student_user):
        """Test form with valid data"""
        form_data = {
            'student_email': student_user.email,
            'scheduled_date': timezone.now() + timezone.timedelta(days=1),
            'remarks': 'Test counseling session'
        }
        form = CounselingSessionForm(data=form_data)
        assert form.is_valid()
    
    def test_invalid_student_email(self):
        """Test form with non-existent student email"""
        form_data = {
            'student_email': 'nonexistent@example.com',
            'scheduled_date': timezone.now() + timezone.timedelta(days=1),
            'remarks': 'Test'
        }
        form = CounselingSessionForm(data=form_data)
        assert not form.is_valid()
        assert 'student_email' in form.errors
    
    def test_scheduled_date_required(self, student_user):
        """Test that scheduled date is required"""
        form_data = {
            'student_email': student_user.email,
            'remarks': 'Test'
        }
        form = CounselingSessionForm(data=form_data)
        assert not form.is_valid()
        assert 'scheduled_date' in form.errors


@pytest.mark.django_db
class TestSanctionForm:
    """Test sanction form validation"""
    
    def test_valid_sanction_form(self):
        """Test form with valid data"""
        form_data = {
            'sanction_type': 'suspension',
            'duration_days': 3,
            'reason': 'Repeated violations'
        }
        form = SanctionForm(data=form_data)
        assert form.is_valid()
    
    def test_sanction_type_required(self):
        """Test that sanction type is required"""
        form_data = {
            'duration_days': 3,
            'reason': 'Test reason'
        }
        form = SanctionForm(data=form_data)
        assert not form.is_valid()
        assert 'sanction_type' in form.errors
    
    def test_reason_required(self):
        """Test that reason is required"""
        form_data = {
            'sanction_type': 'warning',
            'duration_days': 0
        }
        form = SanctionForm(data=form_data)
        assert not form.is_valid()
        assert 'reason' in form.errors


@pytest.mark.django_db
class TestCaseEvaluationForm:
    """Test case evaluation form validation"""
    
    def test_valid_case_evaluation_form(self):
        """Test form with valid data"""
        form_data = {
            'evaluation_notes': 'Detailed evaluation notes',
            'recommendation': 'counseling',
            'verdict': 'guilty',
            'verdict_notes': 'Clear evidence of violation',
            'is_repeat_offender': False
        }
        form = CaseEvaluationForm(data=form_data)
        assert form.is_valid()
    
    def test_evaluation_notes_required(self):
        """Test that evaluation notes are required"""
        form_data = {
            'recommendation': 'counseling',
            'verdict': 'guilty',
            'verdict_notes': 'Test',
            'is_repeat_offender': False
        }
        form = CaseEvaluationForm(data=form_data)
        assert not form.is_valid()
    
    def test_verdict_required(self):
        """Test that verdict is required"""
        form_data = {
            'evaluation_notes': 'Test notes',
            'recommendation': 'counseling',
            'verdict_notes': 'Test',
            'is_repeat_offender': False
        }
        form = CaseEvaluationForm(data=form_data)
        assert not form.is_valid()
        assert 'verdict' in form.errors
    
    def test_na_value_rejection_in_evaluation(self):
        """Test that N/A values are rejected in evaluation"""
        form_data = {
            'evaluation_notes': 'n/a',  # Should be rejected
            'recommendation': 'counseling',
            'verdict': 'guilty',
            'verdict_notes': 'Test',
            'is_repeat_offender': False
        }
        form = CaseEvaluationForm(data=form_data)
        assert not form.is_valid()


@pytest.mark.django_db
class TestInternalNoteForm:
    """Test internal note form validation"""
    
    def test_valid_internal_note_form(self):
        """Test form with valid data"""
        form_data = {
            'note': 'This is an internal note',
            'is_private': True
        }
        form = InternalNoteForm(data=form_data)
        assert form.is_valid()
    
    def test_note_required(self):
        """Test that note content is required"""
        form_data = {
            'is_private': True
        }
        form = InternalNoteForm(data=form_data)
        assert not form.is_valid()
        assert 'note' in form.errors


@pytest.mark.django_db
class TestIncidentTypeForm:
    """Test incident type form validation"""
    
    def test_valid_incident_type_form(self):
        """Test form with valid data"""
        form_data = {
            'name': 'Vandalism',
            'description': 'Destruction of school property',
            'severity': 'grave',
            'legal_references': 'School Code Section 5'
        }
        form = IncidentTypeForm(data=form_data)
        assert form.is_valid()
    
    def test_name_required(self):
        """Test that name is required"""
        form_data = {
            'description': 'Test description',
            'severity': 'grave',
            'legal_references': 'Test ref'
        }
        form = IncidentTypeForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
    
    def test_severity_required(self):
        """Test that severity is required"""
        form_data = {
            'name': 'Test Incident',
            'description': 'Test description',
            'legal_references': 'Test ref'
        }
        form = IncidentTypeForm(data=form_data)
        assert not form.is_valid()
        assert 'severity' in form.errors


@pytest.mark.django_db
class TestTeacherAssignmentForm:
    """Test teacher assignment form validation"""
    
    def test_valid_teacher_assignment_form(self, curriculum):
        """Test form with valid data"""
        form_data = {
            'teacher_name': 'John Doe',
            'curriculum': curriculum.id,
            'track_code': 'STE',
            'grade_level': '10',
            'section_name': 'Section 1'
        }
        form = TeacherAssignmentForm(data=form_data)
        assert form.is_valid()
    
    def test_teacher_name_required(self, curriculum):
        """Test that teacher name is required"""
        form_data = {
            'curriculum': curriculum.id,
            'track_code': 'STE',
            'grade_level': '10',
            'section_name': 'Section 1'
        }
        form = TeacherAssignmentForm(data=form_data)
        assert not form.is_valid()
        assert 'teacher_name' in form.errors
    
    def test_grade_level_required(self, curriculum):
        """Test that grade level is required"""
        form_data = {
            'teacher_name': 'John Doe',
            'curriculum': curriculum.id,
            'track_code': 'STE',
            'section_name': 'Section 1'
        }
        form = TeacherAssignmentForm(data=form_data)
        assert not form.is_valid()
        assert 'grade_level' in form.errors
