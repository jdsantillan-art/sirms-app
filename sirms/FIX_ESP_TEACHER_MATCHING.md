# Fix: ESP Teacher VPF Cases Not Showing

## 🔧 Issue

ESP teachers receive notifications when assigned to VPF cases, but the cases don't appear in their "VPF Cases" or "VPF Schedule" pages.

## 🎯 Root Cause

The system matches ESP teacher **user accounts** to **Counselor records** by name, which can fail if:
1. Names don't match exactly
2. Name format is different (e.g., "Maria Santos" vs "Santos, Maria")
3. Middle names are included/excluded
4. Spelling differences

## ✅ Solution Applied

### 1. Improved Matching Logic

**Before:**
```python
# Only matched by name
matching_counselors = Counselor.objects.filter(name__icontains=esp_teacher_name)
```

**After:**
```python
# Match by email first (most reliable), then by name
matching_counselors = Counselor.objects.filter(
    Q(email__iexact=esp_teacher_email) |  # Match by email
    Q(name__icontains=esp_teacher_name)    # Or match by name
).filter(is_active=True)
```

### 2. Files Updated

- ✅ `incidents/views.py` - `vpf_cases()` function
- ✅ `incidents/views.py` - `vpf_schedule()` function

---

## 🔍 How to Diagnose

### Run Debug Script:
```bash
python debug_esp_teacher_matching.py
```

This will show:
- All ESP teacher user accounts
- All Counselor records
- Which ones match
- Which VPF cases are assigned
- Suggestions for fixing mismatches

---

## 📋 How to Fix Matching Issues

### Option 1: Match by Email (Recommended)

Ensure the ESP teacher's **user email** matches the **Counselor email**:

**User Account:**
```
Email: santosespteacher@gmail.com
```

**Counselor Record (Manage ESP Teachers):**
```
Email: santosespteacher@gmail.com  ← Must match!
```

### Option 2: Match by Name

Ensure the ESP teacher's **full name** matches the **Counselor name**:

**User Account:**
```
First Name: Maria
Last Name: Santos
Full Name: "Maria Santos"
```

**Counselor Record:**
```
Name: "Maria Santos"  ← Must match!
```

---

## 🛠️ Step-by-Step Fix

### Step 1: Identify the Mismatch

Run the debug script:
```bash
python debug_esp_teacher_matching.py
```

Look for:
```
User: maria.santos
- Full Name: Maria Santos
- Email: maria@example.com
❌ NO MATCH FOUND
```

### Step 2: Fix the Mismatch

**Option A: Update Counselor Email**
1. Go to "Manage ESP Teachers"
2. Edit the ESP teacher
3. Change email to match user's email
4. Save

**Option B: Update User Email**
1. Go to Django admin
2. Find the user account
3. Change email to match Counselor's email
4. Save

**Option C: Update Counselor Name**
1. Go to "Manage ESP Teachers"
2. Edit the ESP teacher
3. Change name to match user's full name exactly
4. Save

### Step 3: Verify the Fix

Run the debug script again:
```bash
python debug_esp_teacher_matching.py
```

Look for:
```
User: maria.santos
- Full Name: Maria Santos
- Email: santosespteacher@gmail.com
✅ MATCHED to Counselor(s):
   - Maria Santos (santosespteacher@gmail.com)
   - VPF Cases: 2
```

### Step 4: Test in Browser

1. Login as ESP teacher
2. Go to "VPF Cases"
3. Should see assigned cases
4. Go to "VPF Schedule"
5. Should be able to schedule sessions

---

## 📊 Common Scenarios

### Scenario 1: Email Mismatch

**Problem:**
```
User Email: maria.santos@school.com
Counselor Email: santosespteacher@gmail.com
Result: ❌ No match
```

**Solution:**
Update Counselor email to `maria.santos@school.com`

### Scenario 2: Name Format Mismatch

**Problem:**
```
User Name: "Maria Santos"
Counselor Name: "Santos, Maria"
Result: ❌ No match (name doesn't contain "Maria Santos")
```

**Solution:**
Update Counselor name to "Maria Santos"

### Scenario 3: Middle Name Issue

**Problem:**
```
User Name: "Maria Elena Santos"
Counselor Name: "Maria Santos"
Result: ✅ Match (contains "Maria Santos")
```

**Solution:**
No fix needed - this works!

### Scenario 4: Perfect Match

**Problem:**
```
User Email: santosespteacher@gmail.com
User Name: "Maria Santos"
Counselor Email: santosespteacher@gmail.com
Counselor Name: "Maria Santos"
Result: ✅ Match
```

**Solution:**
No fix needed - working correctly!

---

## 🎯 Best Practices

### 1. Use Email Matching (Most Reliable)

Always ensure emails match:
```
User: santosespteacher@gmail.com
Counselor: santosespteacher@gmail.com
```

### 2. Use Consistent Name Format

Use "First Last" format:
```
✅ Good: "Maria Santos"
❌ Bad: "Santos, Maria"
❌ Bad: "MARIA SANTOS"
❌ Bad: "maria santos"
```

### 3. Create User Accounts for All ESP Teachers

For each Counselor record, create a matching user account:
```python
# In Django shell or admin
user = CustomUser.objects.create_user(
    username='maria.santos',
    email='santosespteacher@gmail.com',  # Match Counselor email!
    first_name='Maria',
    last_name='Santos',
    role='esp_teacher'
)
user.set_password('password123')
user.save()
```

### 4. Test After Creating

Always test:
1. Run debug script
2. Login as ESP teacher
3. Check "VPF Cases" page
4. Verify cases appear

---

## 🚀 Deployment

### Files Changed:
- ✅ `incidents/views.py` - Improved matching logic
- ✅ `debug_esp_teacher_matching.py` - Debug tool

### To Deploy:
```bash
git add incidents/views.py debug_esp_teacher_matching.py FIX_ESP_TEACHER_MATCHING.md
git commit -m "Fix: Improve ESP teacher matching by email and name"
git push origin main
```

---

## ✅ Verification

After deployment, verify:
- [ ] ESP teachers can see assigned cases in "VPF Cases"
- [ ] ESP teachers can schedule sessions in "VPF Schedule"
- [ ] Cases appear immediately after assignment
- [ ] Statistics show correct counts

---

## 📝 Summary

**Problem:** ESP teachers couldn't see assigned VPF cases  
**Cause:** Name-only matching was unreliable  
**Solution:** Added email matching (more reliable)  
**Result:** ESP teachers now see cases if email OR name matches  

**Matching Priority:**
1. ✅ Email match (most reliable)
2. ✅ Name match (fallback)
3. ✅ Must be active Counselor

---

**Fix Applied:** December 4, 2025  
**Status:** ✅ READY TO DEPLOY  
**Impact:** ESP teachers will see assigned cases  
