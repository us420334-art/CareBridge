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

    emergency_contact_email = models.EmailField(
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

class RepresentedPerson(models.Model):

    PERSON_TYPE_CHOICES = [
        ('Elderly Person', 'Elderly Person'),
        ('Person with Mobility Impairment', 'Person with Mobility Impairment'),
        ('Person with Hearing Impairment', 'Person with Hearing Impairment'),
    ]

    RELATIONSHIP_CHOICES = [
        ('Parent', 'Parent'),
        ('Child', 'Child'),
        ('Spouse', 'Spouse'),
        ('Sibling', 'Sibling'),
        ('Relative', 'Relative'),
        ('Guardian', 'Guardian'),
        ('Friend', 'Friend'),
        ('Other', 'Other'),
    ]

    care_representative = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='represented_person'
    )

    full_name = models.CharField(
        max_length=100
    )

    age = models.PositiveIntegerField()

    person_type = models.CharField(
        max_length=50,
        choices=PERSON_TYPE_CHOICES
    )

    relationship = models.CharField(
        max_length=30,
        choices=RELATIONSHIP_CHOICES
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    blood_group = models.CharField(
        max_length=10,
        blank=True
    )

    medical_conditions = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.full_name} - represented by {self.care_representative.username}"


class DirectCaregiverBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Emergency', 'Emergency'),
    ]

    SERVICE_CHOICES = [
    ('Home Support', 'Home Support'),
    ('Hospital Assistance', 'Hospital Assistance'),
    ('Medication Support', 'Medication Support'),
    ('Health & Wellness Support', 'Health & Wellness Support'),
    ('Post-Hospital Care', 'Post-Hospital Care'),
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

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        blank=True,
        default=''
    )

    address = models.TextField(
        blank=True,
        default=''
    )

    booking_date = models.DateField(
        null=True,
        blank=True
    )

    booking_time = models.TimeField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    description = models.TextField(
        blank=True,
        default=''
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

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Emergency', 'Emergency'),
    ]

    SERVICE_CHOICES = [
        ('Shopping Assistance', 'Shopping Assistance'),
        ('Bank Assistance', 'Bank Assistance'),
        ('Transport Assistance', 'Transport Assistance'),
        ('Hospital Accompaniment', 'Hospital Accompaniment'),
        ('General Support', 'General Support'),
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

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        blank=True,
        default=''
    )

    address = models.TextField(
        blank=True,
        default=''
    )

    booking_date = models.DateField(
        null=True,
        blank=True
    )

    booking_time = models.TimeField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    description = models.TextField(
        blank=True,
        default=''
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

    emergency_contact_email = models.EmailField(
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

    
class Feedback(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    SERVICE_CHOICES = [
        ('Caregiver', 'Caregiver'),
        ('Volunteer', 'Volunteer'),
        ('Service Request', 'Service Request'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        default='Other'
    )

    # The caregiver or volunteer being reviewed
    service_provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_feedbacks',
        null=True,
        blank=True
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.service_provider:
            return f"{self.user.username} → {self.service_provider.username} - {self.rating} Stars"

        return f"{self.user.username} - {self.rating} Stars"

class Notification(models.Model):

    NOTIFICATION_TYPES = [
    ('Booking', 'Booking'),
    ('Service', 'Service'),
    ('Medicine', 'Medicine'),
    ('SOS', 'SOS'),
    ('Feedback', 'Feedback'),
    ('System', 'System'),
]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"