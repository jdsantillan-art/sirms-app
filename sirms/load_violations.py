"""
Load all Prohibited Acts and Other School Policies into the database
Run this after setup_initial_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentType, LegalReference

def create_legal_references():
    """Create all legal reference documents"""
    references = [
        {
            'title': 'DepEd Child Protection Policy',
            'reference_number': 'DepEd Order (DO) 40, s.2012',
            'description': 'Child Protection Policy'
        },
        {
            'title': 'Comprehensive Dangerous Drugs Act',
            'reference_number': 'RA 9165',
            'description': 'Comprehensive Dangerous Drugs Act of 2002'
        },
        {
            'title': 'Direct Assault',
            'reference_number': 'RPC Art. 148',
            'description': 'Direct Assault in relation to Art. 152'
        },
        {
            'title': 'Commonwealth Act on Persons in Authority',
            'reference_number': 'Commonwealth Act 578',
            'description': 'Teachers/personnel as persons in authority'
        },
        {
            'title': 'Theft',
            'reference_number': 'RPC Art. 308-310',
            'description': 'Theft provisions'
        },
        {
            'title': 'Falsification of Documents',
            'reference_number': 'RPC Art. 171-172',
            'description': 'Falsification of documents'
        },
        {
            'title': 'Prohibition of Fraternities/Sororities',
            'reference_number': 'DO 7, s.2006',
            'description': 'Prohibition of fraternities/sororities in elementary & secondary schools'
        },
        {
            'title': 'Robbery and Estafa',
            'reference_number': 'RPC Art. 293-296, 315',
            'description': 'Robbery with violence/intimidation and Estafa/Swindling'
        },
        {
            'title': 'Anti-Bullying Act',
            'reference_number': 'RA 10627',
            'description': 'Anti-Bullying Act of 2013'
        },
        {
            'title': 'IRR of Anti-Bullying Act',
            'reference_number': 'DO 55, s.2013',
            'description': 'Implementing Rules and Regulations of RA 10627'
        },
        {
            'title': 'Physical Injuries',
            'reference_number': 'RPC Art. 262-266',
            'description': 'Physical Injuries provisions'
        },
        {
            'title': 'Malicious Mischief',
            'reference_number': 'RPC Art. 327',
            'description': 'Malicious Mischief / Vandalism'
        },
        {
            'title': 'Ecological Solid Waste Management Act',
            'reference_number': 'RA 9003',
            'description': 'Ecological Solid Waste Management Act'
        },
        {
            'title': 'Tobacco Regulation Act',
            'reference_number': 'RA 9211',
            'description': 'Tobacco Regulation Act'
        },
        {
            'title': 'Smoke-Free Environments',
            'reference_number': 'EO 26 (2017)',
            'description': 'Smoke-Free Environments Executive Order'
        },
        {
            'title': 'Vape Law',
            'reference_number': 'RA 11900',
            'description': 'Vape Law, restricts sales/use by minors & in schools'
        },
        {
            'title': 'Illegal Gambling',
            'reference_number': 'PD 1602',
            'description': 'Illegal gambling penalties'
        },
        {
            'title': 'Obscenity Laws',
            'reference_number': 'PD 969 / PD 960',
            'description': 'Obscenity Laws'
        },
        {
            'title': 'Child Protection - Pornography',
            'reference_number': 'RA 7610',
            'description': 'Special Protection of Children Against Abuse, Exploitation and Discrimination'
        },
        {
            'title': 'Regulation of Firecrackers',
            'reference_number': 'RA 7183',
            'description': 'Regulation of Firecrackers and Other Pyrotechnic Devices'
        },
        {
            'title': 'Student Discipline Guidelines',
            'reference_number': 'DO 32, s.2003',
            'description': 'Student discipline guidelines including uniform compliance'
        },
        {
            'title': 'Classroom Assessment',
            'reference_number': 'DO 8, s.2015',
            'description': 'Classroom Assessment including attendance expectations'
        },
        {
            'title': 'Physical Hygiene and School Decorum',
            'reference_number': 'DepEd Order No. 46, s. 2008',
            'description': 'Promoting physical hygiene and proper school decorum'
        },
        {
            'title': 'Gender-Responsive Basic Education Policy',
            'reference_number': 'DepEd Order No. 32, s. 2017',
            'description': 'Gender-Responsive Basic Education Policy'
        },
    ]
    
    created_refs = {}
    for ref_data in references:
        ref, created = LegalReference.objects.get_or_create(
            reference_number=ref_data['reference_number'],
            defaults={
                'title': ref_data['title'],
                'description': ref_data['description']
            }
        )
        created_refs[ref_data['reference_number']] = ref
        if created:
            print(f"✅ Created legal reference: {ref.reference_number}")
    
    return created_refs

def create_prohibited_acts(legal_refs):
    """Create all Prohibited Acts violations"""
    
    prohibited_acts = [
        {
            'name': 'Possession of deadly weapons',
            'description': 'Possession of deadly weapons (e.g., Indian pana, ice pick, pointed comb, knives, improvised weapons)',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Use/peddling/pushing of marijuana or prohibited drugs',
            'description': 'Use of / peddling / pushing of marijuana or any prohibited drugs',
            'severity': 'prohibited',
            'references': ['RA 9165', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Assaulting teacher/school personnel',
            'description': 'Assaulting a teacher or school personnel; participating in unsanctioned strikes/demonstrations',
            'severity': 'prohibited',
            'references': ['RPC Art. 148', 'Commonwealth Act 578', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Theft/shoplifting/stealing',
            'description': 'Theft / shoplifting / stealing (in-campus or off-campus)',
            'severity': 'prohibited',
            'references': ['RPC Art. 308-310']
        },
        {
            'name': 'Forging/tampering of school records',
            'description': 'Forging / tampering of school records; misrepresentation',
            'severity': 'prohibited',
            'references': ['RPC Art. 171-172']
        },
        {
            'name': 'Gross indecency in conduct',
            'description': 'Gross indecency in conduct (PDA; acts of lasciviousness; exhibitionism) or perennial misbehavior',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Fraternity/sorority/gang membership',
            'description': 'Organization/membership in any fraternity, sorority, gang, or any group not sanctioned by the school',
            'severity': 'prohibited',
            'references': ['DO 7, s.2006']
        },
        {
            'name': 'Extortion/swindling',
            'description': 'Extortion / swindling',
            'severity': 'prohibited',
            'references': ['RPC Art. 293-296, 315', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Bullying or peer abuse',
            'description': 'Bullying or peer abuse (Physical, Psychological, Sexual, Emotional, Cyber, Social, Gender-based)',
            'severity': 'prohibited',
            'references': ['RA 10627', 'DO 55, s.2013', 'DepEd Order (DO) 40, s.2012'],
            'bullying_types': ['Physical', 'Psychological', 'Sexual', 'Emotional', 'Cyber', 'Social', 'Gender-based']
        },
        {
            'name': 'Inflicting injury upon another student/physical assault',
            'description': 'Inflicting injury upon another student/physical assault',
            'severity': 'prohibited',
            'references': ['RPC Art. 262-266', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Vandalism/destruction of school property',
            'description': 'Vandalism / intentional destruction of school property',
            'severity': 'prohibited',
            'references': ['RPC Art. 327']
        },
        {
            'name': 'Destruction of nature',
            'description': 'Destruction of nature (plants/trees/animals used for education)',
            'severity': 'prohibited',
            'references': []
        },
        {
            'name': 'Littering/non-observance of waste management',
            'description': 'Littering/scattering pieces of papers/peelings/wrappers/plastics or non-observance of waste/garbage management',
            'severity': 'prohibited',
            'references': ['RA 9003']
        },
        {
            'name': 'Cheating on classwork',
            'description': 'Cheating on classwork',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Intentional spitting on walls and railings',
            'description': 'Intentional spitting on walls and railings of stairs',
            'severity': 'prohibited',
            'references': []
        },
        {
            'name': 'Smoking & vaping',
            'description': 'Smoking & vaping (in-campus & within the 20-meter perimeter radius outside the school)',
            'severity': 'prohibited',
            'references': ['RA 9211', 'EO 26 (2017)', 'RA 11900']
        },
        {
            'name': 'Taking/bringing intoxicating drinks',
            'description': 'Taking and/or bringing any intoxicating drinks on campus or entering the campus under the influence of alcohol',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Any form of gambling',
            'description': 'Any form of gambling',
            'severity': 'prohibited',
            'references': ['PD 1602']
        },
        {
            'name': 'Insinuating trouble or fight',
            'description': 'Insinuating trouble or fight',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Unsafe behavior on school premises',
            'description': 'Sitting on railings or arms of chairs, jumping and/or sliding on stairway railings, hanging on/jumping over windows/storeys',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Making unnecessary noise',
            'description': 'Shouting or making unnecessary noise while passing along lobbies or corridors',
            'severity': 'prohibited',
            'references': []
        },
        {
            'name': 'Making derogatory statements',
            'description': 'Making any derogatory statements against fellow student, teacher, school personnel, administrators and visitors',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012', 'RA 10627']
        },
        {
            'name': 'Climbing over perimeter fence',
            'description': 'Climbing over perimeter fence in going in or out of the school premises',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Truancy/habitual absenteeism/tardiness',
            'description': 'Truancy/habitual absenteeism/tardiness/cutting or skipping classes',
            'severity': 'prohibited',
            'references': ['DO 8, s.2015']
        },
        {
            'name': 'Unauthorized use of personal gadgets',
            'description': 'Using/playing of personal gadgets while the class is going on (unless allowed by the teacher)',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Possession of pornographic materials',
            'description': 'Possession and/or showing of pornographic materials (printed or digital)',
            'severity': 'prohibited',
            'references': ['PD 969 / PD 960', 'RA 7610', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Bringing/igniting firecrackers',
            'description': 'Bringing and igniting fire crackers in the school premises',
            'severity': 'prohibited',
            'references': ['RA 7183']
        },
        {
            'name': 'School I.D. violation',
            'description': 'Tampering; wearing ID without/or having different picture; wearing different ID or cord; wearing ID with sticker or accessories',
            'severity': 'prohibited',
            'references': ['DO 32, s.2003']
        },
        {
            'name': 'Hurling stones/materials over fence',
            'description': 'Hurling stones and/or any other materials over the perimeter fence',
            'severity': 'prohibited',
            'references': ['RPC Art. 327', 'DepEd Order (DO) 40, s.2012']
        },
        {
            'name': 'Prohibited games/activities',
            'description': 'Playing billiards, online/offline games during school hours; ball games in prohibited areas',
            'severity': 'prohibited',
            'references': ['DepEd Order (DO) 40, s.2012']
        },
    ]
    
    for violation in prohibited_acts:
        # Combine legal references into a single string
        legal_refs_text = "; ".join(violation['references'])
        
        incident_type, created = IncidentType.objects.get_or_create(
            name=violation['name'],
            defaults={
                'description': violation['description'],
                'severity': violation['severity'],
                'legal_references': legal_refs_text
            }
        )
        
        if created:
            print(f"✅ Created prohibited act: {incident_type.name}")

def create_other_school_policies(legal_refs):
    """Create Other School Policies violations"""
    
    other_policies = [
        {
            'name': 'Improper haircut (male students)',
            'description': 'Maintain regular and clean haircuts for male students',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 46, s. 2008']
        },
        {
            'name': 'Excessive makeup/colored nail polish',
            'description': 'Wearing excessive makeup, colored nail polish and nail extensions',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 46, s. 2008']
        },
        {
            'name': 'Bright colored/unnatural hair dyes',
            'description': 'Bright colored or unnatural hair dyes',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 46, s. 2008']
        },
        {
            'name': 'Wearing tattoos/unauthorized piercings',
            'description': 'Wearing tattoos, earring (male student), multiple earrings (female student), unnecessary visible body piercing accessories',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 46, s. 2008']
        },
        {
            'name': 'Wearing caps inside classroom',
            'description': 'Wearing caps inside the classroom',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 46, s. 2008']
        },
        {
            'name': 'LGBTQA+ Non-compliance with uniform/hairstyle',
            'description': 'LGBTQA+ Non-compliance with the prescribed school uniform and hairstyle (Gender expression considerations)',
            'severity': 'school_policy',
            'references': ['DepEd Order No. 32, s. 2017']
        },
    ]
    
    for violation in other_policies:
        # Combine legal references into a single string
        legal_refs_text = "; ".join(violation['references'])
        
        incident_type, created = IncidentType.objects.get_or_create(
            name=violation['name'],
            defaults={
                'description': violation['description'],
                'severity': violation['severity'],
                'legal_references': legal_refs_text
            }
        )
        
        if created:
            print(f"✅ Created other school policy: {incident_type.name}")

def main():
    print("\n" + "=" * 80)
    print("🏫 LOADING ALL VIOLATIONS AND SCHOOL POLICIES")
    print("=" * 80 + "\n")
    
    print("📚 Step 1: Creating Legal References...")
    print("-" * 80)
    legal_refs = create_legal_references()
    
    print("\n🚫 Step 2: Creating Prohibited Acts...")
    print("-" * 80)
    create_prohibited_acts(legal_refs)
    
    print("\n📋 Step 3: Creating Other School Policies...")
    print("-" * 80)
    create_other_school_policies(legal_refs)
    
    print("\n" + "=" * 80)
    print("✅ ALL VIOLATIONS AND POLICIES LOADED SUCCESSFULLY!")
    print("=" * 80)
    
    # Summary
    prohibited_count = IncidentType.objects.filter(severity='prohibited').count()
    osp_count = IncidentType.objects.filter(severity='school_policy').count()
    
    print(f"\n📊 Summary:")
    print(f"   • Prohibited Acts: {prohibited_count}")
    print(f"   • Other School Policies: {osp_count}")
    print(f"   • Legal References: {LegalReference.objects.count()}")
    print(f"   • Total Violations: {IncidentType.objects.count()}")
    print("\n")

if __name__ == '__main__':
    main()
