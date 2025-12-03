# Deploy ESP Teacher Feature to Render - December 4, 2025

## 🚀 Deployment Steps

### Pre-Deployment Checklist
- ✅ ESP Teacher system implemented
- ✅ 5 ESP teachers populated locally
- ✅ All templates created
- ✅ Views and URLs configured
- ✅ Forms validated
- ✅ Documentation complete

---

## Step 1: Commit Changes to Git

```bash
# Add all ESP Teacher files
git add .

# Commit with descriptive message
git commit -m "Add ESP Teacher Management System - Full Implementation

- Add Manage ESP Teachers page (add/edit/deactivate)
- Add For VPF page with assignment functionality
- Add ESP teacher dropdown with full info display
- Add 5 ESP teachers with proper format
- Email format: lastnameespteacher@gmail.com
- Phone format: 09XX XXX XXXX
- Complete documentation (6 guides)
- Tested and verified"

# Push to GitHub
git push origin main
```

---

## Step 2: Render Will Auto-Deploy

Render will automatically detect the push and start deployment.

**What Render Will Do:**
1. Pull latest code from GitHub
2. Run `build.sh` script
3. Install dependencies from `requirements.txt`
4. Collect static files
5. Run migrations
6. Start the application

---

## Step 3: Run Migrations on Render

After deployment completes, the migrations should run automatically via `build.sh`.

**Verify migrations include:**
- Counselor model (already exists)
- VPFCase model with esp_teacher_assigned field (already exists)

---

## Step 4: Populate ESP Teachers on Render

**Option A: Via Render Shell**
```bash
# In Render Dashboard → Shell
python populate_esp_teachers.py
```

**Option B: Via Django Admin**
1. Go to: https://your-app.onrender.com/admin
2. Login as superuser
3. Go to Counselors section
4. Add 5 ESP teachers manually

**Option C: Via Management Command (Recommended)**
Create a management command to populate on first run.

---

## Step 5: Verify Deployment

### Check These URLs:
1. **Manage ESP Teachers:** `/manage-esp-teachers/`
2. **For VPF:** `/for-vpf/`
3. **Add ESP Teacher:** `/esp-teacher/add/`

### Test These Features:
- ✅ Add ESP teacher
- ✅ Edit ESP teacher
- ✅ View For VPF page
- ✅ Assign teacher to VPF case
- ✅ View assigned cases

---

## Deployment Commands

### Quick Deploy (All-in-One)
```bash
git add .
git commit -m "Deploy ESP Teacher System - Dec 4, 2025"
git push origin main
```

### Manual Deploy Steps
```bash
# 1. Stage changes
git add sirms/incidents/esp_teacher_views.py
git add sirms/templates/counselor/manage_esp_teachers.html
git add sirms/templates/counselor/esp_teacher_form.html
git add sirms/templates/counselor/for_vpf.html
git add sirms/templates/counselor/assign_esp_teacher.html
git add sirms/populate_esp_teachers.py
git add sirms/test_esp_teacher_system.py
git add sirms/ESP_TEACHER_*.md

# 2. Commit
git commit -m "Add ESP Teacher Management System"

# 3. Push
git push origin main
```

---

## Post-Deployment Tasks

### 1. Populate ESP Teachers
```bash
# Via Render Shell
python populate_esp_teachers.py
```

### 2. Test System
```bash
# Via Render Shell
python test_esp_teacher_system.py
```

### 3. Verify in Browser
- Login as counselor
- Go to "Manage ESP Teachers"
- Verify 5 teachers are listed
- Go to "For VPF"
- Test assignment functionality

---

## Troubleshooting

### Issue: ESP Teachers Not Showing
**Solution:**
```bash
# Run populate script on Render
python populate_esp_teachers.py
```

### Issue: Dropdown Empty
**Solution:**
- Check if ESP teachers exist in database
- Verify `is_active=True` for teachers
- Check view logic in `esp_teacher_views.py`

### Issue: Assignment Not Working
**Solution:**
- Check VPFCase model has `esp_teacher_assigned` field
- Verify migrations ran successfully
- Check form submission in browser console

### Issue: 404 on ESP Teacher URLs
**Solution:**
- Verify URLs are in `incidents/urls.py`
- Check URL patterns match view names
- Restart Render service

---

## Environment Variables (Already Set)

These should already be configured in Render:
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False
- `ALLOWED_HOSTS` - Your Render domain

---

## Build Script (build.sh)

Your existing `build.sh` should handle everything:
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## Files Being Deployed

### New Files:
- `incidents/esp_teacher_views.py`
- `templates/counselor/manage_esp_teachers.html`
- `templates/counselor/esp_teacher_form.html`
- `templates/counselor/for_vpf.html` (updated)
- `templates/counselor/assign_esp_teacher.html`
- `populate_esp_teachers.py`
- `test_esp_teacher_system.py`
- `ESP_TEACHER_*.md` (6 documentation files)

### Modified Files:
- `incidents/urls.py` (ESP teacher routes)
- `incidents/forms.py` (ESPTeacherForm - already exists)
- `incidents/models.py` (Counselor, VPFCase - already exists)

---

## Expected Deployment Time

- **Code Push:** 1 minute
- **Render Build:** 5-10 minutes
- **Migration:** 1 minute
- **Total:** ~10-15 minutes

---

## Verification Checklist

After deployment, verify:
- [ ] Site loads without errors
- [ ] Can access `/manage-esp-teachers/`
- [ ] Can access `/for-vpf/`
- [ ] Can add ESP teacher
- [ ] Can edit ESP teacher
- [ ] Can assign teacher to VPF case
- [ ] Dropdown shows teacher info correctly
- [ ] Email format validated
- [ ] Phone format validated
- [ ] Maximum 5 teachers enforced

---

## Rollback Plan (If Needed)

If deployment fails:
```bash
# Revert to previous commit
git revert HEAD
git push origin main
```

Or in Render Dashboard:
1. Go to your service
2. Click "Manual Deploy"
3. Select previous successful deployment

---

## Success Indicators

✅ **Deployment Successful When:**
- Build completes without errors
- Migrations run successfully
- Site loads normally
- ESP Teacher pages accessible
- Can add and assign teachers
- All features working as expected

---

## Next Steps After Deployment

1. **Populate ESP Teachers:**
   ```bash
   python populate_esp_teachers.py
   ```

2. **Test System:**
   - Login as counselor
   - Add/edit ESP teachers
   - Assign to VPF cases
   - Verify all features

3. **Monitor:**
   - Check Render logs for errors
   - Monitor application performance
   - Verify database queries

4. **Document:**
   - Update deployment log
   - Note any issues encountered
   - Record resolution steps

---

## Contact & Support

If issues arise:
1. Check Render logs
2. Review error messages
3. Verify database state
4. Check documentation files

---

**Deployment Date:** December 4, 2025  
**Feature:** ESP Teacher Management System  
**Status:** Ready to Deploy  
**Estimated Time:** 10-15 minutes  

---

## Quick Deploy Command

```bash
# One-line deploy
git add . && git commit -m "Deploy ESP Teacher System - Dec 4, 2025" && git push origin main
```

Then wait for Render to build and deploy automatically! 🚀
