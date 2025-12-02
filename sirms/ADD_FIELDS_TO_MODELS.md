# 📝 Add 6 Fields to Models - Exact Instructions

## ⚠️ IMPORTANT: Manual Edit Required

The models.py file is too large to automatically edit. You need to manually add these fields.

---

## STEP 1: Add 3 Fields to IncidentReport Model

### Instructions:
1. Open `sirms/incidents/models.py`
2. Search for: `class IncidentReport`
3. Scroll down to find the last field in the model (before `class Meta:` or `def __str__`)
4. Add these 3 fields:

```python
    # Proper Process System Fields (ADD THESE)
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

### Example of where to add:
```python
class IncidentReport(models.Model):
    # ... existing fields ...
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ADD THE 3 NEW FIELDS HERE:
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
    
    class Meta:
        # ... existing meta ...
```

---

## STEP 2: Add 3 Fields to Notification Model

### Instructions:
1. In the same file (`sirms/incidents/models.py`)
2. Search for: `class Notification`
3. Scroll down to find the last field in the model
4. Add these 3 fields:

```python
    # Notification Tracking Fields (ADD THESE)
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

### Example of where to add:
```python
class Notification(models.Model):
    # ... existing fields ...
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ADD THE 3 NEW FIELDS HERE:
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
    
    class Meta:
        # ... existing meta ...
```

---

## STEP 3: Save and Run Migrations

After adding all 6 fields:

1. Save `models.py`
2. Open a NEW terminal
3. Run:

```bash
cd sirms
python manage.py makemigrations
python manage.py migrate
```

---

## ✅ VERIFICATION

After running migrations, verify:

```bash
python manage.py shell
```

Then in the shell:
```python
from incidents.models import IncidentReport, Notification

# Check IncidentReport fields
print(hasattr(IncidentReport, 'reporter_is_victim'))  # Should print: True
print(hasattr(IncidentReport, 'is_confidential'))     # Should print: True
print(hasattr(IncidentReport, 'involved_parties'))    # Should print: True

# Check Notification fields
print(hasattr(Notification, 'notification_type'))     # Should print: True
print(hasattr(Notification, 'email_sent'))            # Should print: True
print(hasattr(Notification, 'email_sent_at'))         # Should print: True
```

If all print `True`, fields are added successfully!

---

## 🆘 TROUBLESHOOTING

### Can't find IncidentReport or Notification class?
- Search for `class IncidentReport(models.Model):`
- Search for `class Notification(models.Model):`
- They should be in `sirms/incidents/models.py`

### Migration errors?
- Check for syntax errors (missing commas, parentheses)
- Ensure InvolvedParty model exists (it should - we added it)
- Try: `python manage.py makemigrations --dry-run` to see what will happen

### Fields already exist error?
- Check if fields are already in the model
- If yes, just run migrations
- If no, add them as shown above

---

## 📋 QUICK CHECKLIST

- [ ] Opened `sirms/incidents/models.py`
- [ ] Found `class IncidentReport`
- [ ] Added 3 fields to IncidentReport
- [ ] Found `class Notification`
- [ ] Added 3 fields to Notification
- [ ] Saved the file
- [ ] Ran `python manage.py makemigrations`
- [ ] Ran `python manage.py migrate`
- [ ] Verified fields exist (optional)

---

## 🚀 NEXT STEPS

After successfully adding fields and running migrations:

1. Update report form template (see `IMPLEMENTATION_STEPS_NOW.md` Step 3)
2. Update report view (see `IMPLEMENTATION_STEPS_NOW.md` Step 4)
3. Test the system (see `IMPLEMENTATION_STEPS_NOW.md` Step 5)

---

**Copy the code blocks above and paste them into your models.py file at the indicated locations!**

