from django.contrib import admin

from .models import (
    UserProfile,
    DirectCaregiverBooking,
    DirectVolunteerBooking,
    ServiceRequest,
)


admin.site.register(UserProfile)
admin.site.register(DirectCaregiverBooking)
admin.site.register(DirectVolunteerBooking)
admin.site.register(ServiceRequest)