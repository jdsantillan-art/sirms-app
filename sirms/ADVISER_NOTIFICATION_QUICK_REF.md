# Adviser Notification - Quick Reference Card

## 🎯 What It Does
Automatically notifies teachers/advisers when counseling sessions are scheduled for their students.

## 📋 Who Gets Notified
**Teachers/Advisers** of students when:
- Guidance Counselor schedules counseling
- ESP Teacher schedules VPF session
- Discipline Officer schedules parent conference/interview

## 🔍 How Teachers Are Found
System searches using:
1. Teacher name from incident report
2. Section adviser assignment
3. Teacher assignment records (curriculum + grade + section)

## 📨 Notification Format

### Title
`[Type] Session Scheduled for Your Student`

### Content
- Student name
- Case ID
- Date and time
- Location
- Who scheduled it

### Example
```
Title: Counseling Session Scheduled for Your Student

Message: A counseling session has been scheduled for your 
student Juan Dela Cruz (Case: 2024-0015) on December 15, 
2024 at 2:00 PM. Location: Guidance Office. 
Counselor: Dr. Carmen Reyes.
```

## ✅ Quick Test

### As Counselor/DO/ESP Teacher:
1. Create a schedule for a student
2. Note the student's grade and section

### As Teacher:
1. Login to your account
2. Check notifications (bell icon)
3. Should see notification if you're the adviser

## 🔧 Troubleshooting

### Teacher Not Notified?

**Check 1:** Is teacher name in the report?
```python
# Django shell
report = IncidentReport.objects.get(case_id='2024-XXXX')
print(report.teacher_name)
```

**Check 2:** Does teacher account exist?
```python
CustomUser.objects.filter(role='teacher', 
                         first_name__icontains='Maria')
```

**Check 3:** Is section adviser assigned?
```python
Section.objects.filter(grade__level='10', name='A')
```

## 📊 Verify It's Working

### Run Test Script
```bash
cd sirms
python manage.py shell < test_adviser_notifications.py
```

### Check Recent Notifications
```python
from incidents.models import Notification
from django.utils import timezone

recent = timezone.now() - timezone.timedelta(hours=24)
notifs = Notification.objects.filter(
    user__role='teacher',
    created_at__gte=recent
)
print(f"Recent teacher notifications: {notifs.count()}")
```

## 📁 Documentation Files

- `ADVISER_NOTIFICATION_FEATURE.md` - Complete documentation
- `ADVISER_NOTIFICATION_EXAMPLE.md` - Real-world examples
- `TESTING_ADVISER_NOTIFICATIONS.md` - Testing guide
- `ADVISER_NOTIFICATION_SUMMARY.md` - Implementation summary
- `test_adviser_notifications.py` - Test script

## 🚀 Key Benefits

✅ Automatic - no manual work
✅ Comprehensive - all three roles
✅ Smart - multiple search methods
✅ Informative - complete details
✅ Reliable - graceful error handling

## 💡 Pro Tips

1. **Keep teacher names consistent** in reports and accounts
2. **Assign section advisers** for better matching
3. **Update TeacherAssignment** records regularly
4. **Monitor notifications** in first week
5. **Train teachers** to check notifications

## 🎓 Training Points

### For Counselors/DO/ESP Teachers:
- No change to your workflow
- Notifications sent automatically
- Teachers will be informed

### For Teachers:
- Check notifications regularly
- You'll be notified of student sessions
- Can prepare/follow up with students
- Better support for your students

## 📞 Support

Issues? Check:
1. `TESTING_ADVISER_NOTIFICATIONS.md` for troubleshooting
2. Run `test_adviser_notifications.py` to verify
3. Check admin panel for notification logs
4. Verify teacher and report data accuracy

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: ✅ Active and Working
