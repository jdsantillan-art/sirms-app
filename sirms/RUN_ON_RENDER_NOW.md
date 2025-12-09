# ⚡ Create Ms. Mercado's Account on Render NOW

## Status: Code Deployed ✓

The code has been pushed to GitHub. Render is now deploying it automatically.

## Steps to Create Account on Render

### Option 1: Use Render Shell (Easiest)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Login to your account

2. **Open Your SIRMS Service**
   - Click on your SIRMS web service
   - Wait for deployment to finish (green "Live" status)

3. **Open Shell**
   - Click on "Shell" tab in the left sidebar
   - Wait for shell to connect

4. **Run This Command**
   Copy and paste this entire command:

```bash
python manage.py create_mercado
```

   OR use this one-liner:

```bash
python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('✓ Account created successfully!')"
```

5. **Verify Success**
   You should see:
   ```
   ============================================================
   ACCOUNT CREATED SUCCESSFULLY
   ============================================================
   Username: stephanie.mercado
   Password: Teacher2024!
   ```

### Option 2: Use Render API (Advanced)

If you have Render API access, you can run:

```bash
curl -X POST https://api.render.com/v1/services/YOUR_SERVICE_ID/shell \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"command": "python manage.py create_mercado"}'
```

## After Account is Created

### Login Credentials

**URL:** Your Render app URL (e.g., https://sirms-app.onrender.com)

**Username:** `stephanie.mercado`  
**Password:** `Teacher2024!`

### What Ms. Mercado Will See

- Dashboard with all Grade 8 Section 2 student reports
- Notifications for new incidents
- Updates from Guidance, DO, and ESP Teacher
- Real-time case status changes

## Troubleshooting

### If deployment is taking too long:
- Check Render dashboard for deployment status
- Look for any error messages in the logs
- Wait 5-10 minutes for deployment to complete

### If shell command fails:
- Make sure deployment is complete (green "Live" status)
- Try the one-liner command instead
- Check that you're in the correct service

### If login still doesn't work:
- Clear browser cache
- Try incognito/private browsing mode
- Verify you're using the correct Render URL
- Double-check username and password (case-sensitive)

## Quick Reference

**Render Dashboard:** https://dashboard.render.com  
**Username:** stephanie.mercado  
**Password:** Teacher2024!  
**Role:** Teacher  
**Assignment:** Grade 8 Section 2 (ICT)

---

**Next Step:** Go to Render Dashboard and run the command in Shell!
