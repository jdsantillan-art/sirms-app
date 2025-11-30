# Violation Classification System

## Overview
The system now classifies all violations into **two main categories**:
1. **Prohibited Acts** (30 violations)
2. **Other School Policies** (6 violations)

---

## Classification Categories

### 🚫 Prohibited Acts (30 Items)

Serious violations with legal references and significant consequences:

1. **Possession of deadly weapons**
   - References: DO 40, s.2012; School Policy on contraband; RPC

2. **Use/peddling/pushing of marijuana or prohibited drugs**
   - References: RA 9165; DO 40, s.2012

3. **Assaulting teacher/school personnel or physical assault**
   - References: RPC Art. 148, 152; Commonwealth Act 578; DO 40, s.2012

4. **Theft/shoplifting/stealing**
   - References: RPC Art. 308-310; School Policy

5. **Forging/tampering of school records**
   - References: RPC Art. 171-172; School Policy

6. **Gross indecency in conduct**
   - References: School Policy; DO 40, s.2012; RPC

7. **Organization/membership in unsanctioned groups**
   - References: DO 7, s.2006; School Policy

8. **Extortion/swindling**
   - References: RPC Art. 293-296, 315; DO 40, s.2012

9. **Bullying or peer abuse**
   - References: RA 10627; DO 55, s.2013; DO 40, s.2012

10. **Inflicting injury upon another student**
    - References: RPC Art. 262-266; DO 40, s.2012

11. **Vandalism/destruction of school property**
    - References: RPC Art. 327; School Policy

12. **Destruction of nature**
    - References: School Policy; LGU Ordinance

13. **Littering/non-observance of waste management**
    - References: RA 9003; School Policy; LGU Ordinance

14. **Cheating on classwork**
    - References: School Policy; DO 40, s.2012

15. **Intentional spitting on walls and railings**
    - References: School Policy

16. **Smoking & vaping**
    - References: RA 9211; EO 26 (2017); RA 11900

17. **Taking/bringing intoxicating drinks or entering under influence**
    - References: School Policy; DO 40, s.2012

18. **Any form of gambling**
    - References: PD 1602; School Policy

19. **Insinuating trouble or fight**
    - References: DO 40, s.2012; School Policy

20. **Unsafe behavior on school premises**
    - References: School Safety Policy; DO 40, s.2012

21. **Making unnecessary noise in corridors**
    - References: School Policy

22. **Making derogatory statements**
    - References: DO 40, s.2012; RA 10627; School Policy

23. **Climbing over perimeter fence**
    - References: School Policy; DO 40, s.2012

24. **Truancy/habitual absenteeism/tardiness**
    - References: DO 8, s.2015; School Policy

25. **Unauthorized use of personal gadgets in class**
    - References: School Policy; DO 40, s.2012

26. **Possession/showing of pornographic materials**
    - References: PD 969/960; RA 7610; DO 40, s.2012

27. **Bringing and igniting firecrackers**
    - References: RA 7183; School Policy

28. **School I.D. violation**
    - References: School Policy; DO 32, s.2003

29. **Hurling stones/materials over fence**
    - References: RPC Art. 327; School Policy; DO 40, s.2012

30. **Prohibited games on campus**
    - References: School Policy; DO 40, s.2012

---

### 📋 Other School Policies (6 Items)

Appearance and conduct policies:

1. **Improper haircut (male students)**
   - References: DepEd Order No. 46, s. 2008, item No.4

2. **Excessive makeup/colored nail polish**
   - References: DepEd Order No. 46, s. 2008, item No.4

3. **Unnatural hair dyes**
   - References: DepEd Order No. 46, s. 2008, item No.4

4. **Unauthorized body modifications**
   - Tattoos, earrings (male), multiple earrings (female), body piercings
   - References: DepEd Order No. 46, s. 2008, item No.4

5. **Wearing caps inside classroom**
   - References: DepEd Order No. 46, s. 2008, item No.4

6. **LGBTQA+ Non-compliance with uniform/hairstyle**
   - References: DepEd Order No. 32, s. 2017, Gender-Responsive Basic Education Policy

---

## Database Structure

### Model Changes

```python
class IncidentType(models.Model):
    SEVERITY_CHOICES = [
        ('prohibited', 'Prohibited Acts'),
        ('school_policy', 'Other School Policies'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    legal_references = models.TextField()
    
    class Meta:
        ordering = ['severity', 'name']
```

---

## User Interface Updates

### Report Incident Form

The incident type dropdown now shows **grouped options**:

```
Select Violation Type *
├── 🚫 Prohibited Acts
│   ├── Possession of deadly weapons
│   ├── Use/peddling/pushing of marijuana or prohibited drugs
│   ├── Assaulting teacher/school personnel or physical assault
│   └── ... (27 more)
└── 📋 Other School Policies
    ├── Improper haircut (male students)
    ├── Excessive makeup/colored nail polish
    └── ... (4 more)
```

### Benefits:
✅ **Clear categorization** - Easy to find the right violation type  
✅ **Visual grouping** - Prohibited Acts vs School Policies  
✅ **Better organization** - Alphabetically sorted within groups  
✅ **Legal references** - Automatically displayed when selected  

---

## Classification Logic

### When a report is submitted:

1. **User selects violation type** from grouped dropdown
2. **System automatically classifies** based on severity field:
   - `prohibited` → Prohibited Acts
   - `school_policy` → Other School Policies
3. **Classification is saved** with the incident report
4. **Legal references** are stored and displayed
5. **All interfaces** show the correct classification

### Where Classification Appears:

- ✅ Report Incident Form (grouped dropdown)
- ✅ Fact-Check Reports (severity badge)
- ✅ Report Detail Page (classification section)
- ✅ Case Evaluation (incident type display)
- ✅ All Reports List (type column)
- ✅ Dashboard Statistics (filtered by type)

---

## Migration Steps

### To Update Your Database:

1. **Run the migration batch file:**
   ```batch
   migrate_incident_types.bat
   ```

2. **Or manually:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python update_incident_types.py
   ```

### What Happens:
1. Database schema updated (severity field expanded to 20 chars)
2. Old incident types cleared
3. 30 Prohibited Acts created
4. 6 Other School Policies created
5. All with proper legal references

---

## Legal References

### Key DepEd Orders:
- **DO 40, s.2012** - Child Protection Policy
- **DO 46, s.2008** - Physical hygiene and school decorum
- **DO 32, s.2017** - Gender-Responsive Basic Education Policy
- **DO 7, s.2006** - Prohibition of fraternities/sororities
- **DO 55, s.2013** - IRR of Anti-Bullying Act
- **DO 8, s.2015** - Classroom Assessment
- **DO 32, s.2003** - Student discipline guidelines

### Key Republic Acts:
- **RA 9165** - Comprehensive Dangerous Drugs Act
- **RA 10627** - Anti-Bullying Act of 2013
- **RA 9003** - Ecological Solid Waste Management Act
- **RA 9211** - Tobacco Regulation Act
- **RA 11900** - Vape Law
- **RA 7610** - Child protection (pornography)
- **RA 7183** - Regulation of Firecrackers

### Revised Penal Code (RPC):
- **Art. 148** - Direct Assault
- **Art. 152** - Persons in authority
- **Art. 308-310** - Theft
- **Art. 171-172** - Falsification of documents
- **Art. 293-296** - Robbery
- **Art. 315** - Estafa/Swindling
- **Art. 262-266** - Physical Injuries
- **Art. 327** - Malicious Mischief

### Other Laws:
- **Commonwealth Act 578** - Teachers as persons in authority
- **PD 1602** - Illegal gambling penalties
- **PD 969/960** - Obscenity Laws
- **EO 26 (2017)** - Smoke-Free Environments

---

## Reporting Flow

### For Prohibited Acts:
1. Report submitted → DO fact-checks
2. DO classifies as Minor or Major
3. If Major → Counselor evaluates
4. Counselor may assign VPF
5. Principal reviews and sanctions

### For Other School Policies:
1. Report submitted → DO fact-checks
2. Usually classified as Minor
3. DO handles directly
4. May involve adviser/teacher
5. Lighter sanctions applied

---

## Files Modified

1. **sirms/incidents/models.py**
   - Updated `IncidentType.SEVERITY_CHOICES`
   - Changed field length to 20 chars
   - Added Meta ordering

2. **sirms/templates/report_incident.html**
   - Added grouped dropdown with optgroups
   - Visual icons for categories
   - Better labeling

3. **sirms/incidents/views.py**
   - Updated incident types ordering
   - Severity-based sorting

4. **sirms/update_incident_types.py** (NEW)
   - Script to populate all 36 incident types
   - Includes all legal references

5. **sirms/migrate_incident_types.bat** (NEW)
   - Batch file to run migration
   - User-friendly process

---

## Testing Checklist

After migration, verify:

- [ ] Report Incident form shows grouped dropdown
- [ ] 30 Prohibited Acts appear under first group
- [ ] 6 Other School Policies appear under second group
- [ ] Legal references display when type selected
- [ ] Reports save with correct classification
- [ ] Fact-check page shows correct severity
- [ ] Report detail shows classification
- [ ] All existing reports still work
- [ ] No database errors

---

## Status

✅ **Implemented and Ready**

- Model updated
- Templates updated
- Views updated
- Migration scripts created
- Documentation complete
- 36 incident types defined
- All legal references included

---

## Future Enhancements

- 📊 Statistics by violation category
- 📈 Trend analysis (Prohibited vs Policies)
- 🔍 Advanced filtering by category
- 📱 Mobile-optimized dropdown
- 🎨 Color-coded severity badges
- 📧 Category-specific notifications
- 📋 Printable violation reference guide
