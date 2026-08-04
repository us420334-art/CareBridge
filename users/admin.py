from django.contrib import admin

from .models import (
    UserProfile,
    CareRepresentativeRequest,
    CareRepresentativeConnection,
    CaregiverAssignment,
    VolunteerAssignment,
)


admin.site.register(UserProfile)
admin.site.register(CareRepresentativeRequest)
admin.site.register(CareRepresentativeConnection)


@admin.register(CaregiverAssignment)
class CaregiverAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "caregiver",
        "assigned_by",
        "assigned_at",
    )


@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "volunteer",
        "assigned_by",
        "assigned_at",
    )