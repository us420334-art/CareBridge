from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('Elderly Person', 'Elderly Person'),
        ('Person with Mobility Impairment', 'Person with Mobility Impairment'),
        ('Person with Hearing Impairment', 'Person with Hearing Impairment'),
        ('Care Representative', 'Care Representative'),
        ('Caregiver', 'Caregiver'),
        ('Volunteer', 'Volunteer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True
    )

    blood_group = models.CharField(
        max_length=10,
        blank=True
    )

    medical_conditions = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username



class CareRepresentativeRequest(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]


    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='care_requests_sent'
    )


    representative = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='care_requests_received'
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.requester.username} → {self.representative.username} ({self.status})"




class CareRepresentativeConnection(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='connected_users'
    )

    representative = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='connected_representatives'
    )

    connected_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} ↔ {self.representative.username}"


class CaregiverAssignment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='caregiver_assignment'
    )

    caregiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_caregiver'
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='caregiver_assigned_by'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} → {self.caregiver.username} ({self.status})"


class VolunteerAssignment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer_assignment'
    )

    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_volunteer'
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer_assigned_by'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} → {self.volunteer.username} ({self.status})"
class DirectCaregiverBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='direct_caregiver_bookings'
    )

    caregiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='caregiver_direct_bookings'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} booked {self.caregiver.username}"

class DirectVolunteerBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='direct_volunteer_bookings'
    )

    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer_direct_bookings'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} booked {self.volunteer.username}"