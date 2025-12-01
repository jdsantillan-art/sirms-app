# 🧪 Testing the Violation System

## ✅ Quick Test Guide

### **Step 1: Check Server is Running**
Your server should be running at: **http://127.0.0.1:8000**

### **Step 2: Login**
- Username: `admin`
- Password: `admin123`

### **Step 3: Go to Report Incident**
Click on "Report Incident" in the menu

### **Step 4: Test the Dropdown**

You should see **47 violations** grouped into two categories:

#### **🚫 Prohibited Acts (39 violations):**
- Possession of deadly weapons
- Use/peddling/pushing of marijuana or prohibited drugs
- Assaulting teacher/school personnel
- Theft/shoplifting/stealing
- Forging/tampering of school records
- Gross indecency in conduct
- Fraternity/sorority/gang membership
- Extortion/swindling
- **Bullying or peer abuse** ⭐
- Inflicting injury upon another student/physical assault
- Vandalism/destruction of school property
- Destruction of nature
- Littering/non-observance of waste management
- Cheating on classwork
- Intentional spitting on walls and railings
- Smoking & vaping
- Taking/bringing intoxicating drinks
- Any form of gambling
- Insinuating trouble or fight
- Unsafe behavior on school premises
- Making unnecessary noise
- Making derogatory statements
- Climbing over perimeter fence
- Truancy/habitual absenteeism/tardiness
- Unauthorized use of personal gadgets
- Possession of pornographic materials
- Bringing/igniting firecrackers
- School I.D. violation
- Hurling stones/materials over fence
- Prohibited games/activities

#### **📋 Other School Policies (8 violations):**
- Improper haircut (male students)
- Excessive makeup/colored nail polish
- Bright colored/unnatural hair dyes
- Wearing tattoos/unauthorized piercings
- Wearing caps inside classroom
- LGBTQA+ Non-compliance with uniform/hairstyle

---

### **Step 5: Test Bullying Dropdown**

1. Select **"Bullying or peer abuse"** from the dropdown
2. A new dropdown should appear below with:
   - Physical Bullying
   - Psychological Bullying
   - Sexual Bullying
   - Emotional Bullying
   - Cyber Bullying
   - Social Bullying
   - Gender-based Bullying

3. Legal references should also appear in a blue sidebar showing:
   - RA 10627
   - DO 55, s.2013
   - DepEd Order (DO) 40, s.2012

---

### **Step 6: Test Legal References**

Select any violation and check if legal references appear in the sidebar.

Examples:
- **Possession of deadly weapons** → Shows: "DepEd Order (DO) 40, s.2012"
- **Smoking & vaping** → Shows: "RA 9211; EO 26 (2017); RA 11900"
- **Theft/shoplifting/stealing** → Shows: "RPC Art. 308-310"

---

## ❌ Troubleshooting

### **Problem: Dropdown is empty**

**Solution 1: Reload the violations**
```bash
python load_violations.py
```

**Solution 2: Check if violations exist**
```bash
python check_violations.py
```

**Solution 3: Restart the server**
1. Stop the server (Ctrl+C)
2. Start again: `python manage.py runserver`
3. Refresh your browser (Ctrl+F5)

### **Problem: Bullying dropdown doesn't appear**

**Solution: Clear browser cache**
1. Press Ctrl+Shift+Delete
2. Clear cache
3. Refresh page (Ctrl+F5)

Or try in incognito/private mode

### **Problem: Legal references don't show**

**Solution: Check JavaScript console**
1. Press F12
2. Go to Console tab
3. Look for errors
4. Refresh page

---

## ✅ Expected Behavior

### **When you select a Prohibited Act:**
- ✅ Legal references appear in sidebar
- ✅ If "Bullying", dropdown appears
- ✅ Form can be submitted
- ✅ Saves with "Prohibited" classification

### **When you select a School Policy:**
- ✅ Legal references appear in sidebar
- ✅ Form can be submitted
- ✅ Saves with "School Policy" classification

### **When you select Bullying:**
- ✅ Legal references appear
- ✅ Bullying type dropdown appears
- ✅ Bullying type is required
- ✅ Saves with both classification and bullying type

---

## 📊 Verify Data Saved Correctly

After submitting a report:

1. Go to "My Reports"
2. Click on the report you just created
3. Check:
   - ✅ Violation type is shown
   - ✅ Classification is correct (Prohibited/School Policy)
   - ✅ If bullying, bullying type is shown
   - ✅ Legal references are displayed

---

## 🎯 Quick Commands

**Check violations count:**
```bash
python check_violations.py
```

**Reload violations:**
```bash
python load_violations.py
```

**Start server:**
```bash
python manage.py runserver
```

**Access app:**
```
http://127.0.0.1:8000
```

---

**If everything works, you're ready to deploy to Render!** 🚀
