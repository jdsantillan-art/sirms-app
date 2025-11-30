"""
Update Incident Types with New Classification System
Prohibited Acts vs Other School Policies
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentType

# Clear existing incident types
print("Clearing existing incident types...")
IncidentType.objects.all().delete()

# Prohibited Acts (30 items)
prohibited_acts = [
    {
        'name': 'Possession of deadly weapons',
        'description': 'Possession of deadly weapons (e.g., Indian pana, ice pick, pointed comb, knives, improvised weapons)',
        'severity': 'prohibited',
        'legal_references': 'DepEd Child Protection Policy — DepEd Order (DO) 40, s.2012; School Policy on contraband; RPC provisions on unlawful aggression may apply case-to-case.'
    },
    {
        'name': 'Use/peddling/pushing of marijuana or prohibited drugs',
        'description': 'Use of / peddling / pushing of marijuana or any prohibited drugs',
        'severity': 'prohibited',
        'legal_references': 'RA 9165 (Comprehensive Dangerous Drugs Act of 2002) & DepEd\'s Anti-Drug policies; DO 40, s.2012 (protection/discipline procedures).'
    },
    {
        'name': 'Assaulting teacher/school personnel or physical assault',
        'description': 'Assaulting a teacher or school personnel; participating in unsanctioned strikes/demonstrations; inflicting injury upon another student / physical assault',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 148 (Direct Assault) in relation to Art. 152 (teachers/personnel as persons in authority via Commonwealth Act 578); DO 40, s.2012 (violence, threats, due process). Peaceable assembly needs prior approval per School Policy.'
    },
    {
        'name': 'Theft/shoplifting/stealing',
        'description': 'Theft / shoplifting / stealing (in-campus or off-campus)',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 308-310 (Theft); School Policy for administrative discipline.'
    },
    {
        'name': 'Forging/tampering of school records',
        'description': 'Forging / tampering of school records; misrepresentation',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 171-172 (Falsification of documents); School Policy on academic records.'
    },
    {
        'name': 'Gross indecency in conduct',
        'description': 'Gross indecency in conduct (PDA; acts of lasciviousness; exhibitionism) or perennial misbehavior',
        'severity': 'prohibited',
        'legal_references': 'School Policy / Code of Conduct; DO 40, s.2012 (protection from sexual harassment/abuse). Criminal acts, if any, fall under RPC (e.g., acts of lasciviousness).'
    },
    {
        'name': 'Organization/membership in unsanctioned groups',
        'description': 'Organization/membership in any fraternity, sorority, gang, or any group not sanctioned by the school',
        'severity': 'prohibited',
        'legal_references': 'DO 7, s.2006 (Prohibition of fraternities/sororities in elementary & secondary schools); School Policy on student organizations.'
    },
    {
        'name': 'Extortion/swindling',
        'description': 'Extortion / swindling',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 293-296 (Robbery with violence/intimidation); RPC Art. 315 (Estafa/Swindling); DO 40, s.2012 (bullying/harassment).'
    },
    {
        'name': 'Bullying or peer abuse',
        'description': 'Bullying or peer abuse',
        'severity': 'prohibited',
        'legal_references': 'RA 10627 (Anti-Bullying Act of 2013); DO 55, s.2013 (IRR of RA 10627); DO 40, s.2012 (Child Protection Policy; Sec. 3.M definition of bullying).'
    },
    {
        'name': 'Inflicting injury upon another student',
        'description': 'Inflicting injury upon another student/physical assault',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 262-266 (Physical Injuries); DO 40, s.2012 (Violence, threats); School Policy.'
    },
    {
        'name': 'Vandalism/destruction of school property',
        'description': 'Vandalism / intentional destruction of school property',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 327 (Malicious Mischief); School Policy (restitution/discipline).'
    },
    {
        'name': 'Destruction of nature',
        'description': 'Destruction of nature (plants/trees/animals used for education)',
        'severity': 'prohibited',
        'legal_references': 'School Policy; possible LGU Ordinance / environmental laws depending on context.'
    },
    {
        'name': 'Littering/non-observance of waste management',
        'description': 'Littering/scattering pieces of papers/peelings/wrappers/plastics or non-observance of waste/garbage management',
        'severity': 'prohibited',
        'legal_references': 'RA 9003 (Ecological Solid Waste Management Act); School Policy; LGU Ordinance.'
    },
    {
        'name': 'Cheating on classwork',
        'description': 'Cheating on classwork',
        'severity': 'prohibited',
        'legal_references': 'School Policy on Academic Integrity; DO 40, s.2012 (discipline due process).'
    },
    {
        'name': 'Intentional spitting on walls and railings',
        'description': 'Intentional spitting on walls and railings of stairs',
        'severity': 'prohibited',
        'legal_references': 'School Policy (sanitation & conduct).'
    },
    {
        'name': 'Smoking & vaping',
        'description': 'Smoking & vaping (in-campus & within the 20-meter perimeter radius outside the school)',
        'severity': 'prohibited',
        'legal_references': 'RA 9211 (Tobacco Regulation Act) & EO 26 (2017) (Smoke-Free Environments); RA 11900 (Vape Law, restricts sales/use by minors & in schools); School Policy (alcohol prohibition).'
    },
    {
        'name': 'Taking/bringing intoxicating drinks or entering under influence',
        'description': 'Taking and/or bringing any intoxicating drinks on campus or entering the campus under the influence of alcohol',
        'severity': 'prohibited',
        'legal_references': 'School Policy; DO 40, s.2012 (safety and well-being provisions).'
    },
    {
        'name': 'Any form of gambling',
        'description': 'Any form of gambling',
        'severity': 'prohibited',
        'legal_references': 'PD 1602 (Illegal gambling penalties); School Policy.'
    },
    {
        'name': 'Insinuating trouble or fight',
        'description': 'Insinuating trouble or fight',
        'severity': 'prohibited',
        'legal_references': 'DO 40, s.2012 (violence/threats); School Policy.'
    },
    {
        'name': 'Unsafe behavior on school premises',
        'description': 'Sitting on railings or arms of chairs, jumping and/or sliding on stairway railings in going down, hanging on/jumping over the windows/storeys of building',
        'severity': 'prohibited',
        'legal_references': 'School Safety Policy; DO 40, s.2012 (child protection & safety).'
    },
    {
        'name': 'Making unnecessary noise in corridors',
        'description': 'Shouting or making unnecessary noise while passing along lobbies or corridors',
        'severity': 'prohibited',
        'legal_references': 'School Policy (order and discipline).'
    },
    {
        'name': 'Making derogatory statements',
        'description': 'Making any derogatory statements against fellow student, teacher, school personnel, administrators and visitors',
        'severity': 'prohibited',
        'legal_references': 'DO 40, s.2012 (bullying—verbal abuse); RA 10627, if peer-to-peer; School Policy.'
    },
    {
        'name': 'Climbing over perimeter fence',
        'description': 'Climbing over perimeter fence in going in or out of the school premises',
        'severity': 'prohibited',
        'legal_references': 'School Policy on safety; DO 40, s.2012 (hazardous conduct).'
    },
    {
        'name': 'Truancy/habitual absenteeism/tardiness',
        'description': 'Truancy/habitual absenteeism/tardiness/cutting or skipping classes',
        'severity': 'prohibited',
        'legal_references': 'DO 8, s.2015 (Classroom Assessment—attendance expectations); School Policy.'
    },
    {
        'name': 'Unauthorized use of personal gadgets in class',
        'description': 'Using/playing of personal gadgets while the class is going on (unless allowed by the teacher for educational purposes, and for emergency cases)',
        'severity': 'prohibited',
        'legal_references': 'School Policy on electronic device use; DO 40, s.2012 (classroom discipline).'
    },
    {
        'name': 'Possession/showing of pornographic materials',
        'description': 'Possession and/or showing of pornographic materials (printed or digital)',
        'severity': 'prohibited',
        'legal_references': 'PD 969 / PD 960 (Obscenity Laws); RA 7610 (child protection—pornography); DO 40, s.2012; School Policy.'
    },
    {
        'name': 'Bringing and igniting firecrackers',
        'description': 'Bringing and igniting fire crackers in the school premises',
        'severity': 'prohibited',
        'legal_references': 'RA 7183 (Regulation of Firecrackers); School Policy.'
    },
    {
        'name': 'School I.D. violation',
        'description': 'School I.D. violation such as: tampering; wearing the ID without/or having different picture; wearing a different I.D. or different cord and color, wearing of I.D. with sticker or other accessories',
        'severity': 'prohibited',
        'legal_references': 'School Policy; DO 32, s.2003 (Student discipline guidelines—ID part of uniform compliance).'
    },
    {
        'name': 'Hurling stones/materials over fence',
        'description': 'Hurling stones and/or any other materials over the perimeter fence',
        'severity': 'prohibited',
        'legal_references': 'RPC Art. 327 (Malicious Mischief); School Policy; DO 40, s.2012 (violent/risky conduct).'
    },
    {
        'name': 'Prohibited games on campus',
        'description': 'Playing billiards online & offline games during school hours. Playing kick, badminton, and other ball games on campus is allowed with restrictions. However Games that may cause property or pose a risk to other learners are prohibited inside classroom, along corridors in hallways, near office, parking areas, pathways, and gardens. The designated venues for ballgames are the old covered court (OCC) in the oval field.',
        'severity': 'prohibited',
        'legal_references': 'School Policy on conduct and safety; DO 40, s.2012 (child protection & safe environment).'
    },
]

# Other School Policies (6 items)
school_policies = [
    {
        'name': 'Improper haircut (male students)',
        'description': 'Maintain regular and clean haircuts for male student',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 46, s. 2008, item No.4, Clearly Stipulates that: "4. Promoting physical hygiene and proper school decorum is part of the teaching-learning process in school, thus a student\'s attire and physical appearance should manifest learnings from this process."'
    },
    {
        'name': 'Excessive makeup/colored nail polish',
        'description': 'Wearing excessive makeup, colored nail polish and nail extensions',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 46, s. 2008, item No.4, Clearly Stipulates that: "4. Promoting physical hygiene and proper school decorum is part of the teaching-learning process in school, thus a student\'s attire and physical appearance should manifest learnings from this process."'
    },
    {
        'name': 'Unnatural hair dyes',
        'description': 'Bright colored or unnatural hair dyes',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 46, s. 2008, item No.4, Clearly Stipulates that: "4. Promoting physical hygiene and proper school decorum is part of the teaching-learning process in school, thus a student\'s attire and physical appearance should manifest learnings from this process."'
    },
    {
        'name': 'Unauthorized body modifications',
        'description': 'Wearing Tattoos, earring (male student) and multiple earrings (female student), unnecessary visible body piercing accessories, such as nose rings, lip rings, eyebrow rings and other similar items, while on campus',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 46, s. 2008, item No.4, Clearly Stipulates that: "4. Promoting physical hygiene and proper school decorum is part of the teaching-learning process in school, thus a student\'s attire and physical appearance should manifest learnings from this process."'
    },
    {
        'name': 'Wearing caps inside classroom',
        'description': 'Wearing caps inside the classroom',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 46, s. 2008, item No.4, Clearly Stipulates that: "4. Promoting physical hygiene and proper school decorum is part of the teaching-learning process in school, thus a student\'s attire and physical appearance should manifest learnings from this process."'
    },
    {
        'name': 'LGBTQA+ Non-compliance with uniform/hairstyle',
        'description': 'LGBTQA+ Non-compliance with the prescribed school uniform and hairstyle.',
        'severity': 'school_policy',
        'legal_references': 'DepEd Order No. 32, s. 2017, Gender-Responsive Basic Education Policy, IV.i clearly stipulates that: i. Gender expressions refers to the way in which a person acts to communicate gender within a given culture, for example in terms of clothing, communication patterns, and interest. A person\'s gender expressions may not be consistent with socially prescribed gender roles and may or may not reflect his or her gender identity'
    },
]

print("\nCreating Prohibited Acts...")
for idx, incident in enumerate(prohibited_acts, 1):
    IncidentType.objects.create(**incident)
    print(f"  {idx}. {incident['name']}")

print("\nCreating Other School Policies...")
for idx, incident in enumerate(school_policies, 1):
    IncidentType.objects.create(**incident)
    print(f"  {idx}. {incident['name']}")

print(f"\n✅ Successfully created {len(prohibited_acts)} Prohibited Acts and {len(school_policies)} Other School Policies")
print(f"Total: {len(prohibited_acts) + len(school_policies)} incident types")
