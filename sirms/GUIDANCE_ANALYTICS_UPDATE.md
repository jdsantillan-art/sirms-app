# Guidance Counselor Dashboard Analytics Update

## Overview
Updated the Guidance Counselor dashboard analytics cards to display the correct metrics with clickable links to relevant pages.

## Changes Made

### Dashboard Analytics Cards (6 Total)

All cards are now clickable and link to their respective management pages:

1. **Total Prohibited Acts** (Red Card)
   - Variable: `total_prohibited_acts`
   - Links to: Major Case Review page
   - Icon: Ban icon (fas fa-ban)
   - Description: "Click to review"

2. **Total OSP** (Blue Card)
   - Variable: `total_osp`
   - Links to: Major Case Review page
   - Icon: Clipboard list (fas fa-clipboard-list)
   - Description: "Other School Policies"

3. **Scheduled Sessions** (Purple Card)
   - Variable: `scheduled_sessions`
   - Links to: Counselor Schedule page
   - Icon: Calendar (fas fa-calendar-alt)
   - Description: "Click to manage"

4. **Completed Sessions** (Green Card)
   - Variable: `completed_sessions`
   - Links to: Counseling Management page (filtered by completed status)
   - Icon: Check circle (fas fa-check-circle)
   - Description: "Click to view"

5. **Completed VPF** (Orange Card)
   - Variable: `completed_vpf`
   - Links to: VPF Cases page
   - Icon: User shield (fas fa-user-shield)
   - Description: "Click to view VPF"

6. **Total VPF Referrals** (Teal Card)
   - Variable: `total_vpf_referrals`
   - Links to: VPF Cases page
   - Icon: User check (fas fa-user-check)
   - Description: "Click to view all VPF"

## Backend Data (Already Implemented)

The following context variables are already being passed from `views.py`:

```python
context.update({
    'total_prohibited_acts': total_prohibited_acts,
    'total_osp': total_osp,
    'scheduled_sessions': scheduled_sessions_count,
    'completed_vpf': completed_vpf,
    'total_vpf_referrals': total_vpf_referrals,
    'completed_sessions': completed_sessions,
})
```

## Features

- **Clickable Cards**: All analytics cards are clickable and navigate to relevant pages
- **Hover Effects**: Cards scale up slightly on hover for better UX
- **Counter Animation**: Numbers animate from 0 to target value on page load
- **Color Coding**: Each metric has a distinct color scheme for easy identification
- **Responsive Design**: Cards adapt to different screen sizes (grid layout)

## Files Modified

- `sirms/templates/dashboard.html` - Updated counselor analytics section

## Testing

To verify the changes:
1. Log in as a Guidance Counselor
2. View the dashboard
3. Verify all 6 analytics cards display correct data
4. Click each card to ensure proper navigation
5. Verify hover effects and animations work correctly

## Notes

- The 6th card was previously duplicated showing "Completed" - now correctly shows "Total VPF Referrals"
- All cards maintain consistent styling and behavior
- Links are properly configured to filter data where applicable (e.g., completed sessions filter)
