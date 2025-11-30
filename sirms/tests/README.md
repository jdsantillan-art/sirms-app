# SIRMS White-Box Testing Suite

This directory contains comprehensive white-box (code-based) tests for the SIRMS (Student Incident Reporting and Management System).

## Test Files

Each test file can be run independently using pytest:

### 1. **test_models.py** - Model Logic Tests
Tests internal model logic, data validation, and database constraints.

```bash
pytest tests/test_models.py -v
```

**What it tests:**
- CustomUser model (name capitalization, role validation, unique constraints)
- IncidentReport model (case_id generation, status management)
- Classification model (one-to-one relationships, severity validation)
- CounselingSession model (scheduling, status tracking)
- IncidentType model (severity choices)
- Notification model (read/unread status)
- Counselor model (name capitalization)
- CaseEvaluation model (verdict logic, badge colors)
- ViolationHistory model (student tracking)
- TeacherAssignment model (unique constraints)

### 2. **test_views.py** - View Logic Tests
Tests view functions, authentication, permissions, and workflows.

```bash
pytest tests/test_views.py -v
```

**What it tests:**
- Authentication views (login, logout, register)
- Dashboard views for all user roles (student, teacher, DO, counselor, principal)
- Incident report views (create, view, list)
- Classification views (DO classification workflow)
- Counseling views (schedule, sessions)
- Notification views (mark as read)
- Sanction views (principal-only access)
- Account settings views
- API endpoints (dynamic dropdowns)

### 3. **test_forms.py** - Form Validation Tests
Tests form validation logic, data cleaning, and business rules.

```bash
pytest tests/test_forms.py -v
```

**What it tests:**
- CustomUserCreationForm (email uniqueness, password validation, name capitalization)
- IncidentReportForm (required fields, N/A rejection, date validation)
- ClassificationForm (severity validation)
- CounselingSessionForm (student email validation)
- SanctionForm (sanction type and reason validation)
- CaseEvaluationForm (verdict validation, N/A rejection)
- InternalNoteForm (note content validation)
- IncidentTypeForm (severity and legal references)
- TeacherAssignmentForm (teacher and grade validation)

### 4. **test_google_auth.py** - OAuth Authentication Tests
Tests Google OAuth authentication backend and email validation.

```bash
pytest tests/test_google_auth.py -v
```

**What it tests:**
- GoogleOAuthBackend authentication logic
- Email format validation for all roles
- DMLMHS email pattern matching
- Token verification and exchange
- Helper functions (generate_dmlmhs_email, get_google_auth_url)
- Integration tests for full authentication flow

## Running All Tests

Run all tests at once:

```bash
pytest tests/ -v
```

## Running Specific Test Classes

Run a specific test class:

```bash
pytest tests/test_models.py::TestCustomUserModel -v
```

## Running Specific Test Methods

Run a specific test method:

```bash
pytest tests/test_models.py::TestCustomUserModel::test_user_creation_with_valid_data -v
```

## Test Coverage

To see test coverage:

```bash
pytest tests/ --cov=incidents --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Prerequisites

Make sure you have pytest and pytest-django installed:

```bash
pip install pytest pytest-django pytest-cov
```

## Test Database

Tests use a separate test database that is created and destroyed automatically. Your production database is never affected.

## Fixtures

Common test fixtures are defined in `conftest.py`:
- `client` - Django test client
- `student_user` - Test student user
- `teacher_user` - Test teacher user
- `do_user` - Test discipline officer user
- `counselor_user` - Test counselor user
- `principal_user` - Test principal user
- `curriculum` - Test curriculum
- `incident_type` - Test incident type
- `incident_report` - Test incident report
- `classification` - Test classification
- `counseling_session` - Test counseling session

## Writing New Tests

When adding new tests:

1. Follow the naming convention: `test_*.py`
2. Use descriptive test names: `test_what_is_being_tested`
3. Use pytest fixtures for common setup
4. Mark database tests with `@pytest.mark.django_db`
5. Test both success and failure cases
6. Test edge cases and boundary conditions

## Test Output

- `-v` flag shows verbose output with test names
- `--tb=short` shows shorter traceback on failures
- Tests are color-coded: green (pass), red (fail), yellow (skip)

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: pytest tests/ -v --cov=incidents
```

## Troubleshooting

**Issue: Tests fail with database errors**
- Solution: Make sure Django settings are configured correctly in pytest.ini

**Issue: Import errors**
- Solution: Run pytest from the sirms directory (where manage.py is located)

**Issue: Fixture not found**
- Solution: Check that conftest.py is in the tests directory

## Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test names should describe what they test
3. **Coverage**: Test both happy paths and error cases
4. **Speed**: Keep tests fast by using fixtures and mocking
5. **Maintenance**: Update tests when code changes

## Contact

For questions about the test suite, contact the development team.
