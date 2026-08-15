from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse

from .models import (
    UserProfile,
    DirectCaregiverBooking,
    DirectVolunteerBooking,
    ServiceRequest,
    MedicineReminder,
    EmergencySOS,
     Feedback,
     Notification,
)

def home(request):

    return render(request, 'home.html')


def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role']

        emergency_contact_name = request.POST['emergency_contact_name']
        emergency_contact_phone = request.POST['emergency_contact_phone']

        blood_group = request.POST['blood_group']
        medical_conditions = request.POST['medical_conditions']


        if User.objects.filter(username=username).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Username already exists.'
                }
            )


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            address=address,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            blood_group=blood_group,
            medical_conditions=medical_conditions
        )


        return redirect('/login/')


    return render(request, 'register.html')


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin / Staff user
            if user.is_staff:
                return redirect("admin_dashboard")

            try:

                profile = UserProfile.objects.get(
                    user=user
                )

                if profile.role == "Care Representative":

                    return redirect("care_rep_dashboard")

                elif profile.role == "Caregiver":

                    return redirect("caregiver_dashboard")

                elif profile.role == "Volunteer":

                    return redirect("volunteer_dashboard")

                else:

                    return redirect("dashboard")

            except UserProfile.DoesNotExist:

                return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(
        request,
        "login.html"
    )


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'profile': profile,
        }
    )

def profile(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    return render(
        request,
        'dashboard/profile.html',
        {
            'profile': profile
        }
    )

def edit_profile(request):

    if not request.user.is_authenticated:

        return redirect('/login/')


    profile = UserProfile.objects.get(
        user=request.user
    )


    if request.method == "POST":

        request.user.email = request.POST['email']
        request.user.save()


        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.role = request.POST['role']


        profile.emergency_contact_name = request.POST['emergency_contact_name']
        profile.emergency_contact_phone = request.POST['emergency_contact_phone']


        profile.blood_group = request.POST['blood_group']
        profile.medical_conditions = request.POST['medical_conditions']


        profile.save()


        return redirect('/profile/')


    return render(
        request,
        'dashboard/edit_profile.html',
        {
            'profile': profile
        }
    )

def user_logout(request):

    logout(request)

    return redirect('/')


def care_rep_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.role != "Care Representative":
        return redirect('/dashboard/')

    caregivers = UserProfile.objects.filter(
        role="Caregiver"
    )

    volunteers = UserProfile.objects.filter(
        role="Volunteer"
    )

    return render(
        request,
        "dashboard/care_rep_dashboard.html",
        {
            "profile": profile,
            "caregivers": caregivers,
            "volunteers": volunteers,
        }
    )

def caregiver_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.role != "Caregiver":
        return redirect('/dashboard/')

    bookings = DirectCaregiverBooking.objects.filter(
        caregiver=request.user
    ).order_by('-booked_at')

    return render(
        request,
        "dashboard/caregiver_dashboard.html",
        {
            "profile": profile,
            "bookings": bookings,
        }
    )

def book_caregiver(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    active_booking = DirectCaregiverBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    caregivers = UserProfile.objects.filter(
        role="Caregiver"
    )

    if request.method == "POST":

        caregiver_id = request.POST.get("caregiver_id")
        service = request.POST.get("service")
        address = request.POST.get("address")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        priority = request.POST.get("priority")
        description = request.POST.get("description", "")

        if active_booking:

            messages.warning(
                request,
                "You already have an active caregiver booking."
            )

            return redirect("book_caregiver")

        caregiver = get_object_or_404(
            User,
            id=caregiver_id
        )

        DirectCaregiverBooking.objects.create(
            user=request.user,
            caregiver=caregiver,
            service=service,
            address=address,
            booking_date=booking_date,
            booking_time=booking_time,
            priority=priority,
            description=description,
            status="Pending"
        )

        messages.success(
            request,
            "Caregiver booking request sent successfully."
        )

        return redirect("book_caregiver")

    return render(
        request,
        "dashboard/book_caregiver.html",
        {
            "caregivers": caregivers,
            "profile": profile,
            "active_booking": active_booking,
        }
    )


def confirm_caregiver_booking(request, caregiver_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    # Check whether the user already has an active caregiver booking
    active_booking = DirectCaregiverBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    if active_booking:

        if active_booking.caregiver_id == caregiver_id:

            messages.warning(
                request,
                "You already have an active booking request with this caregiver."
            )

        else:

            messages.warning(
                request,
                "You already have an active caregiver booking. "
                "You can book another caregiver after the current booking "
                "is completed, rejected, or cancelled."
            )

        return redirect('book_caregiver')

    # Get selected caregiver
    caregiver = get_object_or_404(
        User,
        id=caregiver_id
    )

    # Get the logged-in user's profile
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # If the booking form was submitted
    if request.method == "POST":

        service = request.POST.get("service")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        priority = request.POST.get("priority")
        description = request.POST.get("description")

        # Use the user's registered address
        address = profile.address

        # Create the booking
        DirectCaregiverBooking.objects.create(
            user=request.user,
            caregiver=caregiver,
            service=service,
            address=address,
            booking_date=booking_date,
            booking_time=booking_time,
            priority=priority,
            description=description,
            status="Pending"
        )

        messages.success(
            request,
            "Caregiver booking request sent successfully."
        )

        return redirect('book_caregiver')

    # Show booking form
    return render(
        request,
        "dashboard/confirm_caregiver_booking.html",
        {
            "caregiver": caregiver,
            "profile": profile,
        }
    )

def my_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    caregiver_bookings = DirectCaregiverBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at')

    volunteer_bookings = DirectVolunteerBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at')

    # Latest booking status for sidebar
    latest_caregiver_booking = caregiver_bookings.first()
    latest_volunteer_booking = volunteer_bookings.first()

    return render(
        request,
        'dashboard/my_bookings.html',
        {
            'caregiver_bookings': caregiver_bookings,
            'volunteer_bookings': volunteer_bookings,
            'latest_caregiver_booking': latest_caregiver_booking,
            'latest_volunteer_booking': latest_volunteer_booking,
        }
    )

def accept_caregiver_booking(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    booking = get_object_or_404(
        DirectCaregiverBooking,
        id=booking_id,
        caregiver=request.user
    )

    booking.status = "Accepted"
    booking.save()

    create_notification(
        booking.user,
        "Booking",
        "Caregiver Booking Accepted",
        f"Your caregiver booking with {request.user.get_full_name() or request.user.username} has been accepted."
    )

    messages.success(
        request,
        "Booking accepted successfully."
    )

    return redirect('caregiver_dashboard')

def reject_caregiver_booking(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    booking = get_object_or_404(
        DirectCaregiverBooking,
        id=booking_id,
        caregiver=request.user
    )

    booking.status = "Rejected"
    booking.save()

    create_notification(
        booking.user,
        "Booking",
        "Caregiver Booking Rejected",
        f"Your caregiver booking with {request.user.get_full_name() or request.user.username} has been rejected."
    )

    messages.success(
        request,
        "Booking rejected."
    )

    return redirect('caregiver_dashboard')


def service_requests(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == "POST":

        services = request.POST.getlist("services")

        description = request.POST.get("description")

        priority = request.POST.get("priority")

        ServiceRequest.objects.create(

            user=request.user,

            services=", ".join(services),

            description=description,

            priority=priority

        )

        messages.success(
            request,
            "Service request submitted successfully."
        )

        return redirect("service_requests")

    requests = ServiceRequest.objects.filter(
        user=request.user
    ).order_by("-requested_at")

    return render(
        request,
        "dashboard/service_requests.html",
        {
            "requests": requests
        }
    )

def service_choice(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    return render(
        request,
        'dashboard/service_choice.html'
    )

def select_helper(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    mode = request.GET.get(
        "mode",
        "direct"
    )

    if request.method == "POST":

        selected = request.POST.getlist("helper")

        if not selected:

            messages.error(
                request,
                "Please select at least one helper."
            )

            return render(
                request,
                "dashboard/select_helper.html",
                {
                    "mode": mode
                }
            )

        request.session["selected_helpers"] = selected

        request.session["request_mode"] = mode

        return redirect("direct_service_request")

    return render(
        request,
        "dashboard/select_helper.html",
        {
            "mode": mode
        }
    )
def direct_service_request(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    selected_helpers = request.session.get(
        "selected_helpers",
        []
    )

    mode = request.session.get(
        "request_mode",
        "direct"
    )

    if request.method == "POST":

        caregiver_services = request.POST.getlist(
            "caregiver_services"
        )

        volunteer_services = request.POST.getlist(
            "volunteer_services"
        )

        description = request.POST.get(
            "description"
        )

        priority = request.POST.get(
            "priority"
        )

        services = caregiver_services + volunteer_services

        ServiceRequest.objects.create(

            user=request.user,

            services=", ".join(services),

            description=description,

            priority=priority

        )
        request.session["submitted_helpers"] = selected_helpers
        request.session["submitted_mode"] = mode
        messages.success(
            request,
            "Service request submitted successfully."
        )

        return redirect("request_submitted")

    return render(
        request,
        "dashboard/direct_service_request.html",
        {
            "selected_helpers": selected_helpers,
            "mode": mode,
        }
    )
def request_submitted(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    helpers = request.session.get(
        "submitted_helpers",
        []
    )

    mode = request.session.get(
        "submitted_mode",
        "direct"
    )

    return render(
        request,
        "dashboard/request_submitted.html",
        {
            "helpers": helpers,
            "mode": mode,
        }
    )

def book_volunteer(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    active_booking = DirectVolunteerBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    volunteers = UserProfile.objects.filter(
        role="Volunteer"
    )

    if request.method == "POST":

        volunteer_id = request.POST.get("volunteer_id")
        service = request.POST.get("service")
        address = request.POST.get("address")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        priority = request.POST.get("priority")
        description = request.POST.get("description", "")

        if active_booking:

            messages.warning(
                request,
                "You already have an active volunteer booking."
            )

            return redirect("book_volunteer")

        volunteer = get_object_or_404(
            User,
            id=volunteer_id
        )

        DirectVolunteerBooking.objects.create(
            user=request.user,
            volunteer=volunteer,
            service=service,
            address=address,
            booking_date=booking_date,
            booking_time=booking_time,
            priority=priority,
            description=description,
            status="Pending"
        )

        messages.success(
            request,
            "Volunteer booking request sent successfully."
        )

        return redirect("book_volunteer")

    return render(
        request,
        "dashboard/book_volunteer.html",
        {
            "volunteers": volunteers,
            "profile": profile,
            "active_booking": active_booking,
        }
    )


def confirm_volunteer_booking(request, volunteer_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    # Check whether the user already has an active volunteer booking
    active_booking = DirectVolunteerBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    if active_booking:

        if active_booking.volunteer_id == volunteer_id:

            messages.warning(
                request,
                "You already have an active booking request with this volunteer."
            )

        else:

            messages.warning(
                request,
                "You already have an active volunteer booking. "
                "You can book another volunteer after the current booking "
                "is completed, rejected, or cancelled."
            )

        return redirect('book_volunteer')

    # Get selected volunteer
    volunteer = get_object_or_404(
        User,
        id=volunteer_id
    )

    # Get logged-in user's profile
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # =========================
    # FORM SUBMISSION
    # =========================

    if request.method == "POST":

        service = request.POST.get("service")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        priority = request.POST.get("priority")
        description = request.POST.get("description", "")

        # Use registered address
        address = profile.address

        # Create volunteer booking
        booking = DirectVolunteerBooking.objects.create(
            user=request.user,
            volunteer=volunteer,
            service=service,
            address=address,
            booking_date=booking_date,
            booking_time=booking_time,
            priority=priority,
            description=description,
            status="Pending"
        )

        # Notification to volunteer
        create_notification(
            volunteer,
            "Booking",
            "New Volunteer Booking",
            f"You have received a new volunteer booking request "
            f"from {request.user.get_full_name() or request.user.username}."
        )

        messages.success(
            request,
            "Volunteer booking request sent successfully."
        )

        return redirect('book_volunteer')

    # =========================
    # SHOW CONFIRMATION FORM
    # =========================

    return render(
        request,
        "dashboard/confirm_volunteer_booking.html",
        {
            "volunteer": volunteer,
            "profile": profile,
        }
    )


def volunteer_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.role != "Volunteer":
        return redirect('/dashboard/')

    bookings = DirectVolunteerBooking.objects.filter(
        volunteer=request.user
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/volunteer_dashboard.html',
        {
            'profile': profile,
            'bookings': bookings,
        }
    )

def update_volunteer_booking_status(request, booking_id, status):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != "Volunteer":
        return redirect('/dashboard/')

    booking = get_object_or_404(
        DirectVolunteerBooking,
        id=booking_id,
        volunteer=request.user
    )

    # =========================
    # ACCEPT BOOKING
    # =========================

    if status == "Accepted":

        if booking.status == "Pending":

            booking.status = "Accepted"
            booking.save()

            create_notification(
                booking.user,
                "Booking",
                "Volunteer Booking Accepted",
                f"Your volunteer booking with "
                f"{request.user.get_full_name() or request.user.username} "
                f"has been accepted."
            )

            messages.success(
                request,
                "Volunteer booking accepted successfully."
            )


    # =========================
    # REJECT BOOKING
    # =========================

    elif status == "Rejected":

        if booking.status == "Pending":

            booking.status = "Rejected"
            booking.save()

            create_notification(
                booking.user,
                "Booking",
                "Volunteer Booking Rejected",
                f"Your volunteer booking with "
                f"{request.user.get_full_name() or request.user.username} "
                f"has been rejected."
            )

            messages.warning(
                request,
                "Volunteer booking rejected."
            )


    # =========================
    # COMPLETE BOOKING
    # =========================

    elif status == "Completed":

        if booking.status == "Accepted":

            booking.status = "Completed"
            booking.save()

            create_notification(
                booking.user,
                "Booking",
                "Volunteer Service Completed",
                f"Your volunteer service with "
                f"{request.user.get_full_name() or request.user.username} "
                f"has been completed successfully."
            )

            messages.success(
                request,
                "Volunteer service marked as completed."
            )

    return redirect('volunteer_dashboard')


def accept_volunteer_booking(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    booking = get_object_or_404(
        DirectVolunteerBooking,
        id=booking_id,
        volunteer=request.user
    )

    booking.status = "Accepted"
    booking.save()

    # Send notification to the user who made the booking
    create_notification(
        booking.user,
        "Booking",
        "Volunteer Booking Accepted",
        f"Your volunteer booking with {request.user.get_full_name() or request.user.username} has been accepted."
    )

    messages.success(
        request,
        "Volunteer booking accepted successfully."
    )

    return redirect('volunteer_dashboard')

def reject_volunteer_booking(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    booking = get_object_or_404(
        DirectVolunteerBooking,
        id=booking_id,
        volunteer=request.user
    )

    booking.status = "Rejected"
    booking.save()

    # Send notification to the user who made the booking
    create_notification(
        booking.user,
        "Booking",
        "Volunteer Booking Rejected",
        f"Your volunteer booking with {request.user.get_full_name() or request.user.username} has been rejected."
    )

    messages.success(
        request,
        "Volunteer booking rejected."
    )

    return redirect('volunteer_dashboard')


def caregiver_schedule(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(user=request.user)

    if profile.role != "Caregiver":
        return redirect('/dashboard/')

    bookings = DirectCaregiverBooking.objects.filter(
        caregiver=request.user,
        status="Accepted"
    ).order_by('booked_at')

    return render(
        request,
        'dashboard/caregiver_schedule.html',
        {
            'bookings': bookings,
        }
    )



def complete_caregiver_service(request, booking_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    booking = get_object_or_404(
        DirectCaregiverBooking,
        id=booking_id,
        caregiver=request.user
    )

    print("COMPLETE BUTTON CLICKED")
    print("BOOKING:", booking.id)
    print("USER WHO BOOKED:", booking.user.username)
    print("CURRENT STATUS:", booking.status)

    booking.status = "Completed"
    booking.save()

    create_notification(
        booking.user,
        "Booking",
        "Caregiver Service Completed",
        f"Your caregiver service with "
        f"{request.user.get_full_name() or request.user.username} "
        f"has been completed successfully."
    )

    print("COMPLETION NOTIFICATION CREATED FOR:", booking.user.username)

    messages.success(
        request,
        "Service marked as completed successfully."
    )

    return redirect('caregiver_dashboard')


def completed_services(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(user=request.user)

    bookings = DirectCaregiverBooking.objects.filter(
        caregiver=request.user,
        status="Completed"
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/completed_services.html',
        {
            'profile': profile,
            'bookings': bookings,
        }
    )


def medicine_alerts(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == "POST":

        medicine_name = request.POST.get("medicine_name")
        dosage = request.POST.get("dosage")
        reminder_time = request.POST.get("reminder_time")
        start_date = request.POST.get("start_date")
        instructions = request.POST.get("instructions")

        MedicineReminder.objects.create(
            user=request.user,
            medicine_name=medicine_name,
            dosage=dosage,
            reminder_time=reminder_time,
            start_date=start_date,
            instructions=instructions
        )

        messages.success(
            request,
            "Medicine reminder added successfully."
        )

        return redirect("medicine_alerts")

    reminders = MedicineReminder.objects.filter(
        user=request.user
    ).order_by("reminder_time")

    current_date = datetime.now().date()
    current_time = datetime.now().time()

    due_reminders = []

    for reminder in reminders:

        # Medicine is due
        if (
            reminder.status == "Pending"
            and reminder.start_date <= current_date
            and reminder.reminder_time <= current_time
        ):

            due_reminders.append(reminder)

            create_notification(
                request.user,
                "Medicine",
                "Medicine Reminder Due",
                f"Your medicine '{reminder.medicine_name}' is due now. Dosage: {reminder.dosage}."
            )

    return render(
        request,
        "dashboard/medicine_alerts.html",
        {
            "reminders": reminders,
            "due_reminders": due_reminders,
        }
    )


def medicine_alerts_status(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "authenticated": False
        })

    reminders = MedicineReminder.objects.filter(
        user=request.user,
        status="Pending"
    )

    current_date = datetime.now().date()
    current_time = datetime.now().time()

    due_reminders = []

    for reminder in reminders:

        if (
            reminder.start_date <= current_date
            and reminder.reminder_time <= current_time
        ):
            due_reminders.append({
                "id": reminder.id,
                "medicine_name": reminder.medicine_name,
                "dosage": reminder.dosage,
                "instructions": reminder.instructions or ""
            })

    return JsonResponse({
        "authenticated": True,
        "due_reminders": due_reminders
    })


def mark_medicine_taken(request, reminder_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    reminder = get_object_or_404(
        MedicineReminder,
        id=reminder_id,
        user=request.user
    )

    reminder.status = 'Taken'
    reminder.save()

    messages.success(
        request,
        f"{reminder.medicine_name} marked as taken."
    )

    return redirect('medicine_alerts')

def delete_medicine_reminder(request, reminder_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    reminder = get_object_or_404(
        MedicineReminder,
        id=reminder_id,
        user=request.user
    )

    medicine_name = reminder.medicine_name

    reminder.delete()

    messages.success(
        request,
        f"{medicine_name} reminder deleted successfully."
    )

    return redirect('medicine_alerts')

def edit_medicine_reminder(request, reminder_id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    reminder = get_object_or_404(
        MedicineReminder,
        id=reminder_id,
        user=request.user
    )

    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        dosage = request.POST.get('dosage')
        reminder_time = request.POST.get('reminder_time')
        start_date = request.POST.get('start_date')
        instructions = request.POST.get('instructions')

        reminder.medicine_name = medicine_name
        reminder.dosage = dosage
        reminder.reminder_time = reminder_time
        reminder.start_date = start_date
        reminder.instructions = instructions

        reminder.save()

        messages.success(
            request,
            'Medicine reminder updated successfully.'
        )

        return redirect('medicine_alerts')

    return render(
        request,
        'dashboard/edit_medicine_reminder.html',
        {
            'reminder': reminder
        }
    )

def emergency_sos(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        emergency_name = profile.emergency_contact_name.strip()
        emergency_phone = profile.emergency_contact_phone.strip()

        # Check whether emergency contact details exist
        if not emergency_name or not emergency_phone:

            messages.error(
                request,
                "Please add an emergency contact in your profile before using Emergency SOS."
            )

            return redirect("emergency_sos")

        # Record the SOS activation
        EmergencySOS.objects.create(
            user=request.user,
            emergency_contact_name=emergency_name,
            emergency_contact_phone=emergency_phone,
            status="Activated"
        )

        # Create notification
        create_notification(
            request.user,
            "Emergency SOS",
            "Emergency SOS Activated",
            "Your Emergency SOS alert has been activated successfully."
        )

        messages.success(
            request,
            "Emergency SOS activated successfully."
        )

        return redirect("emergency_sos")

    # Get previous SOS alerts for this user
    sos_history = EmergencySOS.objects.filter(
        user=request.user
    ).order_by("-triggered_at")

    return render(
        request,
        "dashboard/emergency_sos.html",
        {
            "profile": profile,
            "sos_history": sos_history,
        }
    )


def delete_emergency_sos(request, sos_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    sos = get_object_or_404(
        EmergencySOS,
        id=sos_id,
        user=request.user
    )

    sos.delete()

    messages.success(
        request,
        "SOS history record deleted successfully."
    )

    return redirect("emergency_sos")

def feedback(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    # Get all caregivers
    caregivers = User.objects.filter(
        userprofile__role="Caregiver"
    )

    # Get all volunteers
    volunteers = User.objects.filter(
        userprofile__role="Volunteer"
    )

    # Handle feedback submission
    if request.method == "POST":

        service_type = request.POST.get("service_type")
        service_provider_id = request.POST.get("service_provider")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Check rating and comment
        if not rating or not comment:
            messages.error(
                request,
                "Please provide a rating and feedback."
            )

            return redirect("feedback")

        # Caregiver or Volunteer feedback
        if service_type in ["Caregiver", "Volunteer"]:

            # Make sure a person is selected
            if not service_provider_id:

                messages.error(
                    request,
                    "Please select the person who provided the service."
                )

                return redirect("feedback")

            # Get selected user
            service_provider = get_object_or_404(
                User,
                id=service_provider_id
            )

            # Check selected person's role
            if service_type == "Caregiver":

                if (
                    not hasattr(service_provider, "userprofile")
                    or service_provider.userprofile.role != "Caregiver"
                ):

                    messages.error(
                        request,
                        "Invalid caregiver selected."
                    )

                    return redirect("feedback")

            elif service_type == "Volunteer":

                if (
                    not hasattr(service_provider, "userprofile")
                    or service_provider.userprofile.role != "Volunteer"
                ):

                    messages.error(
                        request,
                        "Invalid volunteer selected."
                    )

                    return redirect("feedback")

        else:

            # Service Request / Other
            service_provider = None

        # Create feedback
        Feedback.objects.create(
            user=request.user,
            service_type=service_type,
            service_provider=service_provider,
            rating=rating,
            comment=comment
        )

        # Create notification
        create_notification(
            request.user,
            "Feedback",
            "Feedback Submitted",
            "Your feedback has been submitted successfully. "
            "Thank you for helping us improve CareBridge."
        )

        messages.success(
            request,
            "Your feedback has been submitted successfully."
        )

        return redirect("feedback")

    # Get user's previous feedback
    feedbacks = Feedback.objects.filter(
        user=request.user
    ).select_related(
        "service_provider"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/feedback.html",
        {
            "feedbacks": feedbacks,
            "caregivers": caregivers,
            "volunteers": volunteers,
        }
    )


def delete_feedback(request, feedback_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        user=request.user
    )

    feedback.delete()

    messages.success(
        request,
        "Feedback deleted successfully."
    )

    return redirect("feedback")

def create_notification(user, notification_type, title, message):
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message
    )

def notifications(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    notification_list = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/notifications.html",
        {
            "notifications": notification_list,
        }
    )


def mark_notification_read(request, notification_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("notifications")

def assign_service_request(request, request_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    service_request.status = "Assigned"
    service_request.save()

    create_notification(
        service_request.user,
        "Service Request",
        "Service Request Assigned",
        "Your service request has been assigned successfully."
    )

    messages.success(
        request,
        "Service request assigned successfully."
    )

    return redirect('service_requests')

def complete_service_request(request, request_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    service_request.status = "Completed"
    service_request.save()

    create_notification(
        service_request.user,
        "Service Request",
        "Service Request Completed",
        "Your service request has been completed successfully."
    )

    messages.success(
        request,
        "Service request marked as completed."
    )

    return redirect('service_requests')


# ==============================
# ADMIN DASHBOARD
# ==============================

def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    # --------------------------
    # User statistics
    # --------------------------

    total_users = User.objects.count()

    elderly_users = UserProfile.objects.filter(
        role="Elderly Person"
    ).count()

    mobility_users = UserProfile.objects.filter(
        role="Person with Mobility Impairment"
    ).count()

    hearing_users = UserProfile.objects.filter(
        role="Person with Hearing Impairment"
    ).count()

    caregivers = UserProfile.objects.filter(
        role="Caregiver"
    ).count()

    volunteers = UserProfile.objects.filter(
        role="Volunteer"
    ).count()

    care_representatives = UserProfile.objects.filter(
        role="Care Representative"
    ).count()

    # --------------------------
    # Booking statistics
    # --------------------------

    total_caregiver_bookings = DirectCaregiverBooking.objects.count()

    total_volunteer_bookings = DirectVolunteerBooking.objects.count()

    pending_caregiver_bookings = DirectCaregiverBooking.objects.filter(
        status="Pending"
    ).count()

    pending_volunteer_bookings = DirectVolunteerBooking.objects.filter(
        status="Pending"
    ).count()

    accepted_caregiver_bookings = DirectCaregiverBooking.objects.filter(
        status="Accepted"
    ).count()

    accepted_volunteer_bookings = DirectVolunteerBooking.objects.filter(
        status="Accepted"
    ).count()

    completed_caregiver_bookings = DirectCaregiverBooking.objects.filter(
        status="Completed"
    ).count()

    completed_volunteer_bookings = DirectVolunteerBooking.objects.filter(
        status="Completed"
    ).count()

    # --------------------------
    # Other statistics
    # --------------------------

    total_service_requests = ServiceRequest.objects.count()

    total_feedback = Feedback.objects.count()

    total_sos = EmergencySOS.objects.count()

    total_notifications = Notification.objects.count()

    unread_notifications = Notification.objects.filter(
        is_read=False
    ).count()

    # --------------------------
    # Recent users
    # --------------------------

    recent_users = User.objects.order_by(
        "-date_joined"
    )[:10]

    # --------------------------
    # Recent caregiver bookings
    # --------------------------

    recent_caregiver_bookings = DirectCaregiverBooking.objects.select_related(
        "user",
        "caregiver"
    ).order_by("-booked_at")[:5]

    # --------------------------
    # Recent volunteer bookings
    # --------------------------

    recent_volunteer_bookings = DirectVolunteerBooking.objects.select_related(
        "user",
        "volunteer"
    ).order_by("-booked_at")[:5]

    # --------------------------
    # Recent notifications
    # --------------------------

    recent_notifications = Notification.objects.select_related(
        "user"
    ).order_by("-created_at")[:5]

    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "total_users": total_users,

            "elderly_users": elderly_users,
            "mobility_users": mobility_users,
            "hearing_users": hearing_users,
            "caregivers": caregivers,
            "volunteers": volunteers,
            "care_representatives": care_representatives,

            "total_caregiver_bookings": total_caregiver_bookings,
            "total_volunteer_bookings": total_volunteer_bookings,

            "pending_caregiver_bookings": pending_caregiver_bookings,
            "pending_volunteer_bookings": pending_volunteer_bookings,

            "accepted_caregiver_bookings": accepted_caregiver_bookings,
            "accepted_volunteer_bookings": accepted_volunteer_bookings,

            "completed_caregiver_bookings": completed_caregiver_bookings,
            "completed_volunteer_bookings": completed_volunteer_bookings,

            "total_service_requests": total_service_requests,
            "total_feedback": total_feedback,
            "total_sos": total_sos,

            "total_notifications": total_notifications,
            "unread_notifications": unread_notifications,

            "recent_users": recent_users,
            "recent_caregiver_bookings": recent_caregiver_bookings,
            "recent_volunteer_bookings": recent_volunteer_bookings,
            "recent_notifications": recent_notifications,
        }
    )

# ==============================
# ADMIN - MANAGE USERS
# ==============================

def admin_users(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    users = User.objects.select_related(
        'userprofile'
    ).order_by('-date_joined')

    return render(
        request,
        'dashboard/admin_users.html',
        {
            'users': users,
        }
    )

# ==============================
# ADMIN - EDIT USER
# ==============================

def admin_edit_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    user = get_object_or_404(
        User,
        id=user_id
    )

    # Do not allow editing the main administrator
    if user.is_superuser:
        messages.warning(
            request,
            "The administrator account cannot be edited here."
        )

        return redirect('admin_users')

    profile = get_object_or_404(
        UserProfile,
        user=user
    )

    if request.method == "POST":

        user.email = request.POST.get(
            "email"
        )

        user.first_name = request.POST.get(
            "first_name"
        )

        user.last_name = request.POST.get(
            "last_name"
        )

        user.save()


        profile.phone = request.POST.get(
            "phone"
        )

        profile.address = request.POST.get(
            "address"
        )

        profile.role = request.POST.get(
            "role"
        )

        profile.emergency_contact_name = request.POST.get(
            "emergency_contact_name"
        )

        profile.emergency_contact_phone = request.POST.get(
            "emergency_contact_phone"
        )

        profile.blood_group = request.POST.get(
            "blood_group"
        )

        profile.medical_conditions = request.POST.get(
            "medical_conditions"
        )

        profile.save()


        messages.success(
            request,
            "User details updated successfully."
        )

        return redirect('admin_users')


    return render(
        request,
        'dashboard/admin_edit_user.html',
        {
            'user_obj': user,
            'profile': profile,
        }
    )

# ==============================
# ADMIN - ENABLE / DISABLE USER
# ==============================

def admin_toggle_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user.is_superuser:

        messages.warning(
            request,
            "The administrator account cannot be disabled."
        )

        return redirect('admin_users')

    user.is_active = not user.is_active

    user.save()

    if user.is_active:

        messages.success(
            request,
            f"{user.username} has been enabled."
        )

    else:

        messages.warning(
            request,
            f"{user.username} has been disabled."
        )

    return redirect('admin_users')

# ==============================
# ADMIN - DELETE USER
# ==============================

def admin_delete_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user.is_superuser:

        messages.error(
            request,
            "The administrator account cannot be deleted."
        )

        return redirect('admin_users')

    username = user.username

    user.delete()

    messages.success(
        request,
        f"User {username} deleted successfully."
    )

    return redirect('admin_users')

# ==============================
# ADMIN - MANAGE CAREGIVERS
# ==============================

def admin_caregivers(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    caregivers = User.objects.select_related(
        'userprofile'
    ).filter(
        userprofile__role='Caregiver'
    ).order_by('-date_joined')

    return render(
        request,
        'dashboard/admin_caregivers.html',
        {
            'caregivers': caregivers,
        }
    )

# ==============================
# ADMIN - MANAGE VOLUNTEERS
# ==============================

def admin_volunteers(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    volunteers = User.objects.filter(
        userprofile__role="Volunteer"
    ).select_related(
        'userprofile'
    ).order_by('-date_joined')

    return render(
        request,
        'dashboard/admin_volunteers.html',
        {
            'volunteers': volunteers,
        }
    )

# ==============================
# ADMIN - MANAGE CARE REPRESENTATIVES
# ==============================

def admin_care_representatives(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    care_representatives = User.objects.filter(
        userprofile__role="Care Representative",
        is_superuser=False
    ).select_related(
        'userprofile'
    ).order_by('-date_joined')

    return render(
        request,
        'dashboard/admin_care_representatives.html',
        {
            'care_representatives': care_representatives,
        }
    )

# ==============================
# ADMIN - CAREGIVER BOOKINGS
# ==============================

def admin_caregiver_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    bookings = DirectCaregiverBooking.objects.select_related(
        'user',
        'caregiver'
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/admin_caregiver_bookings.html',
        {
            'bookings': bookings,
        }
    )

# ==============================
# ADMIN - VOLUNTEER BOOKINGS
# ==============================

def admin_volunteer_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    bookings = DirectVolunteerBooking.objects.select_related(
        'user',
        'volunteer'
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/admin_volunteer_bookings.html',
        {
            'bookings': bookings,
        }
    )

# ==============================
# ADMIN - SOS ALERTS
# ==============================

def admin_sos(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    sos_alerts = EmergencySOS.objects.select_related(
        'user'
    ).order_by('-triggered_at')

    return render(
        request,
        'dashboard/admin_sos.html',
        {
            'sos_alerts': sos_alerts,
        }
    )

# ==============================
# ADMIN - FEEDBACK
# ==============================

def admin_feedback(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    feedbacks = Feedback.objects.select_related(
        'user',
        'service_provider'
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/admin_feedback.html',
        {
            'feedbacks': feedbacks,
        }
    )

# ==============================
# ADMIN - MANAGE NOTIFICATIONS
# ==============================

def admin_notifications(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if not request.user.is_staff:
        return redirect('dashboard')

    notifications = Notification.objects.select_related(
        'user'
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/admin_notifications.html',
        {
            'notifications': notifications,
        }
    )