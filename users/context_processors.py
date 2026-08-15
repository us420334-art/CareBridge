from .models import DirectCaregiverBooking, DirectVolunteerBooking


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