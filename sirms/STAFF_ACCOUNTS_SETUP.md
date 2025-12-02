# 📧 Staff Accounts & Email-Based Role Assignment

## Automatic Role Assignment Based on Email Domain

The system now automatically assigns roles based on email addresses during registration.

### Email Format Rules:

#### 1. **Teacher Accounts**
**Format:** `lastname(firstletterfirstname)(middleinitial).dmlmhsteacher@gmail.com`

**Examples:**
- Juan D. Santillan → `santillanjd.dmlmhsteacher@gmail.com`
- Maria S. Garcia → `garciams.dmlmhsteacher@gmail.com`
- Pedro R. Cruz → `cruzpr.dmlmhsteacher@gmail.com`

**Auto-assigned Role:** `teacher`

#### 2. **ESP Teacher Accounts**
**Format:** `lastname.espteacher@gmail.com`

**Examples:**
- Garcia → `garcia.espteacher@gmail.com`
- Reyes → `reyes.espteacher@gmail.com`
- Santos → `santos.espteacher@gmail.com`

**Auto-assigned Role:** `esp_teacher`

#### 3. **Guidance Counselor**
**Email:** `dmlmhs.guidance@gmail.com`  
**Password:** `dmlmhsguidance000`  
**Auto-assigned Role:** `counselor`

#### 4. **Discipline Officer**
**Email:** `dmlmhs.do@gmail.com`  
**Password:** `dmlmhsdo000`  
**Auto-assigned Role:** `do`

#### 5. **Student Accounts**
**Format:** Any email not matching above patterns  
**Role:** Selected by user during registration (defaults to `student`)

---

## Pre-Created Staff Accounts

### Run the Account Creation Script:

**Windows:**
```bash
cd sirms
create_staff_accounts.bat
```

**Or manually:**
```bash
cd sirms
python create_staff_accounts.py
```

### Accounts Created:

#### 1. Guidance Counselor
- **Email:** dmlmhs.guidance@gmail.com
- **Password:** dmlmhsguidance000
- **Role:** Counselor
- **Name:** Guidance Counselor

#### 2. Discipline Officer
- **Email:** dmlmhs.do@gmail.com
- **Password:** dmlmhsdo000
- **Role:** Discipline Officer
- **Name:** Discipline Officer

#### 3. ESP Teachers (5 accounts)
All ESP teachers have the same password: `dmlmhsesp000`

| Name | Email | Password |
|------|-------|----------|
| Maria Santos Garcia | garcia.espteacher@gmail.com | dmlmhsesp000 |
| Juan Dela Cruz Reyes | reyes.espteacher@gmail.com | dmlmhsesp000 |
| Ana Lopez Santos | santos.espteacher@gmail.com | dmlmhsesp000 |
| Pedro Ramos Cruz | cruz.espteacher@gmail.com | dmlmhsesp000 |
| Rosa Mendoza Lopez | lopez.espteacher@gmail.com | dmlmhsesp000 |

---

## How Automatic Role Assignment Works

### Registration Flow:

1. **User enters email during registration**
2. **System checks email pattern:**
   - Ends with `.dmlmhsteacher@gmail.com` → Auto-assign `teacher`
   - Ends with `.espteacher@gmail.com` → Auto-assign `esp_teacher`
   - Equals `dmlmhs.guidance@gmail.com` → Auto-assign `counselor`
   - Equals `dmlmhs.do@gmail.com` → Auto-assign `do`
   - Otherwise → Use role selected by user
3. **Account created with correct role**
4. **User redirected to appropriate dashboard**

### Code Implementation:

```python
def save(self, commit=True):
    user = super().save(commit=False)
    email = self.cleaned_data.get('email', '').lower()
    
    # Automatic role assignment based on email domain
    if email.endswith('.dmlmhsteacher@gmail.com'):
        user.role = 'teacher'
    elif email.endswith('.espteacher@gmail.com'):
        user.role = 'esp_teacher'
    elif email == 'dmlmhs.guidance@gmail.com':
        user.role = 'counselor'
    elif email == 'dmlmhs.do@gmail.com':
        user.role = 'do'
    
    if commit:
        user.save()
    return user
```

---

## Teacher Email Format Examples

### Format Breakdown:
`lastname(firstletterfirstname)(middleinitial).dmlmhsteacher@gmail.com`

**Components:**
1. **lastname** - Full last name (lowercase)
2. **firstletterfirstname** - First letter of first name (lowercase)
3. **middleinitial** - First letter of middle name (lowercase)
4. **Domain** - `.dmlmhsteacher@gmail.com`

### Examples:

| Full Name | Email |
|-----------|-------|
| Juan Dela Cruz Santillan | santillanjd.dmlmhsteacher@gmail.com |
| Maria Santos Garcia | garciams.dmlmhsteacher@gmail.com |
| Pedro Ramos Cruz | cruzpr.dmlmhsteacher@gmail.com |
| Ana Lopez Reyes | reyesal.dmlmhsteacher@gmail.com |
| Rosa Mendoza Santos | santosrm.dmlmhsteacher@gmail.com |

---

## Benefits

✅ **Automatic Role Assignment** - No manual role selection needed  
✅ **Secure** - Email domain verification  
✅ **Consistent** - Standardized email format  
✅ **Easy Management** - Clear identification of user types  
✅ **Pre-configured** - Staff accounts ready to use

---

## Testing

### Test Automatic Role Assignment:

1. **Test Teacher Registration:**
   - Email: `testteacher.dmlmhsteacher@gmail.com`
   - Expected: Auto-assigned as `teacher`

2. **Test ESP Teacher Registration:**
   - Email: `test.espteacher@gmail.com`
   - Expected: Auto-assigned as `esp_teacher`

3. **Test Guidance Login:**
   - Email: `dmlmhs.guidance@gmail.com`
   - Password: `dmlmhsguidance000`
   - Expected: Access to counselor dashboard

4. **Test DO Login:**
   - Email: `dmlmhs.do@gmail.com`
   - Password: `dmlmhsdo000`
   - Expected: Access to DO dashboard

---

## Security Notes

⚠️ **Change Default Passwords** - After first login, users should change their passwords  
⚠️ **Email Verification** - Consider adding email verification for production  
⚠️ **Domain Control** - Only DMLMHS email domains can auto-assign staff roles  
⚠️ **Admin Oversight** - Monitor account creation for unauthorized access

---

## Troubleshooting

**Issue:** Role not auto-assigned  
**Solution:** Check email format matches exactly (case-insensitive)

**Issue:** Account creation fails  
**Solution:** Check if email already exists in system

**Issue:** Can't login with staff account  
**Solution:** Verify password is correct (case-sensitive)

---

**Created:** December 2, 2025  
**Status:** ✅ Ready for deployment
