from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
path(
    'admin-users/',
    views.admin_users,
    name='admin_users'
),
path(
    'admin-users/edit/<int:user_id>/',
    views.admin_edit_user,
    name='admin_edit_user'
),

path(
    'admin-users/toggle/<int:user_id>/',
    views.admin_toggle_user,
    name='admin_toggle_user'
),

path(
    'admin-users/delete/<int:user_id>/',
    views.admin_delete_user,
    name='admin_delete_user'
),
path(
    'admin-caregivers/',
    views.admin_caregivers,
    name='admin_caregivers'
),
path(
    'admin-volunteers/',
    views.admin_volunteers,
    name='admin_volunteers'
),
path(
    'admin-care-representatives/',
    views.admin_care_representatives,
    name='admin_care_representatives'
),
path(
    'admin-caregiver-bookings/',
    views.admin_caregiver_bookings,
    name='admin_caregiver_bookings'
),
path(
    'admin-volunteer-bookings/',
    views.admin_volunteer_bookings,
    name='admin_volunteer_bookings'
),
path(
    'admin-sos/',
    views.admin_sos,
    name='admin_sos'
),
path(
    'admin-feedback/',
    views.admin_feedback,
    name='admin_feedback'
),
path(
    'admin-notifications/',
    views.admin_notifications,
    name='admin_notifications'
),
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
    name='complete_caregiver_booking'
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
    'volunteer-booking/<int:booking_id>/<str:status>/',
    views.update_volunteer_booking_status,
    name='update_volunteer_booking_status'
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
    # Feedback

path(
    'feedback/',
    views.feedback,
    name='feedback'
),

path(
    'delete-feedback/<int:feedback_id>/',
    views.delete_feedback,
    name='delete_feedback'
),
path(
    'notifications/',
    views.notifications,
    name='notifications'
),

path(
    'notifications/read/<int:notification_id>/',
    views.mark_notification_read,
    name='mark_notification_read'
),
]