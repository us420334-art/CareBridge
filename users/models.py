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

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    phone = models.CharField(max_length=15)

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