# 📋 All Code Changes Needed - Copy & Paste Guide

This file contains ALL the code changes you need to make to implement the proper process and notification system.

---

## ✅ WHAT'S ALREADY DONE:
1. InvolvedParty model - ADDED to models.py
2. notification_utils.py - CREATED
3. All documentation - CREATED

---

## 🔧 CHANGES YOU NEED TO MAKE:

### 1. Update IncidentReport Model in `incidents/models.py`

**Find the IncidentReport class and add these 3 fields:**

```python
class IncidentReport(models.Model):
    # ... all existing fields ...
    
    # ADD THESE 3 NEW FIELDS:
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
```

---

### 2. Update Notification Model in `incidents/models.py`

**Find the Notification class and add these 3 fields:**

```python
class Notification(models.Model):
    # ... all existing fields ...
    
    # ADD THESE 3 NEW FIELDS:
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
```

---

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Update Report Form Template `templates/report_incident.html`

**Add these sections to the form (after reporter information, before incident details):**

```html
<!-- Reporter is Victim Checkbox -->
<div class="mb-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
    <label class="flex items-center cursor-pointer">
        <input type="checkbox" name="reporter_is_victim" id="reporterIsVictim" class="mr-3 h-5 w-5">
        <span class="text-sm font-semibold text-gray-800">
            <i class="fas fa-user-check text-blue-600 mr-2"></i>
            I am a victim/involved party in this incident
        </span>
    </label>
    <p class="text-xs text-gray-600 mt-2 ml-8">
        Check this if you are directly involved in the incident you're reporting
    </p>
</div>

<!-- Party Type Selection -->
<div class="mb-4">
    <label class="block text-sm font-bold text-gray-800 mb-2">
        Involved Party Type <span class="text-red-500">*</span>
    </label>
    <select name="party_type" id="partyType" 
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none" 
            required>
        <option value="">-- Select Type --</option>
        <option value="student">👨‍🎓 Student</option>
        <option value="teacher">👨‍🏫 Teacher/Staff</option>
    </select>
</div>

<!-- Student Fields (existing - keep as is) -->
<div id="studentFields" style="display:none;">
    <!-- Your existing student fields here -->
</div>

<!-- Teacher Fields (NEW) -->
<div id="teacherFields" style="display:none;">
    <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
        <p class="text-sm text-purple-800 mb-3">
            <i class="fas fa-info-circle mr-2"></i>
            <strong>Note:</strong> Teacher incidents are handled confidentially by DO and Guidance.
        </p>
        
        <div class="mb-4">
            <label class="block text-sm font-bold text-gray-800 mb-2">
                Teacher Name <span class="text-red-500">*</span>
            </label>
            <input type="text" name="teacher_name" id="teacherName"
                   class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 outline-none"
                   placeholder="Enter teacher's full name">
        </div>
        
        <div class="mb-4">
            <label class="block text-sm font-bold text-gray-800 mb-2">
                Department/Subject
            </label>
            <input type="text" name="department" id="department"
                   class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 outline-none"
                   placeholder="e.g., Math Department, Science Department">
        </div>
        
        <div class="mb-4">
            <label class="flex items-center cursor-pointer">
                <input type="checkbox" name="is_confidential" id="isConfidential" class="mr-3 h-5 w-5" checked>
                <span class="text-sm font-semibold text-gray-800">
                    <i class="fas fa-lock text-purple-600 mr-2"></i>
                    Mark as confidential (recommended)
                </span>
            </label>
            <p class="text-xs text-gray-600 mt-2 ml-8">
                Confidential reports are only visible to DO and Guidance
            </p>
        </div>
    </div>
</div>

<!-- JavaScript to toggle fields -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const partyType = document.getElementById('partyType');
    const studentFields = document.getElementById('studentFields');
    const teacherFields = document.getElementById('teacherFields');
    const teacherName = document.getElementById('teacherName');
    
    partyType.addEventListener('change', function() {
        if (this.value === 'student') {
            studentFields.style.display = 'block';
            teacherFields.style.display = 'none';
            teacherName.removeAttribute('required');
        } else if (this.value === 'teacher') {
            studentFields.style.display = 'none';
            teacherFields.style.display = 'block';
            teacherName.setAttribute('required', 'required');
        } else {
            studentFields.style.display = 'none';
            teacherFields.style.display = 'none';
        }
    });
});
</script>
```

---

### 5. Update Report Submission View in `incidents/views.py`

**Find the `report_incident` function and update the POST section:**

```python
from .notification_utils import send_smart_notifications
from .models import InvolvedParty

def report_incident(request):
    if request.method == 'POST':
        # ... existing code to get form data ...
        
        # NEW: Get new fields
        reporter_is_victim = request.POST.get('reporter_is_victim') == 'on'
        is_confidential = request.POST.get('is_confidential') == 'on'
        party_type = request.POST.get('party_type')
        
        # Create report with new fields
        report = IncidentReport.objects.create(
            reporter=request.user,
            reporter_first_name=request.POST.get('reporter_first_name'),
            reporter_middle_name=request.POST.get('reporter_middle_name', ''),
            reporter_last_name=request.POST.get('reporter_last_name'),
            # ... all other existing fields ...
            reporter_is_victim=reporter_is_victim,  # NEW
            is_confidential=is_confidential,  # NEW
            status='pending',
        )
        
        # NEW: Create involved party based on type
        if party_type == 'student':
            # Student involved party
            involved_party = InvolvedParty.objects.create(
                party_type='student',
                student=reported_student if reported_student else None,
                name_if_unknown=request.POST.get('involved_students') if not reported_student else None,
                curriculum=curriculum if curriculum else None,
                grade_level=grade_level,
                section=section if section else None,
                adviser=None,  # Will be set by system
            )
            report.involved_parties.add(involved_party)
            
        elif party_type == 'teacher':
            # Teacher involved party
            teacher_name = request.POST.get('teacher_name')
            department = request.POST.get('department', '')
            
            involved_party = InvolvedParty.objects.create(
                party_type='teacher',
                name_if_unknown=teacher_name,
                department=department,
            )
            report.involved_parties.add(involved_party)
        
        # NEW: If reporter is victim, add them as involved party
        if reporter_is_victim and request.user.role == 'student':
            victim_party = InvolvedParty.objects.create(
                party_type='student',
                student=request.user,
                is_confirmed=True,
                confirmed_by=request.user,
                confirmed_at=timezone.now(),
            )
            report.involved_parties.add(victim_party)
        
        # NEW: Send smart notifications
        send_smart_notifications(report, 'report_submitted')
        
        messages.success(request, f'Report submitted successfully! Case ID: {report.case_id}')
        return redirect('my_reports')
```

---

### 6. Update All Reports Display in `templates/all_reports.html`

**Replace the "Student Name" column with "Involved Parties":**

```html
<!-- In the table header -->
<th class="px-3 py-2 text-left text-xs font-medium text-gray-500">Involved Parties</th>
<th class="px-3 py-2 text-left text-xs font-medium text-gray-500">Academic Info/Dept</th>

<!-- In the table body -->
<td class="px-3 py-2">
    <div class="text-sm font-medium text-gray-900">
        {% if report.involved_parties.exists %}
            {% for party in report.involved_parties.all %}
                <div class="mb-1 flex items-center gap-2">
                    <span>{{ party.get_display_name }}</span>
                    <span class="text-xs px-2 py-0.5 rounded font-semibold
                        {% if party.party_type == 'student' %}bg-blue-100 text-blue-800
                        {% else %}bg-purple-100 text-purple-800{% endif %}">
                        {{ party.get_party_type_display }}
                    </span>
                    {% if not party.is_confirmed %}
                        <span class="text-xs px-2 py-0.5 bg-yellow-100 text-yellow-800 rounded">
                            <i class="fas fa-clock mr-1"></i>Pending
                        </span>
                    {% endif %}
                    {% if report.is_confidential %}
                        <span class="text-xs px-2 py-0.5 bg-red-100 text-red-800 rounded">
                            <i class="fas fa-lock mr-1"></i>Confidential
                        </span>
                    {% endif %}
                </div>
            {% endfor %}
        {% elif report.reported_student %}
            <!-- Fallback for old reports -->
            <div class="flex items-center gap-2">
                <span>{{ report.reported_student.get_full_name }}</span>
                <span class="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-semibold">
                    Student
                </span>
            </div>
        {% else %}
            <span class="text-gray-400 italic">No parties specified</span>
        {% endif %}
    </div>
</td>

<td class="px-3 py-2">
    <div class="text-xs text-gray-600">
        {% if report.involved_parties.exists %}
            {% for party in report.involved_parties.all %}
                <div class="mb-1">{{ party.get_academic_info }}</div>
            {% endfor %}
        {% elif report.reported_student %}
            <!-- Fallback for old reports -->
            G{{ report.grade_level }} - {{ report.section_name }}
        {% endif %}
    </div>
</td>
```

---

### 7. Add Email Configuration to `sirms_project/settings.py`

**Add at the end of settings.py:**

```python
# Email Configuration for Notifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'SIRMS <noreply@sirms.edu>')

# For development/testing without email server:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

### 8. Update Report Detail View (Optional Enhancement)

**In `templates/report_detail.html`, add involved parties section:**

```html
<!-- Involved Parties Section -->
<div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
    <h3 class="text-lg font-bold text-gray-900 mb-4">
        <i class="fas fa-users text-blue-600 mr-2"></i>
        Involved Parties
    </h3>
    
    {% if report.involved_parties.exists %}
        {% for party in report.involved_parties.all %}
            <div class="mb-4 p-4 border rounded-lg
                {% if party.party_type == 'student' %}border-blue-200 bg-blue-50
                {% else %}border-purple-200 bg-purple-50{% endif %}">
                
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-3">
                        <span class="text-lg font-semibold">{{ party.get_display_name }}</span>
                        <span class="text-xs px-2 py-1 rounded font-semibold
                            {% if party.party_type == 'student' %}bg-blue-200 text-blue-900
                            {% else %}bg-purple-200 text-purple-900{% endif %}">
                            {{ party.get_party_type_display }}
                        </span>
                        {% if party.is_confirmed %}
                            <span class="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">
                                <i class="fas fa-check-circle mr-1"></i>Confirmed
                            </span>
                        {% else %}
                            <span class="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
                                <i class="fas fa-clock mr-1"></i>Pending Confirmation
                            </span>
                        {% endif %}
                    </div>
                </div>
                
                <div class="text-sm text-gray-700">
                    {{ party.get_academic_info }}
                </div>
                
                {% if party.is_confirmed %}
                    <div class="text-xs text-gray-500 mt-2">
                        Confirmed by {{ party.confirmed_by.get_full_name }} on {{ party.confirmed_at|date:"M d, Y" }}
                    </div>
                {% endif %}
            </div>
        {% endfor %}
    {% else %}
        <p class="text-gray-500 italic">No involved parties specified</p>
    {% endif %}
</div>
```

---

## 🧪 TESTING STEPS

### Test 1: Student Case
1. Login as student or teacher
2. Go to Report Incident
3. Select "Student" as party type
4. Fill in student details
5. Submit
6. Check notifications for:
   - All DOs
   - Student (if known)
   - Student's adviser

### Test 2: Teacher Case
1. Login as student or teacher
2. Go to Report Incident
3. Select "Teacher" as party type
4. Fill in teacher name and department
5. Check "Confidential" box
6. Submit
7. Check notifications for:
   - All DOs
   - All Counselors
   - NO notification to teacher yet

### Test 3: Reporter is Victim
1. Login as student
2. Go to Report Incident
3. Check "I am a victim" checkbox
4. Fill in incident details
5. Submit
6. Verify you're added as involved party

---

## ✅ CHECKLIST

- [ ] Add 3 fields to IncidentReport model
- [ ] Add 3 fields to Notification model
- [ ] Run makemigrations
- [ ] Run migrate
- [ ] Update report_incident.html template
- [ ] Update report_incident view in views.py
- [ ] Update all_reports.html display
- [ ] Add email configuration to settings.py
- [ ] Test student case
- [ ] Test teacher case
- [ ] Test reporter is victim
- [ ] Test notifications
- [ ] Test email delivery (if configured)

---

## 🚀 DEPLOYMENT

After testing locally:

```bash
git add .
git commit -m "Implement proper process and notification system with involved parties"
git push origin main
```

Render will automatically deploy.

---

**Everything you need is in this file! Just copy and paste the code sections into the appropriate files.** 🎯

