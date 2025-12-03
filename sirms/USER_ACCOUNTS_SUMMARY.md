# 👥 SIRMS User Accounts - Complete List

## 🎯 Quick Access

**Your Render URL:** https://your-app.onrender.com (replace with your actual URL)

---

## 🔐 Pre-Created Accounts (Ready to Use)

### 1. **Admin Account**
```
Username: admin
Password: admin123
Email: admin@example.com
Role: Administrator
```
**Access:** Full system access, all features

---

### 2. **Discipline Officer (DO) Accounts**

#### Primary DO Account (Recommended)
```
Username: do_admin
Password: do123
Email: do.admin@school.edu
Name: Discipline Officer
```

#### Secondary DO Account
```
Username: do1
Password: do123
Email: do1@example.com
Name: Ana Garcia
```

#### Official DO Account (Email-based)
```
Email: dmlmhs.do@gmail.com
Password: dmlmhsdo000
Name: Discipline Officer
```

**DO Can:**
- View all incident reports
- Fact-check and approve reports
- Create DO schedules
- Manage disciplinary actions
- Access analytics
- Generate reports

---

### 3. **Guidance Counselor Accounts**

#### Primary Counselor
```
Username: counselor1
Password: counselor123
Email: counselor1@example.com
```

#### Official Guidance Account (Email-based)
```
Email: dmlmhs.guidance@gmail.com
Password: dmlmhsguidance000
Name: Guidance Counselor
```

**Counselor Can:**
- Review major cases
- Schedule counseling sessions
- Evaluate cases
- Manage VPF assignments
- View analytics
- Complete sessions

---

### 4. **ESP Teacher Accounts**

All ESP teachers use password: `dmlmhsesp000`

| Name | Email | Password |
|------|-------|----------|
| Maria Santos Garcia | garcia.espteacher@gmail.com | dmlmhsesp000 |
| Juan Dela Cruz Reyes | reyes.espteacher@gmail.com | dmlmhsesp000 |
| Ana Lopez Santos | santos.espteacher@gmail.com | dmlmhsesp000 |
| Pedro Ramos Cruz | cruz.espteacher@gmail.com | dmlmhsesp000 |
| Rosa Mendoza Lopez | lopez.espteacher@gmail.com | dmlmhsesp000 |

**ESP Teachers Can:**
- Manage VPF cases
- Schedule VPF sessions
- Track student progress
- View assigned students

---

### 5. **Teacher Account**

```
Username: teacher1
Password: teacher123
Email: teacher1@example.com
```

**Teachers Can:**
- Report incidents
- View their reports
- See advisee records
- Track student behavior

---

### 6. **Student Account**

```
Username: student1
Password: student123
Email: student1@example.com
```

**Students Can:**
- Report incidents
- View their reports
- See violation history
- Check counseling schedules

---

## 📧 Email-Based Auto Role Assignment

### How It Works:
When users register with specific email formats, they're automatically assigned roles:

### Teacher Email Format:
```
Format: lastname(firstletter)(middleinitial).dmlmhsteacher@gmail.com
Example: santillanjd.dmlmhsteacher@gmail.com
Auto-Role: Teacher
```

### ESP Teacher Email Format:
```
Format: lastname.espteacher@gmail.com
Example: garcia.espteacher@gmail.com
Auto-Role: ESP Teacher
```

### Guidance Email:
```
Email: dmlmhs.guidance@gmail.com
Auto-Role: Counselor
```

### DO Email:
```
Email: dmlmhs.do@gmail.com
Auto-Role: Discipline Officer
```

---

## 🚀 How to Login

### Method 1: Username/Password
1. Go to your Render URL
2. Click "Login"
3. Enter username and password
4. Click "Sign In"

### Method 2: Email/Password
1. Go to your Render URL
2. Click "Login"
3. Enter email and password
4. Click "Sign In"

---

## 🎯 Recommended Test Accounts

### For Testing DO Features:
```
Username: do_admin
Password: do123
```

### For Testing Counselor Features:
```
Email: dmlmhs.guidance@gmail.com
Password: dmlmhsguidance000
```

### For Testing Teacher Features:
```
Username: teacher1
Password: teacher123
```

### For Testing Student Features:
```
Username: student1
Password: student123
```

---

## 📊 Account Summary Table

| Role | Count | Login Method | Dashboard Access |
|------|-------|--------------|------------------|
| Admin | 1 | Username/Email | Full system |
| DO | 3 | Username/Email | DO Dashboard |
| Counselor | 2 | Username/Email | Guidance Dashboard |
| ESP Teacher | 5 | Email only | VPF Dashboard |
| Teacher | 1+ | Username/Email | Teacher Dashboard |
| Student | 1+ | Username/Email | Student Dashboard |

---

## 🔒 Security Notes

### Default Passwords:
⚠️ **Change these after first login in production!**

- Admin: `admin123`
- DO: `do123`
- Counselor: `counselor123`
- ESP Teachers: `dmlmhsesp000`
- Guidance: `dmlmhsguidance000`
- DO Official: `dmlmhsdo000`

### Password Requirements:
- Minimum 8 characters
- Mix of letters and numbers recommended
- Change default passwords immediately

---

## 🆕 Creating New Accounts

### Option 1: Self-Registration
1. Go to your Render URL
2. Click "Register"
3. Fill in details
4. Email determines role (if using official format)
5. Submit

### Option 2: Admin Creation
1. Login as admin
2. Go to Django Admin (`/admin`)
3. Add new user
4. Set role manually

### Option 3: Run Script
```bash
python create_staff_accounts.py
```

---

## 🧪 Testing Checklist

Test each role:

- [ ] **Admin** - Login and access all features
- [ ] **DO** - Login and view incident reports
- [ ] **Counselor** - Login and schedule sessions
- [ ] **ESP Teacher** - Login and manage VPF
- [ ] **Teacher** - Login and report incident
- [ ] **Student** - Login and view reports

---

## 📞 Account Issues?

### Can't Login?
1. Check username/email spelling
2. Verify password (case-sensitive)
3. Try password reset
4. Check account exists in database

### Wrong Dashboard?
1. Check user role in admin panel
2. Verify email format for auto-assignment
3. Logout and login again

### Account Not Found?
1. Run `create_staff_accounts.py`
2. Check database connection
3. Verify deployment completed

---

## 🎉 Quick Start

**To start using SIRMS right now:**

1. **Go to:** Your Render URL
2. **Login as DO:**
   - Username: `do_admin`
   - Password: `do123`
3. **Explore the system!**

---

## 📝 Notes

- All accounts are created automatically on first deployment
- Email-based accounts require exact email format
- Default passwords should be changed in production
- Admin account has access to Django admin panel
- Each role has specific permissions and dashboard

---

**Created:** December 3, 2025  
**Status:** ✅ All accounts ready  
**Total Accounts:** 13+ pre-created accounts

🎯 **Your system is ready with multiple test accounts for all roles!**
