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

    caregivers = UserProfile.objects.filter(
        role="Caregiver"
    )

    active_booking = DirectCaregiverBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    return render(
        request,
        'dashboard/book_caregiver.html',
        {
            'caregivers': caregivers,
            'active_booking': active_booking,
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
                "You can book another caregiver after the current booking is completed, rejected, or cancelled."
            )

        return redirect('book_caregiver')

    caregiver = get_object_or_404(
        User,
        id=caregiver_id
    )

    DirectCaregiverBooking.objects.create(
        user=request.user,
        caregiver=caregiver,
        status="Pending"
    )

    messages.success(
        request,
        "Caregiver booking request sent successfully."
    )

    return redirect('book_caregiver')


def my_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    caregiver_bookings = DirectCaregiverBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at')

    volunteer_bookings = DirectVolunteerBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/my_bookings.html',
        {
            'caregiver_bookings': caregiver_bookings,
            'volunteer_bookings': volunteer_bookings,
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

    volunteers = UserProfile.objects.filter(
        role="Volunteer"
    )

    # Check whether the user already has an active volunteer booking
    active_booking = DirectVolunteerBooking.objects.filter(
        user=request.user,
        status__in=["Pending", "Accepted"]
    ).first()

    booking_status = {}

    if active_booking:
        booking_status[active_booking.volunteer_id] = active_booking.status

    return render(
        request,
        'dashboard/book_volunteer.html',
        {
            'volunteers': volunteers,
            'booking_status': booking_status,
            'active_booking': active_booking,
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
                "You can book another volunteer after the current booking is completed, rejected, or cancelled."
            )

        return redirect('book_volunteer')

    volunteer = get_object_or_404(
        User,
        id=volunteer_id
    )

    DirectVolunteerBooking.objects.create(
        user=request.user,
        volunteer=volunteer,
        status="Pending"
    )

    messages.success(
        request,
        "Volunteer booking request sent successfully."
    )

    return redirect('book_volunteer')


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

    booking.status = "Completed"
    booking.save()

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

    current_time = datetime.now().time()

    due_reminders = []

    for reminder in reminders:

        if (
            reminder.status == "Pending"
            and reminder.start_date <= datetime.now().date()
            and reminder.reminder_time <= current_time
        ):
            due_reminders.append(reminder)

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