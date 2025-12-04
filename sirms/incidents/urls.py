from django.urls import path
from . import views
from . import oauth_views
from . import direct_report_views
from . import export_views
from . import completed_sessions_views
from . import completed_reports_views
from . import incident_type_views
from . import do_schedule_views
from . import behavior_concerns_views
from . import esp_teacher_views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    
    # Google OAuth URLs
    path('auth/google/', oauth_views.google_login, name='google_login'),
    path('auth/callback/', oauth_views.google_callback, name='google_callback'),
    path('auth/logout/', oauth_views.google_logout, name='google_logout'),
    path('auth/no-access/', oauth_views.no_access, name='no_access'),
    
    # Traditional auth (keep for backward compatibility)
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('report-incident/', views.report_incident, name='report_incident'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('all-reports/', views.all_reports, name='all_reports'),
    path('report/<str:case_id>/', views.report_detail, name='report_detail'),
    path('counseling-schedule/', views.counseling_schedule, name='counseling_schedule'),
    path('sanction/<str:case_id>/', views.create_sanction, name='create_sanction'),
    path('notifications/', views.notifications, name='notifications'),
    path('schedule-notification/<int:notification_id>/', views.schedule_notification_detail, name='schedule_notification_detail'),
    path('account-settings/', views.account_settings, name='account_settings'),
    
    # API endpoints for dynamic dropdowns
    path('api/tracks/', views.get_tracks, name='get_tracks'),
    path('api/dashboard-analytics/', views.get_dashboard_analytics, name='get_dashboard_analytics'),
    
    # Test page for charts
    path('test-charts/', views.test_charts, name='test_charts'),
    path('simple-chart-test/', views.simple_chart_test, name='simple_chart_test'),
    path('api/grades/', views.get_grades, name='get_grades'),
    path('api/sections/', views.get_sections, name='get_sections'),
    path('api/teachers/', views.get_teachers, name='get_teachers'),
    
    # Student-specific URLs
    path('violation-history/', views.violation_history, name='violation_history'),
    path('legal-references/', views.legal_references, name='legal_references'),
    
    # Teacher-specific URLs
    path('advisee-records/', views.advisee_records, name='advisee_records'),
    
    # DO-specific URLs
    path('fact-check-reports/', views.fact_check_reports, name='fact_check_reports'),
    path('behavior-concerns/', behavior_concerns_views.behavior_concerns, name='behavior_concerns'),
    path('classify-violations/', views.classify_violations, name='classify_violations'),  # Backward compatibility
    path('pre-counseling-schedule/', views.pre_counseling_schedule, name='pre_counseling_schedule'),
    path('case-history/', views.case_history, name='case_history'),
    path('internal-notes/', views.internal_notes, name='internal_notes'),
    path('direct-report/', direct_report_views.direct_report, name='direct_report'),  # Direct Report for DO and Guidance
    path('do-schedule/', do_schedule_views.do_schedule, name='do_schedule'),
    path('do-schedule/create/', do_schedule_views.create_do_schedule, name='create_do_schedule'),
    path('do-schedule/<int:schedule_id>/update/', do_schedule_views.update_do_schedule_status, name='update_do_schedule_status'),
    path('do-schedule/<int:schedule_id>/delete/', do_schedule_views.delete_do_schedule, name='delete_do_schedule'),
    
    # Counselor-specific URLs
    path('major-case-review/', views.major_case_review, name='major_case_review'),
    path('major-case-detail/<int:case_id>/', views.major_case_detail, name='major_case_detail'),
    path('counseling-management/', views.counseling_management, name='counseling_management'),
    path('counseling/session/<int:session_id>/complete/', views.complete_counseling_session, name='complete_counseling_session'),
    path('counseling/session/<int:session_id>/reschedule/', views.reschedule_counseling_session, name='reschedule_counseling_session'),
    path('counseling/session/<int:session_id>/cancel/', views.cancel_counseling_session, name='cancel_counseling_session'),
    path('case-evaluation/', views.case_evaluation, name='case_evaluation'),
    path('counselor-schedule/', views.counselor_schedule, name='counselor_schedule'),
    path('completed-sessions/', completed_sessions_views.completed_sessions, name='completed_sessions'),
    path('prohibited-acts/', incident_type_views.prohibited_acts, name='prohibited_acts'),
    path('other-school-policies/', incident_type_views.other_school_policies, name='other_school_policies'),
    path('counseling-schedule/complete/<int:schedule_id>/', views.complete_counseling_schedule, name='complete_counseling_schedule'),
    path('counseling-schedule/missed/<int:schedule_id>/', views.missed_counseling_schedule, name='missed_counseling_schedule'),
    
    # Principal-specific URLs
    path('evaluated-cases/', views.evaluated_cases, name='evaluated_cases'),
    path('sanction-management/', views.sanction_management, name='sanction_management'),
    path('final-verdicts/', views.final_verdicts, name='final_verdicts'),
    path('student-monitoring/', views.student_monitoring, name='student_monitoring'),
    
    # Shared URLs
    path('reports-analytics/', views.reports_analytics, name='reports_analytics'),
    
    # ESP Teacher / VPF URLs
    path('vpf-cases/', views.vpf_cases, name='vpf_cases'),
    path('vpf/update-status/<int:vpf_id>/', views.update_vpf_status, name='update_vpf_status'),
    path('vpf-schedule/', views.vpf_schedule, name='vpf_schedule'),
    path('assign-vpf-teacher/', views.assign_vpf_teacher, name='assign_vpf_teacher'),
    
    # API endpoints for dashboard analytics
    path('api/dashboard-data/', views.dashboard_analytics_api, name='dashboard_analytics_api'),
    path('api/export/', views.export_report_api, name='export_report_api'),
    path('export-analytics/', views.export_analytics, name='export_analytics'),
    
    # Export URLs
    path('export-all-reports-excel/', export_views.export_all_reports_excel, name='export_all_reports_excel'),
    path('export-behavior-concerns-excel/', export_views.export_behavior_concerns_excel, name='export_behavior_concerns_excel'),
    path('export-completed-reports-excel/', export_views.export_completed_reports_excel, name='export_completed_reports_excel'),
    
    # Counselor Completed Reports
    path('completed-reports/', completed_reports_views.completed_reports, name='completed_reports'),
    
    # Maintenance URLs (Counselor only)
    path('manage-curriculum/', views.manage_curriculum, name='manage_curriculum'),
    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('manage-incident-types/', views.manage_incident_types, name='manage_incident_types'),
    path('manage-legal-references/', views.manage_legal_references, name='manage_legal_references'),
    path('manage-counselors/', views.manage_counselors, name='manage_counselors'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('backup-restore/', views.backup_restore, name='backup_restore'),
    
    # ESP Teacher Management URLs
    path('manage-esp-teachers/', esp_teacher_views.manage_esp_teachers, name='manage_esp_teachers'),
    path('esp-teacher/add/', esp_teacher_views.add_esp_teacher, name='add_esp_teacher'),
    path('esp-teacher/<int:teacher_id>/edit/', esp_teacher_views.edit_esp_teacher, name='edit_esp_teacher'),
    path('esp-teacher/<int:teacher_id>/delete/', esp_teacher_views.delete_esp_teacher, name='delete_esp_teacher'),
    path('vpf-case/<int:vpf_case_id>/assign-teacher/', esp_teacher_views.assign_esp_teacher_to_vpf, name='assign_esp_teacher_to_vpf'),
    path('for-vpf/', esp_teacher_views.for_vpf_cases, name='for_vpf'),
]
