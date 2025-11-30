# Admin Account Credentials

## 🔐 Login Details

**Username:** `admin`  
**Password:** `admin123`  
**Email:** admin@school.edu  
**Role:** Guidance Counselor (Full Access)

---

## 🌐 Access URLs

### Main SIRMS System
- **Login Page:** http://127.0.0.1:8000/login/
- **Dashboard:** http://127.0.0.1:8000/dashboard/

### Django Admin Panel
- **Admin Panel:** http://127.0.0.1:8000/admin/
- Full database access and management

---

## ✅ What You Can Access

As admin with Counselor role, you have access to:

### System Maintenance
- ✓ Manage Curriculum
- ✓ Manage Teachers
- ✓ Manage Incident Types
- ✓ Manage Counselors
- ✓ Manage Legal References

### Case Management
- ✓ Major Case Review
- ✓ Case Evaluation
- ✓ Case History
- ✓ Counseling Management

### Reports & Analytics
- ✓ Reports & Analytics
- ✓ Export functionality
- ✓ Dashboard analytics

### Django Admin
- ✓ Full database access
- ✓ User management
- ✓ All models CRUD operations

---

## 🔒 Security Notes

1. **Change Password After First Login**
   - Current password is temporary
   - Use a strong password for production

2. **Superuser Privileges**
   - This account has full system access
   - Can modify any data in the database
   - Use responsibly

3. **Recommended Password Requirements**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Not based on dictionary words

---

## 📝 How to Change Password

### Method 1: Django Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Login with admin/admin123
3. Click "Users" → "admin"
4. Scroll to password section
5. Click "this form" to change password

### Method 2: Command Line
```bash
python manage.py changepassword admin
```

### Method 3: Python Script
```python
from incidents.models import CustomUser
admin = CustomUser.objects.get(username='admin')
admin.set_password('your_new_password')
admin.save()
```

---

## 🎯 Quick Start

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Login:**
   - Go to http://127.0.0.1:8000/login/
   - Username: admin
   - Password: admin123

3. **Access features:**
   - Check sidebar for all available options
   - System Maintenance section has all admin tools

---

## 👥 Other Test Accounts

If you need other role accounts for testing:

**Discipline Officer:**
- Username: test_do
- Password: password123

**Counselor:**
- Username: test_counselor
- Password: password123

---

## ⚠️ Important

- Keep these credentials secure
- Don't share admin access
- Change default passwords in production
- Regular security audits recommended

---

**Created:** November 18, 2025  
**Last Updated:** November 18, 2025
