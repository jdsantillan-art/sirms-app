# Ms. Mercado Account - Login Issue Solution

## The Problem

You're getting "Invalid username or password" which usually means one of these:

### 1. **Testing on Production (Render) but Account Created Locally**

If you're trying to login at your **Render production URL** (like `https://your-app.onrender.com`), the account we created only exists in your **local database**, not on Render's database.

**Solution:** Create the account on Render using Django Admin

### 2. **Typo in Username or Password**

Common mistakes:
- Username has a **dot** not a space: `stephanie.mercado` (not `stephanie mercado`)
- Password is case-sensitive: `Teacher2024!` (capital T's, exclamation at end)
- Extra spaces before or after

### 3. **Account Not Saved Properly**

The database might not have committed the changes.

---

## SOLUTION 1: Use Django Admin (EASIEST)

This works for both local and production:

### Step 1: Login to Django Admin

**Local:** http://localhost:8000/admin  
**Production:** https://your-render-url.onrender.com/admin

### Step 2: Login with Admin Account

Use your existing admin credentials (counselor, DO, or superuser account)

### Step 3: Create User

1. Click on **"Users"** or **"Custom users"**
2. Click **"Add User"** button
3. Fill in:
   - **Username:** `stephanie.mercado`
   - **Password:** `Teacher2024!`
   - **Password confirmation:** `Teacher2024!`
4. Click **"Save"**

### Step 4: Edit User Details

After saving, you'll see more fields:
- **First name:** Stephanie
- **Last name:** Mercado
- **Email:** stephanie.mercado@school.edu
- **Role:** Select **"Teacher"** from dropdown
- **Employee ID:** TCH-2024-008
- **Grade level:** Grade 8
- **Section:** Section 2
- **Active:** ✓ (checked)
- **Staff status:** ☐ (unchecked)
- **Superuser status:** ☐ (unchecked)

### Step 5: Save

Click **"Save"** at the bottom

### Step 6: Test Login

Now try logging in with:
- Username: `stephanie.mercado`
- Password: `Teacher2024!`

---

## SOLUTION 2: Use Existing Teacher Account

If you already have teacher accounts in the system, you can use one of those for testing:

1. Check your existing accounts in Django Admin
2. Use an existing teacher's credentials
3. Or reset an existing teacher's password

---

## SOLUTION 3: Create via Command Line (For Production/Render)

If you have SSH access to Render or can run commands:

```bash
python manage.py shell
```

Then paste this:

```python
from incidents.models import CustomUser

# Delete if exists
CustomUser.objects.filter(username='stephanie.mercado').delete()

# Create new
user = CustomUser.objects.create_user(
    username='stephanie.mercado',
    password='Teacher2024!',
    email='stephanie.mercado@school.edu',
    first_name='Stephanie',
    last_name='Mercado',
    role='teacher',
    employee_id='TCH-2024-008',
    grade_level='Grade 8',
    section='Section 2',
    is_active=True
)

print(f"Created: {user.username}")
print("Password: Teacher2024!")
```

Press Ctrl+D to exit

---

## SOLUTION 4: Check What You're Testing

### Are you testing on LOCAL or PRODUCTION?

**Local Development:**
- URL: http://localhost:8000 or http://127.0.0.1:8000
- Database: db.sqlite3 file in your sirms folder
- Account created: ✓ YES (we created it locally)

**Production (Render):**
- URL: https://your-app-name.onrender.com
- Database: PostgreSQL on Render
- Account created: ✗ NO (not created on production yet)

**If testing on Render:** You MUST create the account on Render's database using Django Admin (Solution 1)

---

## Quick Test: Which Database?

Run this locally to see if account exists:

```bash
cd sirms
python manage.py shell -c "from incidents.models import CustomUser; print('Users:', CustomUser.objects.filter(username='stephanie.mercado').count())"
```

- If it shows `Users: 1` → Account exists locally
- If it shows `Users: 0` → Account doesn't exist

---

## Recommended Steps RIGHT NOW:

1. **Determine where you're testing:**
   - Local? → Account should work
   - Render? → Need to create on Render

2. **Use Django Admin (easiest):**
   - Go to /admin
   - Login with existing admin account
   - Create user as shown in Solution 1

3. **Test login:**
   - Username: `stephanie.mercado` (lowercase, with dot)
   - Password: `Teacher2024!` (capital T's, with !)

---

## Still Not Working?

If you've tried everything above and it still doesn't work:

1. **Check browser console** for errors (F12 → Console tab)
2. **Try different browser** (Chrome, Firefox, Edge)
3. **Clear browser cache** (Ctrl+Shift+Delete)
4. **Check if server is running** (for local testing)
5. **Verify you're on the correct URL** (local vs production)

---

## Contact Info for Debugging

If you tell me:
1. Are you testing on **local** or **Render production**?
2. What URL are you using to login?
3. Do you have access to Django Admin?

I can provide more specific help!
