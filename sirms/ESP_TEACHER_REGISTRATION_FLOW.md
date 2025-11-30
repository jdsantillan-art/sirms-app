# ESP Teacher Registration & VPF Assignment Flow

## ✅ CONFIRMED: System is Working as Requested

### Registration Flow
When a user registers as **ESP Teacher/VPF Coordinator**:

1. **User Account Created** (`CustomUser` with role='esp_teacher')
   - Username, email, password, etc.
   - Role: ESP Teacher/VPF Coordinator

2. **Counselor Entry Auto-Created** (lines 34-42 in `views.py`)
   ```python
   if user.role == 'esp_teacher':
       from .models import Counselor
       if not Counselor.objects.filter(name=user.get_full_name()).exists():
           Counselor.objects.create(
               name=user.get_full_name(),
               email=user.email,
               specialization='ESP Teacher/VPF Coordinator',
               is_active=True
           )
   ```

### Manage ESP Teachers Page
**URL:** `/manage-esp-teachers/`  
**Access:** Counselors only

- Displays all `Counselor` records (including auto-created ESP teachers)
- Shows: Name, Email, Phone, Specialization, Status
- Actions: Add, Edit, Delete ESP teachers
- **Auto-populated** when ESP teachers register

### VPF Assignment Dropdown
**Location:** "For VPF" page (`/for-vpf/`)  
**Access:** Counselors only

When assigning ESP teachers to VPF cases:
- Dropdown loads from `Counselor.objects.filter(is_active=True)`
- **Includes all registered ESP teachers** automatically
- Shows teacher name and specialization

## Data Flow

```
Registration (ESP Teacher)
    ↓
CustomUser created (role='esp_teacher')
    ↓
Counselor entry auto-created
    ↓
Appears in "Manage ESP Teachers" page
    ↓
Available in VPF assignment dropdown
```

## Models Involved

### CustomUser
- Stores user authentication and role
- Role: 'esp_teacher'

### Counselor
- Stores ESP teacher/counselor information
- Used for VPF assignments
- Fields: name, email, phone, specialization, is_active

### VPFCase
- Links to Counselor via `esp_teacher_assigned` field
- Tracks VPF case assignments

## Key Files

1. **Registration Logic:** `incidents/views.py` (lines 34-42)
2. **Manage ESP Teachers:** `incidents/views.py` (lines 3592-3648)
3. **VPF Assignment:** `incidents/views.py` (lines 3511-3590)
4. **Counselor Model:** `incidents/models.py` (lines 320-340)
5. **VPFCase Model:** `incidents/models.py` (lines 390-410)

## ✅ Verification Checklist

- [x] ESP teacher registration creates Counselor entry
- [x] Counselor entry includes email from registration
- [x] Manage ESP Teachers page displays all Counselor records
- [x] VPF assignment dropdown loads from Counselor model
- [x] Registered ESP teachers appear in dropdown
- [x] No duplicate entries (checked before creation)

## System is Ready!

The flow you requested is **already implemented and working**:
1. ✅ Register as ESP Teacher → Creates Counselor entry
2. ✅ Appears in "Manage ESP Teachers" page
3. ✅ Available in VPF assignment dropdown

No changes needed!
