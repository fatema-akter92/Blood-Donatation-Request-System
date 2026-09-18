from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # User Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    
    # Donor URLs
    path('donors/', views.donor_list_view, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail_view, name='donor_detail'),
    
    # Blood Request URLs
    path('requests/', views.request_list_view, name='request_list'),
    path('requests/create/', views.request_create_view, name='request_create'),
    path('requests/my/', views.my_requests_view, name='my_requests'),
    path('requests/<int:pk>/', views.request_detail_view, name='request_detail'),
    path('requests/<int:pk>/edit/', views.request_edit_view, name='request_edit'),
    path('requests/<int:pk>/delete/', views.request_delete_view, name='request_delete'),
    path('requests/<int:pk>/status/<str:status>/', views.update_request_status_view, name='update_request_status'),
]
