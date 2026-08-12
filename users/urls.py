from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/', views.profile, name='profile'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path(
    'emergency-sos/',
    views.emergency_sos,
    name='emergency_sos'
),

    path(
    'delete-emergency-sos/<int:sos_id>/',
    views.delete_emergency_sos,
    name='delete_emergency_sos'
),

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

    # Medicine Alerts
    path(
        'medicine-alerts/',
        views.medicine_alerts,
        name='medicine_alerts'
    ),
    path(
    'medicine-alerts-status/',
    views.medicine_alerts_status,
    name='medicine_alerts_status'
   ),

    path(
        'mark-medicine-taken/<int:reminder_id>/',
        views.mark_medicine_taken,
        name='mark_medicine_taken'
    ),

    path(
        'delete-medicine-reminder/<int:reminder_id>/',
        views.delete_medicine_reminder,
        name='delete_medicine_reminder'
    ),

    path(
        'edit-medicine-reminder/<int:reminder_id>/',
        views.edit_medicine_reminder,
        name='edit_medicine_reminder'
    ),
]