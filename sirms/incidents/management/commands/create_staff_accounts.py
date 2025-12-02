"""
Django management command to create staff accounts
This can be run automatically during deployment or manually
"""
from django.core.management.base import BaseCommand
from incidents.models import CustomUser


class Command(BaseCommand):
    help = 'Creates staff accounts for DMLMHS SIRMS (Guidance, DO, ESP Teachers)'

    def handle(self, *args, **kwargs):
        accounts_created = []
        accounts_existing = []
        
        # 1. Create Guidance Counselor Account
        guidance_email = 'dmlmhs.guidance@gmail.com'
        if not CustomUser.objects.filter(email=guidance_email).exists():
            guidance = CustomUser.objects.create_user(
                username='guidance_counselor',
                email=guidance_email,
                password='dmlmhsguidance000',
                first_name='Guidance',
                last_name='Counselor',
                role='counselor'
            )
            accounts_created.append(f"✅ Guidance Counselor: {guidance_email}")
            self.stdout.write(self.style.SUCCESS(f'Created Guidance Counselor: {guidance_email}'))
        else:
            accounts_existing.append(f"⚠️  Guidance Counselor already exists: {guidance_email}")
            self.stdout.write(self.style.WARNING(f'Guidance Counselor already exists: {guidance_email}'))
        
        # 2. Create Discipline Officer Account
        do_email = 'dmlmhs.do@gmail.com'
        if not CustomUser.objects.filter(email=do_email).exists():
            do_user = CustomUser.objects.create_user(
                username='discipline_officer',
                email=do_email,
                password='dmlmhsdo000',
                first_name='Discipline',
                last_name='Officer',
                role='do'
            )
            accounts_created.append(f"✅ Discipline Officer: {do_email}")
            self.stdout.write(self.style.SUCCESS(f'Created Discipline Officer: {do_email}'))
        else:
            accounts_existing.append(f"⚠️  Discipline Officer already exists: {do_email}")
            self.stdout.write(self.style.WARNING(f'Discipline Officer already exists: {do_email}'))
        
        # 3. Create 5 ESP Teacher Accounts
        esp_teachers = [
            {'last_name': 'Garcia', 'first_name': 'Maria', 'middle_name': 'Santos'},
            {'last_name': 'Reyes', 'first_name': 'Juan', 'middle_name': 'Dela Cruz'},
            {'last_name': 'Santos', 'first_name': 'Ana', 'middle_name': 'Lopez'},
            {'last_name': 'Cruz', 'first_name': 'Pedro', 'middle_name': 'Ramos'},
            {'last_name': 'Lopez', 'first_name': 'Rosa', 'middle_name': 'Mendoza'},
        ]
        
        for teacher in esp_teachers:
            email = f"{teacher['last_name'].lower()}.espteacher@gmail.com"
            username = f"{teacher['last_name'].lower()}_esp"
            
            if not CustomUser.objects.filter(email=email).exists():
                esp_user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='dmlmhsesp000',
                    first_name=teacher['first_name'],
                    middle_name=teacher['middle_name'],
                    last_name=teacher['last_name'],
                    role='esp_teacher'
                )
                accounts_created.append(f"✅ ESP Teacher: {email}")
                self.stdout.write(self.style.SUCCESS(f'Created ESP Teacher: {email} ({teacher["first_name"]} {teacher["last_name"]})'))
            else:
                accounts_existing.append(f"⚠️  ESP Teacher already exists: {email}")
                self.stdout.write(self.style.WARNING(f'ESP Teacher already exists: {email}'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('STAFF ACCOUNTS CREATION SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'\nAccounts created: {len(accounts_created)}'))
        self.stdout.write(self.style.WARNING(f'Accounts already existing: {len(accounts_existing)}'))
        
        if accounts_created:
            self.stdout.write(self.style.SUCCESS('\n✅ NEW ACCOUNTS:'))
            for account in accounts_created:
                self.stdout.write(f'   {account}')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('CREDENTIALS:'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write('\n📧 Guidance: dmlmhs.guidance@gmail.com / dmlmhsguidance000')
        self.stdout.write('👮 DO: dmlmhs.do@gmail.com / dmlmhsdo000')
        self.stdout.write('👨‍🏫 ESP Teachers: *.espteacher@gmail.com / dmlmhsesp000')
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
