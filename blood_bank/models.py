from django.db import models
from django.contrib.auth.models import User

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

AVAILABILITY_CHOICES = [
    ('Available', 'Available'),
    ('Not Available', 'Not Available'),
]

REQUEST_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Fulfilled', 'Fulfilled'),
    ('Cancelled', 'Cancelled'),
]

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.blood_group}) - {self.location}"

class BloodRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    hospital_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    required_date = models.DateField()
    bags_required = models.PositiveIntegerField(default=1)
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request for {self.patient_name} ({self.blood_group}) at {self.hospital_name}"
