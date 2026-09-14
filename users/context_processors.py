from .models import DirectCaregiverBooking, DirectVolunteerBooking,Notification


def booking_status(request):

    if not request.user.is_authenticated:
        return {
            'sidebar_caregiver_booking': None,
            'sidebar_volunteer_booking': None,
        }

    caregiver_booking = DirectCaregiverBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at').first()

    volunteer_booking = DirectVolunteerBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at').first()

    return {
        'sidebar_caregiver_booking': caregiver_booking,
        'sidebar_volunteer_booking': volunteer_booking,
    }
def unread_notifications(request):

    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
    else:
        unread_notifications_count = 0

    return {
        'unread_notifications_count': unread_notifications_count,
    }