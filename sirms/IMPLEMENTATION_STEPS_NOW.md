# 🚀 Implementation Steps - DO THIS NOW

## ✅ Complete Implementation in 30 Minutes

Follow these steps exactly to implement the proper process and notification system.

---

## STEP 1: Add Model Fields (10 minutes)

### A. Add to IncidentReport Model

1. Open `sirms/incidents/models.py`
2. Search for `class IncidentReport`
3. Scroll to the end of the field definitions (before `class Meta:` or `def __str__`)
4. Add these 3 fields:

```python
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
```

### B. Add to Notification Model

1. In the same file, search for `class Notification`
2. Add these fields at the end (before `class Meta:` or `def __str__`):

```python
    # Notification Type Tracking
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

3. Save the file

---

## STEP 2: Run Migrations (2 minutes)

Open a NEW terminal (not the one with stuck migration) and run:

```bash
cd sirms
python manage.py makemigrations
python manage.py migrate
```

If you get errors, check that:
- Fields are added correctly
- No syntax errors
- InvolvedParty model exists (it should - we added it earlier)

---

## STEP 3: Update Report Form Template (5 minutes)

1. Open `sirms/templates/report_incident.html`
2. Find the section after reporter information
3. Add this code BEFORE the incident details section:

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
</div>

<!-- Party Type Selection -->
<div class="mb-4">
    <label class="block text-sm font-bold text-gray-800 mb-2">
        Involved Party Type <span class="text-red-500">*</span>
    </label>
    <select name="party_type" id="partyType" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required>
        <option value="">-- Select Type --</option>
        <option value="student">👨‍🎓 Student</option>
        <option value="teacher">👨‍🏫 Teacher/Staff</option>
    </select>
</div>

<!-- Teacher Fields -->
<div id="teacherFields" style="display:none;">
    <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
        <div class="mb-4">
            <label class="block text-sm font-bold text-gray-800 mb-2">
                Teacher Name <span class="text-red-500">*</span>
            </label>
            <input type="text" name="teacher_name" id="teacherName" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
        </div>
        
        <div class="mb-4">
            <label class="block text-sm font-bold text-gray-800 mb-2">Department/Subject</label>
            <input type="text" name="department" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
        </div>
        
        <label class="flex items-center">
            <input type="checkbox" name="is_confidential" checked class="mr-3 h-5 w-5">
            <span class="text-sm font-semibold">🔒 Mark as confidential</span>
        </label>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const partyType = document.getElementById('partyType');
    const studentFields = document.getElementById('studentFields'); // Your existing student section
    const teacherFields = document.getElementById('teacherFields');
    
    partyType.addEventListener('change', function() {
        if (this.value === 'student') {
            if(studentFields) studentFields.style.display = 'block';
            teacherFields.style.display = 'none';
        } else if (this.value === 'teacher') {
            if(studentFields) studentFields.style.display = 'none';
            teacherFields.style.display = 'block';
        }
    });
});
</script>
```

4. Find your existing student fields section and add `id="studentFields"` to the container div
5. Save the file

---

## STEP 4: Update Report View (10 minutes)

1. Open `sirms/incidents/views.py`
2. At the top, add this import:

```python
from .notification_utils import send_smart_notifications
from .models import InvolvedParty
```

3. Find the `report_incident` function
4. In the `if request.method == 'POST':` section, AFTER creating the report, add:

```python
        # Get new fields
        reporter_is_victim = request.POST.get('reporter_is_victim') == 'on'
        is_confidential = request.POST.get('is_confidential') == 'on'
        party_type = request.POST.get('party_type')
        
        # Update report with new fields
        report.reporter_is_victim = reporter_is_victim
        report.is_confidential = is_confidential
        report.save()
        
        # Create involved party
        if party_type == 'student' and reported_student:
            involved_party = InvolvedParty.objects.create(
                party_type='student',
                student=reported_student,
                curriculum=curriculum if 'curriculum' in locals() else None,
                grade_level=grade_level if 'grade_level' in locals() else None,
            )
            report.involved_parties.add(involved_party)
            
        elif party_type == 'teacher':
            teacher_name = request.POST.get('teacher_name')
            department = request.POST.get('department', '')
            
            involved_party = InvolvedParty.objects.create(
                party_type='teacher',
                name_if_unknown=teacher_name,
                department=department,
            )
            report.involved_parties.add(involved_party)
        
        # If reporter is victim, add them
        if reporter_is_victim and request.user.role == 'student':
            victim_party = InvolvedParty.objects.create(
                party_type='student',
                student=request.user,
                is_confirmed=True,
                confirmed_by=request.user,
                confirmed_at=timezone.now(),
            )
            report.involved_parties.add(victim_party)
        
        # Send smart notifications
        try:
            send_smart_notifications(report, 'report_submitted')
        except Exception as e:
            print(f"Notification error: {e}")
```

5. Save the file

---

## STEP 5: Test (3 minutes)

### Test 1: Student Case
1. Run server: `python manage.py runserver`
2. Login as student or teacher
3. Go to Report Incident
4. Select "Student" as party type
5. Fill in details
6. Submit
7. Check: Report created, notifications sent

### Test 2: Teacher Case
1. Go to Report Incident
2. Select "Teacher" as party type
3. Fill in teacher name
4. Check "Confidential"
5. Submit
6. Check: Report created, marked confidential

### Test 3: Reporter is Victim
1. Login as student
2. Go to Report Incident
3. Check "I am a victim" checkbox
4. Fill in details
5. Submit
6. Check: You're added as involved party

---

## ✅ VERIFICATION CHECKLIST

After implementation, verify:

- [ ] Models have 6 new fields
- [ ] Migrations ran successfully
- [ ] Report form shows party type selection
- [ ] Teacher fields appear when teacher selected
- [ ] Reporter is victim checkbox works
- [ ] Reports are created successfully
- [ ] Involved parties are saved
- [ ] Notifications are sent
- [ ] No errors in console

---

## 🆘 TROUBLESHOOTING

### Migration Errors:
- Check field syntax in models.py
- Ensure InvolvedParty model exists
- Try: `python manage.py makemigrations --empty incidents`

### Form Not Showing:
- Check template syntax
- Verify JavaScript is included
- Check browser console for errors

### View Errors:
- Check imports are correct
- Verify notification_utils.py exists
- Check for typos in field names

### Notifications Not Sending:
- Check notification_utils.py exists
- Verify CustomUser model has role field
- Check console for error messages

---

## 📝 AFTER IMPLEMENTATION

Once everything works:

1. Test thoroughly with different scenarios
2. Check all notifications are sent correctly
3. Verify confidential reports work
4. Test with both students and teachers
5. Deploy to production

---

## 🚀 DEPLOYMENT

When ready to deploy:

```bash
git add .
git commit -m "Implement proper process and notification system"
git push origin main
```

Render will auto-deploy. Then run migrations on Render.

---

**Follow these steps exactly and you'll have the system working in 30 minutes!** ✅

