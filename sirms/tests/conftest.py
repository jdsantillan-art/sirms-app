"""
Pytest configuration and fixtures for SIRMS testing
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from incidents.models import (
    CustomUser, Curriculum, Track, Grade, Section, IncidentType,
    IncidentReport, Classification, CounselingSession, Notification
)
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def client():
    """Django test client"""
    return Client()


@pytest.fixture
def student_user(db):
    """Create a test student user"""
    return CustomUser.objects.create_user(
        username='teststudent',
        email='test.student@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Student',
        role='student',
        grade_level='10',
        section='Section 1'
    )


@pytest.fixture
def teacher_user(db):
    """Create a test teacher user"""
    return CustomUser.objects.create_user(
        username='testteacher',
        email='test.teacher@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Teacher',
        role='teacher',
        employee_id='T001'
    )


@pytest.fixture
def do_user(db):
    """Create a test discipline officer user"""
    return CustomUser.objects.create_user(
        username='testdo',
        email='test.do@example.com',
        password='testpass123',
        first_name='Test',
        last_name='DO',
        role='do',
        employee_id='DO001'
    )


@pytest.fixture
def counselor_user(db):
    """Create a test counselor user"""
    return CustomUser.objects.create_user(
        username='testcounselor',
        email='test.counselor@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Counselor',
        role='counselor',
        employee_id='C001'
    )


@pytest.fixture
def principal_user(db):
    """Create a test principal user"""
    return CustomUser.objects.create_user(
        username='testprincipal',
        email='test.principal@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Principal',
        role='principal',
        employee_id='P001'
    )


@pytest.fixture
def curriculum(db):
    """Create a test curriculum"""
    return Curriculum.objects.create(
        name='Junior High School',
        description='Grades 7-10'
    )


@pytest.fixture
def incident_type(db):
    """Create a test incident type"""
    return IncidentType.objects.create(
        name='Bullying',
        description='Physical or verbal bullying',
        severity='grave',
        legal_references='RA 10627 - Anti-Bullying Act'
    )


@pytest.fixture
def incident_report(db, teacher_user, student_user, curriculum, incident_type):
    """Create a test incident report"""
    return IncidentReport.objects.create(
        reporter=teacher_user,
        reporter_first_name='Test',
        reporter_last_name='Teacher',
        reported_student=student_user,
        curriculum=curriculum,
        grade_level='10',
        section_name='Section 1',
        teacher_name='Test Teacher',
        incident_date=timezone.now().date(),
        incident_time=timezone.now().time(),
        incident_type=incident_type,
        description='Test incident description',
        status='pending'
    )


@pytest.fixture
def classification(db, incident_report, do_user):
    """Create a test classification"""
    return Classification.objects.create(
        report=incident_report,
        classified_by=do_user,
        severity='major',
        internal_notes='Test classification notes'
    )


@pytest.fixture
def counseling_session(db, incident_report, counselor_user, student_user):
    """Create a test counseling session"""
    return CounselingSession.objects.create(
        report=incident_report,
        counselor=counselor_user,
        student=student_user,
        scheduled_date=timezone.now() + timedelta(days=1),
        status='scheduled',
        remarks='Test counseling session'
    )
