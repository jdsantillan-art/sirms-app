# Bullying Type Dropdown Feature

## Overview
When reporting an incident, if "Bullying" is selected as the violation type, a dropdown automatically appears allowing the reporter to specify the exact type of bullying. This provides better categorization and documentation of bullying incidents.

## Features

### 1. Conditional Display
- Dropdown only appears when a bullying-related incident type is selected
- Automatically hides when non-bullying incident types are selected
- Smooth transition with no page reload

### 2. Bullying Types
Seven specific types of bullying can be selected:
- **Physical Bullying** - Hitting, pushing, physical harm
- **Psychological Bullying** - Threats, intimidation, manipulation
- **Sexual Bullying** - Unwanted sexual comments or actions
- **Emotional Bullying** - Humiliation, exclusion, emotional harm
- **Cyber Bullying** - Online harassment, social media attacks
- **Social Bullying** - Spreading rumors, social exclusion
- **Gender-based Bullying** - Harassment based on gender identity

### 3. Required Field
- When bullying is selected, the bullying type becomes required
- Form cannot be submitted without selecting a bullying type
- Validation message appears if not filled

### 4. Data Storage
- Bullying type is prepended to the incident description
- Format: `[Bullying Type: {Type}]` followed by description
- Easily identifiable in reports and analytics
- Searchable and filterable

## How It Works

### For Reporters:

1. **Fill Out Incident Report**
   - Navigate to Report Incident page
   - Fill in reporter and student information

2. **Select Violation Type**
   - In the "Incident Details" section
   - Click on "Violation Type" dropdown
   - Select any bullying-related incident type

3. **Bullying Type Appears**
   - Dropdown automatically appears below violation type
   - Shows "Bullying Type *" with red asterisk (required)
   - Lists all 7 types of bullying

4. **Select Bullying Type**
   - Choose the most appropriate type
   - Info message: "Please specify the type of bullying"
   - Continue filling out the rest of the form

5. **Submit Report**
   - Bullying type is saved with the report
   - Appears in description field with special formatting
   - Can be viewed by all authorized users

### For Reviewers:

When viewing a bullying report:
- Description shows: `[Bullying Type: Physical]` at the top
- Followed by the detailed description
- Easy to identify the specific type at a glance

## User Interface

### Incident Report Form
**Before selecting bullying:**
```
Violation Type: [Select Violation Type ▼]
Description: [Text area]
```

**After selecting bullying:**
```
Violation Type: [Bullying ▼]

Bullying Type: [Select Bullying Type ▼] *
ℹ️ Please specify the type of bullying

Description: [Text area]
```

### Bullying Type Dropdown
```
Select Bullying Type
├─ Physical Bullying
├─ Psychological Bullying
├─ Sexual Bullying
├─ Emotional Bullying
├─ Cyber Bullying
├─ Social Bullying
└─ Gender-based Bullying
```

## Technical Implementation

### Files Modified:
1. `templates/report_incident.html` - Added bullying type dropdown and JavaScript
2. `incidents/views.py` - Added bullying type handling in report_incident view

### HTML Structure:
```html
<div id="bullying-type-div" style="display: none;">
    <label>Bullying Type <span class="text-red-500">*</span></label>
    <select name="bullying_type" id="id_bullying_type">
        <option value="">Select Bullying Type</option>
        <option value="Physical">Physical Bullying</option>
        <!-- ... other options ... -->
    </select>
</div>
```

### JavaScript Logic:
```javascript
incidentTypeSelect.addEventListener('change', function() {
    const incidentName = incidentTypes[selectedId].name.toLowerCase();
    
    if (incidentName.includes('bullying')) {
        bullyingTypeDiv.style.display = 'block';
        bullyingTypeSelect.required = true;
    } else {
        bullyingTypeDiv.style.display = 'none';
        bullyingTypeSelect.required = false;
    }
});
```

### Backend Processing:
```python
bullying_type = request.POST.get('bullying_type', '')
if bullying_type:
    report.description = f"[Bullying Type: {bullying_type}]\n\n{description}"
```

## Data Format

### Stored in Database:
```
Description field contains:
"[Bullying Type: Physical]

Student was pushed and hit during recess. 
Multiple witnesses present. Incident occurred 
near the basketball court."
```

### Display Format:
When viewing the report, the description shows the bullying type clearly at the top, making it easy to categorize and analyze bullying incidents.

## Benefits

### 1. Better Categorization
- Specific types of bullying are documented
- Easier to track patterns and trends
- Better data for anti-bullying programs

### 2. Improved Reporting
- Reporters provide more detailed information
- Reduces ambiguity in bullying reports
- Helps identify specific intervention needs

### 3. Enhanced Analytics
- Can filter reports by bullying type
- Track which types are most common
- Target prevention efforts effectively

### 4. Legal Documentation
- Clear categorization for legal purposes
- Meets anti-bullying law requirements
- Proper documentation for investigations

### 5. User-Friendly
- Automatic display/hide
- No extra steps for non-bullying reports
- Clear labeling and instructions

## Use Cases

### Physical Bullying Example:
```
Violation Type: Bullying
Bullying Type: Physical Bullying
Description: Student A repeatedly pushed and 
shoved Student B during lunch break...
```

### Cyber Bullying Example:
```
Violation Type: Bullying
Bullying Type: Cyber Bullying
Description: Student created fake social media 
account to harass classmate...
```

### Psychological Bullying Example:
```
Violation Type: Bullying
Bullying Type: Psychological Bullying
Description: Student threatened to harm another 
student's family if they reported...
```

## Validation Rules

1. **Conditional Requirement**
   - Only required when bullying is selected
   - Not required for other incident types

2. **Form Validation**
   - Cannot submit without selecting type
   - Browser shows validation message
   - Field highlighted in red if empty

3. **Data Integrity**
   - Bullying type always saved with description
   - Format is consistent across all reports
   - Easy to parse and analyze

## Reporting & Analytics

### Potential Reports:
- Bullying incidents by type (pie chart)
- Trends over time by bullying type
- Most common bullying types per grade level
- Cyber bullying vs traditional bullying
- Gender-based bullying statistics

### Search & Filter:
- Search for specific bullying types
- Filter reports by bullying category
- Generate targeted intervention reports

## Best Practices

### For Reporters:
1. **Be Specific**: Choose the most accurate type
2. **Multiple Types**: If multiple types apply, choose the primary one and mention others in description
3. **Detailed Description**: Still provide full details in description field
4. **Evidence**: Attach evidence when available

### For Administrators:
1. **Review Patterns**: Monitor which types are most common
2. **Targeted Interventions**: Design programs for specific types
3. **Training**: Train staff on identifying different types
4. **Prevention**: Use data to prevent future incidents

## Future Enhancements

Potential additions:
1. **Multiple Type Selection**: Allow selecting multiple bullying types
2. **Severity Rating**: Add severity level for each type
3. **Witness Count**: Track number of witnesses
4. **Location Tracking**: Common locations for each type
5. **Time Patterns**: When each type occurs most
6. **Victim Impact**: Document impact on victim
7. **Intervention Tracking**: Track which interventions work best for each type

## Testing Checklist

- [x] Dropdown appears when bullying selected
- [x] Dropdown hides when non-bullying selected
- [x] All 7 bullying types display correctly
- [x] Field is required when visible
- [x] Field is not required when hidden
- [x] Form validation works
- [x] Bullying type saves to description
- [x] Format is correct in database
- [x] No diagnostic errors

## Support

### Common Questions:

**Q: What if multiple types of bullying occurred?**
A: Select the primary type and mention other types in the description field.

**Q: Can I change the bullying type after submission?**
A: Contact the Discipline Office to update the report.

**Q: What if I'm not sure which type?**
A: Choose the closest match and provide details in the description. DO will review and may reclassify if needed.

**Q: Is this required for all bullying reports?**
A: Yes, when you select a bullying-related violation type, you must specify the type.

## Conclusion

The bullying type dropdown feature provides:
- ✅ Better categorization of bullying incidents
- ✅ More detailed reporting
- ✅ Enhanced analytics capabilities
- ✅ User-friendly interface
- ✅ Automatic conditional display
- ✅ Proper documentation for legal purposes

This feature helps schools better understand, track, and address different types of bullying, leading to more effective prevention and intervention strategies.
