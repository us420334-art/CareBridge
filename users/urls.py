from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/', views.profile, name='profile'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Care Representative
    path(
        'care-rep-dashboard/',
        views.care_rep_dashboard,
        name='care_rep_dashboard'
    ),

    # Caregiver
    path(
        'book-caregiver/',
        views.book_caregiver,
        name='book_caregiver'
    ),

    path(
        'book-caregiver/<int:caregiver_id>/',
        views.confirm_caregiver_booking,
        name='confirm_caregiver_booking'
    ),

    path(
        'my-bookings/',
        views.my_bookings,
        name='my_bookings'
    ),

    path(
        'caregiver-dashboard/',
        views.caregiver_dashboard,
        name='caregiver_dashboard'
    ),

    path(
        'caregiver-schedule/',
        views.caregiver_schedule,
        name='caregiver_schedule'
    ),

    path(
        'accept-caregiver-booking/<int:booking_id>/',
        views.accept_caregiver_booking,
        name='accept_caregiver_booking'
    ),

    path(
        'reject-caregiver-booking/<int:booking_id>/',
        views.reject_caregiver_booking,
        name='reject_caregiver_booking'
    ),

    path(
        'complete-caregiver-service/<int:booking_id>/',
        views.complete_caregiver_service,
        name='complete_caregiver_service'
    ),

    path(
        'completed-services/',
        views.completed_services,
        name='completed_services'
    ),

    # Service Requests
    path(
        'service-requests/',
        views.service_requests,
        name='service_requests'
    ),

    path(
        'service-choice/',
        views.service_choice,
        name='service_choice'
    ),

    path(
        'select-helper/',
        views.select_helper,
        name='select_helper'
    ),

    path(
        'direct-service-request/',
        views.direct_service_request,
        name='direct_service_request'
    ),

    path(
        'request-submitted/',
        views.request_submitted,
        name='request_submitted'
    ),

    # Volunteer
    path(
        'book-volunteer/',
        views.book_volunteer,
        name='book_volunteer'
    ),

    path(
        'book-volunteer/<int:volunteer_id>/',
        views.confirm_volunteer_booking,
        name='confirm_volunteer_booking'
    ),

    path(
        'volunteer-dashboard/',
        views.volunteer_dashboard,
        name='volunteer_dashboard'
    ),

    path(
        'accept-volunteer-booking/<int:booking_id>/',
        views.accept_volunteer_booking,
        name='accept_volunteer_booking'
    ),

    path(
        'reject-volunteer-booking/<int:booking_id>/',
        views.reject_volunteer_booking,
        name='reject_volunteer_booking'
    ),

    # Logout
    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
]