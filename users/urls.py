from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/', views.profile, name='profile'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Care Representative module
    path('care-representatives/',views.care_representatives,name='care_representatives' ),
    
    path('care-rep-dashboard/',views.care_rep_dashboard,name='care_rep_dashboard'),

    path('accept-request/<int:request_id>/',views.accept_request,name='accept_request'),

    path('reject-request/<int:request_id>/',views.reject_request,name='reject_request'),

    path('assign-user/<int:connection_id>/',views.assign_user,name='assign_user'),

    path('book-caregiver/',views.book_caregiver,name='book_caregiver'),

    path('book-caregiver/<int:caregiver_id>/',views.confirm_caregiver_booking,name='confirm_caregiver_booking'),

    path('my-bookings/',views.my_bookings,name='my_bookings'),

    path(
    'caregiver-dashboard/',
    views.caregiver_dashboard,
    name='caregiver_dashboard'
),

path(
    'accept-caregiver-booking/<int:booking_id>/',
    views.accept_caregiver_booking,
    name='accept_caregiver_booking'
),

path('reject-caregiver-booking/<int:booking_id>/',views.reject_caregiver_booking,name='reject_caregiver_booking'),

    path('logout/', views.user_logout, name='logout'),

]