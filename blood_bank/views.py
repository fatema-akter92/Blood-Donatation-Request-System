from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import DonorProfile, BloodRequest
from .forms import (
    UserRegisterForm, UserUpdateForm, DonorProfileForm,
    BloodRequestForm, DonorSearchForm, RequestFilterForm
)

def home_view(request):
    total_donors = DonorProfile.objects.count()
    available_donors = DonorProfile.objects.filter(availability='Available').count()
    active_requests = BloodRequest.objects.filter(status='Pending').count()
    fulfilled_requests = BloodRequest.objects.filter(status='Fulfilled').count()
    
    recent_requests = BloodRequest.objects.order_by('-created_at')[:5]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'active_requests': active_requests,
        'fulfilled_requests': fulfilled_requests,
        'recent_requests': recent_requests,
    }
    return render(request, 'blood_bank/home.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.get_full_name() or user.username}!")
            return redirect('profile_edit')
        else:
            messages.error(request, "Registration failed. Please fix the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = getattr(request.user, 'donor_profile', None)
    user_requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    context = {
        'profile': profile,
        'user_requests': user_requests,
    }
    return render(request, 'blood_bank/profile.html', context)

@login_required
def profile_edit_view(request):
    profile, created = DonorProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = DonorProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your donor profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = DonorProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_new': created,
    }
    return render(request, 'blood_bank/profile_edit.html', context)

def donor_list_view(request):
    form = DonorSearchForm(request.GET or None)
    donors = DonorProfile.objects.select_related('user').all().order_by('-updated_at')

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        availability = form.cleaned_data.get('availability')

        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if location:
            donors = donors.filter(location__icontains=location)
        if availability:
            donors = donors.filter(availability=availability)

    paginator = Paginator(donors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_count': donors.count(),
    }
    return render(request, 'blood_bank/donor_list.html', context)

def donor_detail_view(request, pk):
    donor = get_object_or_404(DonorProfile.objects.select_related('user'), pk=pk)
    context = {'donor': donor}
    return render(request, 'blood_bank/donor_detail.html', context)

def request_list_view(request):
    form = RequestFilterForm(request.GET or None)
    blood_requests = BloodRequest.objects.select_related('requester').all().order_by('-created_at')

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        status = form.cleaned_data.get('status')

        if blood_group:
            blood_requests = blood_requests.filter(blood_group=blood_group)
        if location:
            blood_requests = blood_requests.filter(location__icontains=location)
        if status:
            blood_requests = blood_requests.filter(status=status)

    paginator = Paginator(blood_requests, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_count': blood_requests.count(),
    }
    return render(request, 'blood_bank/request_list.html', context)

def request_detail_view(request, pk):
    blood_request = get_object_or_404(BloodRequest.objects.select_related('requester'), pk=pk)
    context = {'req': blood_request}
    return render(request, 'blood_bank/request_detail.html', context)

@login_required
def request_create_view(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_req = form.save(commit=False)
            blood_req.requester = request.user
            blood_req.save()
            messages.success(request, "Blood request submitted successfully!")
            return redirect('request_detail', pk=blood_req.pk)
        else:
            messages.error(request, "Failed to submit request. Please check the inputs.")
    else:
        form = BloodRequestForm()
    return render(request, 'blood_bank/request_form.html', {'form': form, 'title': 'Create Blood Request'})

@login_required
def request_edit_view(request, pk):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if blood_req.requester != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to edit this request.")
        return redirect('request_detail', pk=pk)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_req)
        if form.is_valid():
            form.save()
            messages.success(request, "Blood request updated successfully!")
            return redirect('request_detail', pk=pk)
        else:
            messages.error(request, "Update failed. Please review the errors below.")
    else:
        form = BloodRequestForm(instance=blood_req)
    return render(request, 'blood_bank/request_form.html', {'form': form, 'title': 'Edit Blood Request', 'req': blood_req})

@login_required
def request_delete_view(request, pk):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if blood_req.requester != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this request.")
        return redirect('request_detail', pk=pk)

    if request.method == 'POST':
        blood_req.delete()
        messages.success(request, "Blood request has been deleted successfully.")
        return redirect('my_requests')
    return render(request, 'blood_bank/request_confirm_delete.html', {'req': blood_req})

@login_required
def my_requests_view(request):
    requests_list = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'blood_bank/my_requests.html', {'requests': requests_list})

@login_required
def update_request_status_view(request, pk, status):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if blood_req.requester != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to update this status.")
        return redirect('request_detail', pk=pk)

    if status in ['Pending', 'Fulfilled', 'Cancelled']:
        blood_req.status = status
        blood_req.save()
        messages.success(request, f"Status updated to '{status}'.")
    return redirect('request_detail', pk=pk)
