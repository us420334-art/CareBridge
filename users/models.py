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


class DirectCaregiverBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
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
        ('Rejected', 'Rejected'),
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

class ServiceRequest(models.Model):

    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("High", "High"),
        ("Emergency", "Emergency"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Assigned", "Assigned"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    services = models.TextField()

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.priority}"

class MedicineReminder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Taken', 'Taken'),
        ('Missed', 'Missed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medicine_reminders'
    )

    medicine_name = models.CharField(
        max_length=100
    )

    dosage = models.CharField(
        max_length=100
    )

    reminder_time = models.TimeField()

    start_date = models.DateField()

    instructions = models.TextField(
        blank=True
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
        return f"{self.user.username} - {self.medicine_name}"

class EmergencySOS(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emergency_sos_alerts'
    )

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True
    )

    triggered_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default='Activated'
    )

    def __str__(self):
        return f"{self.user.username} - Emergency SOS - {self.status}"