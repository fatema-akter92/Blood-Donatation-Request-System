import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import DonorProfile, BloodRequest, BLOOD_GROUP_CHOICES, AVAILABILITY_CHOICES, REQUEST_STATUS_CHOICES

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = [
            'blood_group', 'phone', 'location', 'date_of_birth',
            'last_donation_date', 'availability', 'profile_picture', 'description'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Feni, Dhaka, Chittagong'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 01700000000'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself or donation preferences...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[\d\s\-]{7,18}$', phone):
            raise forms.ValidationError("Please enter a valid phone number (digits, spaces, dashes allowed).")
        return phone

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'blood_group', 'hospital_name', 'location',
            'required_date', 'bags_required', 'contact_number', 'description', 'status'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Full Name'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital / Medical Center Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Area'}),
            'required_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bags_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone Number'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason or additional urgency details...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_bags_required(self):
        bags = self.cleaned_data.get('bags_required')
        if bags is None or bags <= 0:
            raise forms.ValidationError("Number of bags must be a positive integer greater than zero.")
        return bags

    def clean_contact_number(self):
        phone = self.cleaned_data.get('contact_number')
        if not re.match(r'^\+?[\d\s\-]{7,18}$', phone):
            raise forms.ValidationError("Please enter a valid contact phone number.")
        return phone

    def clean_required_date(self):
        req_date = self.cleaned_data.get('required_date')
        if req_date and req_date < timezone.now().date():
            raise forms.ValidationError("Required date cannot be in the past.")
        return req_date

class DonorSearchForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'All Blood Groups')] + BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search Location (e.g. Feni)'})
    )
    availability = forms.ChoiceField(
        choices=[('', 'All Status')] + AVAILABILITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RequestFilterForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'All Blood Groups')] + BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + REQUEST_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
