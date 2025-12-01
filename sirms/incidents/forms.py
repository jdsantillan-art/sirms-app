from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import (CustomUser, IncidentReport, CounselingSession, Classification,
                     Curriculum, Track, Grade, Section, IncidentType, TeacherAssignment,
                     ViolationHistory, CaseEvaluation, InternalNote, SystemBackup, ReportAnalytics,
                     LegalReference, DOSchedule)


class NoNAValidationMixin:
    """Mixin to prevent N/A values in form fields"""
    
    def clean(self):
        cleaned_data = super().clean()
        na_values = ['n/a', 'na', 'n.a.', 'n.a', 'not applicable', 'none', '-']
        
        # Create a list of items to avoid modifying dict during iteration
        for field_name, value in list(cleaned_data.items()):
            if isinstance(value, str):
                # Check if value is N/A or similar
                if value.lower().strip() in na_values:
                    self.add_error(field_name, f'Please provide a valid value. "N/A" is not accepted.')
                # Check if field is required and empty
                field = self.fields.get(field_name)
                if field and field.required and not value.strip():
                    self.add_error(field_name, 'This field is required and cannot be empty.')
        
        return cleaned_data

class CustomUserCreationForm(NoNAValidationMixin, UserCreationForm):
    # Restrict role choices to only Student, Teacher, and ESP Teacher
    role = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('esp_teacher', 'ESP Teacher/VPF Coordinator'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full pl-8 pr-3 py-2 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none appearance-none bg-white'
        }),
        help_text='Select your role. Note: Counselor and Discipline Officer accounts are created by administrators.'
    )
    
    middle_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-8 pr-3 py-2 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'placeholder': 'Middle name (optional)'
        }),
        help_text='Optional: Enter your middle name'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'role')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip():
            raise ValidationError('First name is required.')
        return first_name.title()
    
    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')
        if middle_name and middle_name.strip():
            return middle_name.title()
        return ''
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip():
            raise ValidationError('Last name is required.')
        return last_name.title()

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'grade_level', 'section')

class IncidentReportForm(NoNAValidationMixin, forms.ModelForm):
    # Reporter details
    reporter_first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
        'placeholder': 'First name'
    }))
    reporter_middle_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
        'placeholder': 'Middle name'
    }))
    reporter_last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
        'placeholder': 'Last name'
    }))
    
    # Involved students
    involved_students = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none resize-none',
            'placeholder': 'Enter student email, username, or name (e.g., student@school.edu, student123, or John Doe)'
        }),
        help_text="Optional: Enter student email/username to auto-link, or just the name for record keeping. Can be added later by Discipline Officer if unknown."
    )
    
    # Student gender
    student_gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_student_gender'
        })
    )
    
    # Academic details - will be populated via JavaScript
    curriculum = forms.ModelChoiceField(
        queryset=Curriculum.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_curriculum'
        }),
        empty_label="Select Curriculum"
    )
    grade_level = forms.ChoiceField(
        choices=[('', 'Select Grade')] + [(str(i), f'Grade {i}') for i in range(7, 13)],
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_grade_level'
        }),
        required=False
    )
    section_name = forms.ChoiceField(
        choices=[('', 'Select Section')],
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_section_name'
        }),
        required=False
    )
    teacher_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl bg-gray-50 transition-all outline-none',
            'id': 'id_teacher_name',
            'readonly': True,
            'placeholder': 'Auto-filled'
        }),
        required=False
    )
    
    # Incident details
    incident_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none'
        })
    )
    incident_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none'
        })
    )
    incident_type = forms.ModelChoiceField(
        queryset=IncidentType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_incident_type'
        }),
        empty_label="Select Type"
    )
    bullying_type = forms.ChoiceField(
        choices=[
            ('', 'Select Bullying Type'),
            ('Physical', 'Physical Bullying'),
            ('Psychological', 'Psychological Bullying'),
            ('Sexual', 'Sexual Bullying'),
            ('Emotional', 'Emotional Bullying'),
            ('Cyber', 'Cyber Bullying'),
            ('Social', 'Social Bullying'),
            ('Gender-based', 'Gender-based Bullying'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
            'id': 'id_bullying_type'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none resize-none',
            'placeholder': 'Describe the incident'
        }),
        help_text="Manually describe the incident (optional)"
    )
    evidence = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png,.mp4,.mov'
        }),
        help_text="Upload files as evidence (optional)"
    )
    
    class Meta:
        model = IncidentReport
        fields = [
            'reporter_first_name', 'reporter_middle_name', 'reporter_last_name',
            'involved_students', 'student_gender', 'curriculum', 'grade_level', 'section_name', 'teacher_name',
            'incident_date', 'incident_time', 'incident_type', 'bullying_type', 'description', 'evidence'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up section choices - will be populated via JavaScript based on curriculum and grade
        # Define all possible sections for both JHS and SHS
        jhs_sections = [
            'Section 1 (STE)', 'Section 2 (STE)', 'Section 1 (SPA)', 'Section 2 (SPA)', 
            'Section 1 (ICT)', 'Section 2 (ICT)', 'Section 1 (RBEC)', 'Section 2 (RBEC)', 'Section 3 (RBEC)',
            'Section 1 (STVEP)', 'Section 2 (STVEP)', 'Section 3 (STVEP)', 'Section 4 (STVEP)', 'Section 5 (STVEP)',
            'Section 6 (STVEP)', 'Section 7 (STVEP)', 'Section 8 (STVEP)', 'Section 9 (STVEP)', 'Section 10 (STVEP)'
        ]
        
        shs_sections = [
            'STEM', 'Arts & Design', 'TVL – ICT', 'TVL – SMAW', 'TVL – EIM', 
            'TVL – Dressmaking', 'TVL – FBS', 'TVL – Bread & Pastry', 'TVL – CSS'
        ]
        
        # Combine all sections for the dropdown (will be filtered by JavaScript)
        all_sections = [('', 'Select Section')] + [(section, section) for section in jhs_sections + shs_sections]
        self.fields['section_name'].choices = all_sections
    
    def clean(self):
        cleaned_data = super().clean()
        grade_level = cleaned_data.get('grade_level')
        section_name = cleaned_data.get('section_name')
        curriculum = cleaned_data.get('curriculum')
        
        # Set defaults if not provided
        if not grade_level:
            cleaned_data['grade_level'] = 'Not specified'
        
        if not section_name:
            cleaned_data['section_name'] = 'Not specified'
        
        return cleaned_data

class ClassificationForm(forms.ModelForm):
    class Meta:
        model = Classification
        fields = ('severity', 'internal_notes')
        widgets = {
            'internal_notes': forms.Textarea(attrs={'rows': 3}),
        }

class CounselingSessionForm(forms.ModelForm):
    # Override student field to use email input instead of dropdown
    student_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter student email address...'
        }),
        label='Student Email',
        help_text='Enter the email address of the student who needs counseling'
    )
    
    class Meta:
        model = CounselingSession
        fields = ('scheduled_date', 'remarks')
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Optional notes about the session...'}),
        }
    
    def clean_student_email(self):
        email = self.cleaned_data.get('student_email')
        try:
            student = CustomUser.objects.get(email=email, role='student')
            return student
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('No student found with this email address. Please check and try again.')
        except CustomUser.MultipleObjectsReturned:
            raise forms.ValidationError('Multiple students found with this email. Please contact the administrator.')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.student = self.cleaned_data['student_email']
        if commit:
            instance.save()
        return instance


class CaseEvaluationForm(NoNAValidationMixin, forms.ModelForm):
    evaluation_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Enter detailed evaluation notes (optional)...'})
    )
    
    class Meta:
        model = CaseEvaluation
        fields = ('evaluation_notes', 'recommendation', 'verdict', 'verdict_notes', 'is_repeat_offender')
        widgets = {
            'recommendation': forms.Select(attrs={'class': 'form-control'}),
            'verdict': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'verdict_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Explain the reasoning for this verdict...'}),
            'is_repeat_offender': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InternalNoteForm(forms.ModelForm):
    class Meta:
        model = InternalNote
        fields = ('note', 'is_private')
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Add internal note...'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('name', 'curriculum')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'curriculum': forms.Select(attrs={'class': 'form-control'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('level', 'track')
        widgets = {
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'track': forms.Select(attrs={'class': 'form-control'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'grade', 'adviser')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'adviser': forms.Select(attrs={'class': 'form-control'}),
        }


class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = ('teacher_name', 'curriculum', 'track_code', 'grade_level', 'section_name')
        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter teacher name'}),
            'curriculum': forms.Select(attrs={'class': 'form-control'}),
            'track_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., STE, STEM, ICT'}),
            'grade_level': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select Grade'),
                ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'), ('10', 'Grade 10'),
                ('11', 'Grade 11'), ('12', 'Grade 12')
            ]),
            'section_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Section 1, STEM'}),
        }


class IncidentTypeForm(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ('name', 'description', 'severity', 'legal_references')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'legal_references': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class ReportAnalyticsForm(forms.Form):
    date_range_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_range_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    report_type = forms.ChoiceField(
        choices=[
            ('summary', 'Summary Report'),
            ('detailed', 'Detailed Report'),
            ('trends', 'Trend Analysis'),
            ('by_grade', 'By Grade Level'),
            ('by_violation', 'By Violation Type'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class LegalReferenceForm(forms.ModelForm):
    class Meta:
        model = LegalReference
        fields = ('title', 'reference_number', 'description', 'incident_types')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'incident_types': forms.CheckboxSelectMultiple(),
        }



class DOScheduleForm(forms.ModelForm):
    """Form for creating DO schedules (parent conferences, interviews)"""
    
    # Student email field for easy lookup
    student_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500',
            'placeholder': 'Enter student email address (optional)...'
        }),
        label='Student Email',
        help_text='Optional: Enter student email to link this schedule to a specific student'
    )
    
    class Meta:
        model = DOSchedule
        fields = ('schedule_type', 'scheduled_date', 'location', 'attendees', 'purpose', 'notes', 'status')
        widgets = {
            'schedule_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500',
                'placeholder': 'e.g., Discipline Office, Conference Room'
            }),
            'attendees': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500',
                'placeholder': 'List attendees (parents, guardians, teachers, etc.)'
            }),
            'purpose': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500',
                'placeholder': 'Describe the purpose of this meeting'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500',
                'placeholder': 'Add notes or outcomes after the meeting (optional)'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border-2 border-gray-300 rounded-lg outline-none focus:border-green-500'
            }),
        }
    
    def clean_student_email(self):
        email = self.cleaned_data.get('student_email')
        if email:
            try:
                student = CustomUser.objects.get(email=email, role='student')
                return student
            except CustomUser.DoesNotExist:
                raise forms.ValidationError('No student found with this email address.')
            except CustomUser.MultipleObjectsReturned:
                raise forms.ValidationError('Multiple students found with this email.')
        return None
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        student = self.cleaned_data.get('student_email')
        if student:
            instance.student = student
        if commit:
            instance.save()
        return instance
