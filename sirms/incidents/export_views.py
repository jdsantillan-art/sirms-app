"""
Export Views for SIRMS
Handles Excel export functionality for reports
"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
from .models import IncidentReport


@login_required
def export_all_reports_excel(request):
    """
    Export all reports to Excel for DO and authorized users
    """
    # Check permissions
    if request.user.role not in ['do', 'counselor', 'principal']:
        messages.error(request, 'You do not have permission to export reports.')
        return redirect('dashboard')
    
    # Get all reports
    reports = IncidentReport.objects.all().select_related(
        'incident_type', 'reported_student', 'reporter', 'classification'
    ).order_by('-created_at')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "All Reports"
    
    # Define styles
    header_fill = PatternFill(start_color="2E8B57", end_color="2E8B57", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Headers
    headers = [
        'Case ID', 'Status', 'Student Name', 'Student Gender', 'Grade', 'Section',
        'Incident Type', 'Type Category', 'Incident Date', 'Incident Time',
        'Reporter Name', 'Reporter Role', 'Description', 'Classification',
        'Reported Date', 'Days Open'
    ]
    
    # Write headers
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border
    
    # Write data
    for row_idx, report in enumerate(reports, start=2):
        # Calculate days open
        days_open = (datetime.now().date() - report.created_at.date()).days
        
        # Get student name
        student_name = report.reported_student.get_full_name() if report.reported_student else report.involved_students
        
        # Get classification
        classification = ""
        if hasattr(report, 'classification'):
            classification = report.classification.get_severity_display()
        
        # Get type category
        type_category = ""
        if report.incident_type:
            type_category = "Prohibited Acts" if report.incident_type.severity == 'prohibited' else "School Policies"
        
        data = [
            report.case_id,
            report.get_status_display(),
            student_name,
            report.student_gender.title() if report.student_gender else 'Not specified',
            f"Grade {report.grade_level}",
            report.section_name,
            report.incident_type.name if report.incident_type else 'Not specified',
            type_category,
            report.incident_date.strftime('%Y-%m-%d') if report.incident_date else '',
            report.incident_time.strftime('%H:%M') if report.incident_time else '',
            f"{report.reporter_first_name} {report.reporter_last_name}",
            report.reporter.get_role_display() if report.reporter else '',
            report.description[:100] + '...' if len(report.description) > 100 else report.description,
            classification,
            report.created_at.strftime('%Y-%m-%d %H:%M'),
            days_open
        ]
        
        for col, value in enumerate(data, start=1):
            cell = ws.cell(row=row_idx, column=col, value=value)
            cell.border = border
            cell.alignment = Alignment(vertical='top', wrap_text=True)
    
    # Adjust column widths
    column_widths = {
        'A': 12,  # Case ID
        'B': 15,  # Status
        'C': 20,  # Student Name
        'D': 12,  # Gender
        'E': 10,  # Grade
        'F': 20,  # Section
        'G': 30,  # Incident Type
        'H': 18,  # Type Category
        'I': 12,  # Incident Date
        'J': 10,  # Incident Time
        'K': 20,  # Reporter Name
        'L': 15,  # Reporter Role
        'M': 40,  # Description
        'N': 15,  # Classification
        'O': 18,  # Reported Date
        'P': 10,  # Days Open
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Freeze header row
    ws.freeze_panes = 'A2'
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'SIRMS_All_Reports_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Save workbook to response
    wb.save(response)
    
    return response
