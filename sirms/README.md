# SIRMS - School Incident Reporting & Management System

A comprehensive Django-based system for managing school incidents in compliance with DepEd Positive Discipline and national child-protection laws.

## Features

- Role-based access control (Student, Teacher, Discipline Officer, Guidance Counselor, Principal)
- Incident reporting and tracking
- Case classification and evaluation
- Counseling session management
- Sanction management
- Real-time notifications
- Analytics and reporting

## Installation

1. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Run migrations:
\`\`\`bash
python manage.py migrate
\`\`\`

4. Create a superuser:
\`\`\`bash
python manage.py createsuperuser
\`\`\`

5. Run the development server:
\`\`\`bash
python manage.py runserver
\`\`\`

6. Access the application at http://localhost:8000

## Usage

- Register as a new user with your role
- Login to access your role-specific dashboard
- File incident reports
- Track case status
- Manage counseling sessions
- Issue sanctions (Principal only)

## Admin Panel

Access the admin panel at http://localhost:8000/admin with your superuser credentials to manage:
- Users and roles
- Incident types
- Legal references
- Curriculum and sections
- All system data
