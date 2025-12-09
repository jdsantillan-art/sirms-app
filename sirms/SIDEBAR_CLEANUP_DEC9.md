# Sidebar Cleanup - December 9, 2025

## Changes Made

### 1. ESP Teacher Sidebar
**Removed:**
- ❌ Dashboard link

**Remaining:**
- ✅ VPF Schedule
- ✅ VPF Cases

### 2. Teacher Sidebar
**Removed:**
- ❌ Advisee Records
- ❌ Legal References (Incident Reference)

**Remaining:**
- ✅ Report Incident
- ✅ My Reports
- ✅ Counseling Schedule

### 3. Student Sidebar
**Removed:**
- ❌ Legal References

**Remaining:**
- ✅ Dashboard
- ✅ Report Incident
- ✅ My Reports
- ✅ Counseling Schedule

## Technical Details

### File Modified
- `templates/base.html`

### Changes Applied

#### ESP Teacher - Removed Dashboard
```html
<!-- Before: Dashboard shown for all roles -->
<a href="{% url 'dashboard' %}" class="nav-item">
    <i class="fas fa-tachometer-alt"></i>
    <span class="sidebar-text">Dashboard</span>
</a>

<!-- After: Dashboard hidden for ESP Teacher -->
{% if user.role != 'esp_teacher' %}
<a href="{% url 'dashboard' %}" class="nav-item">
    <i class="fas fa-tachometer-alt"></i>
    <span class="sidebar-text">Dashboard</span>
</a>
{% endif %}
```

#### Teacher - Removed Advisee Records
```html
<!-- Removed this entire block -->
<a href="{% url 'advisee_records' %}" class="nav-item">
    <i class="fas fa-users"></i>
    <span class="sidebar-text">Advisee Records</span>
</a>
```

#### Teacher - Removed Legal References
```html
<!-- Removed this entire block -->
<a href="{% url 'legal_references' %}" class="nav-item">
    <i class="fas fa-book"></i>
    <span class="sidebar-text">Incident Reference</span>
</a>
```

#### Student - Removed Legal References
```html
<!-- Removed this entire block -->
<a href="{% url 'legal_references' %}" class="nav-item">
    <i class="fas fa-balance-scale"></i>
    <span class="sidebar-text">Legal References</span>
</a>
```

## Deployment

### To Deploy:

**Option 1: Use batch file**
```bash
cd sirms
deploy_sidebar_cleanup.bat
```

**Option 2: Manual commands**
```bash
cd sirms
git add templates/base.html
git commit -m "Remove sidebar items: Dashboard from ESP Teacher, Advisee Records and Legal References from Teacher, Legal References from Student"
git push origin main
```

### After Deployment

1. Wait 5-10 minutes for Render to auto-deploy
2. Check deployment status: https://dashboard.render.com
3. Test each role:
   - Login as ESP Teacher → Dashboard should NOT appear
   - Login as Teacher → Advisee Records and Legal References should NOT appear
   - Login as Student → Legal References should NOT appear

## Impact

### ESP Teacher
- Cleaner sidebar with only relevant VPF functions
- No dashboard clutter

### Teacher
- Simplified sidebar focused on core functions
- Removed unused Advisee Records feature
- Removed Legal References (can still access via other means if needed)

### Student
- Cleaner interface
- Removed Legal References (not typically needed by students)

## Rollback

If you need to restore these items, revert the commit:

```bash
cd sirms
git revert HEAD
git push origin main
```

## Summary

| Role | Removed Items | Reason |
|------|--------------|--------|
| ESP Teacher | Dashboard | Not needed for VPF-focused role |
| Teacher | Advisee Records | Feature not actively used |
| Teacher | Legal References | Simplify sidebar |
| Student | Legal References | Not typically needed by students |

---

**Status**: ✅ Ready to deploy
**Files Changed**: 1 (templates/base.html)
**Risk**: LOW (only UI changes, no functionality removed)
**Testing**: Test login for each role after deployment
