import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blood_bank.models import DonorProfile, BloodRequest

class Command(BaseCommand):
    help = 'Seeds database with initial superuser, donors, and blood requests.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # Create Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@bloodbank.org',
                'first_name': 'System',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        # Sample Donors Data
        donors_data = [
            {
                'username': 'rahim_a',
                'first_name': 'Rahim',
                'last_name': 'Ahmed',
                'email': 'rahim@example.com',
                'blood_group': 'O+',
                'phone': '01711223344',
                'location': 'Feni',
                'date_of_birth': datetime.date(1995, 4, 12),
                'last_donation_date': datetime.date(2026, 6, 15),
                'availability': 'Available',
                'description': 'Regular blood donor. Available on weekends in Feni district area.'
            },
            {
                'username': 'tanvir_h',
                'first_name': 'Tanvir',
                'last_name': 'Hassan',
                'email': 'tanvir@example.com',
                'blood_group': 'A+',
                'phone': '01899887766',
                'location': 'Dhaka',
                'date_of_birth': datetime.date(1998, 9, 25),
                'last_donation_date': datetime.date(2026, 3, 10),
                'availability': 'Available',
                'description': 'Universal plasma donor. Ready for emergency calls in Dhaka North.'
            },
            {
                'username': 'sultana_r',
                'first_name': 'Sultana',
                'last_name': 'Razia',
                'email': 'sultana@example.com',
                'blood_group': 'B+',
                'phone': '01955443322',
                'location': 'Chittagong',
                'date_of_birth': datetime.date(2000, 1, 15),
                'last_donation_date': datetime.date(2026, 1, 20),
                'availability': 'Not Available',
                'description': 'Donated recently. Available again from October 2026.'
            },
            {
                'username': 'kamal_u',
                'first_name': 'Kamal',
                'last_name': 'Uddin',
                'email': 'kamal@example.com',
                'blood_group': 'AB+',
                'phone': '01677889900',
                'location': 'Feni',
                'date_of_birth': datetime.date(1992, 11, 5),
                'last_donation_date': datetime.date(2025, 12, 1),
                'availability': 'Available',
                'description': 'Active volunteer donor in Feni Sadar.'
            },
            {
                'username': 'fatema_z',
                'first_name': 'Fatema',
                'last_name': 'Zohra',
                'email': 'fatema@example.com',
                'blood_group': 'O-',
                'phone': '01511224466',
                'location': 'Sylhet',
                'date_of_birth': datetime.date(1997, 7, 19),
                'last_donation_date': None,
                'availability': 'Available',
                'description': 'Universal negative donor. First-time volunteer ready for urgent requests.'
            }
        ]

        created_users = []
        for d in donors_data:
            user, u_created = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'email': d['email'],
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                }
            )
            if u_created:
                user.set_password('donor123')
                user.save()
            created_users.append(user)

            DonorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'blood_group': d['blood_group'],
                    'phone': d['phone'],
                    'location': d['location'],
                    'date_of_birth': d['date_of_birth'],
                    'last_donation_date': d['last_donation_date'],
                    'availability': d['availability'],
                    'description': d['description']
                }
            )

        # Sample Blood Requests Data
        requests_data = [
            {
                'requester': created_users[0],
                'patient_name': 'Karim Chowdhury',
                'blood_group': 'O+',
                'hospital_name': 'Feni Modern Hospital',
                'location': 'Feni',
                'required_date': datetime.date(2026, 9, 25),
                'bags_required': 2,
                'contact_number': '01711223344',
                'description': 'Urgent requirement for bypass surgery. Please contact immediately.',
                'status': 'Pending'
            },
            {
                'requester': created_users[1],
                'patient_name': 'Nasreen Begum',
                'blood_group': 'A+',
                'hospital_name': 'Square Hospital',
                'location': 'Dhaka',
                'required_date': datetime.date(2026, 9, 20),
                'bags_required': 3,
                'contact_number': '01899887766',
                'description': 'Dengue fever treatment, low blood platelets.',
                'status': 'Pending'
            },
            {
                'requester': created_users[2],
                'patient_name': 'Jahanara Khatun',
                'blood_group': 'B+',
                'hospital_name': 'Chittagong Medical College Hospital',
                'location': 'Chittagong',
                'required_date': datetime.date(2026, 9, 15),
                'bags_required': 1,
                'contact_number': '01955443322',
                'description': 'Maternity emergency delivery.',
                'status': 'Fulfilled'
            },
            {
                'requester': created_users[3],
                'patient_name': 'Shafiqul Islam',
                'blood_group': 'O-',
                'hospital_name': 'Feni District General Hospital',
                'location': 'Feni',
                'required_date': datetime.date(2026, 9, 28),
                'bags_required': 2,
                'contact_number': '01677889900',
                'description': 'Accident trauma patient needing rare O- blood.',
                'status': 'Pending'
            }
        ]

        for req in requests_data:
            BloodRequest.objects.get_or_create(
                patient_name=req['patient_name'],
                hospital_name=req['hospital_name'],
                defaults=req
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
