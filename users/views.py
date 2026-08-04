from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import DirectCaregiverBooking, DirectVolunteerBooking


from .models import (
    UserProfile,
    CareRepresentativeRequest,
    CareRepresentativeConnection,
    CaregiverAssignment,
    VolunteerAssignment,
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

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile = UserProfile.objects.get(
                user=user
            )

            if profile.role == "Care Representative":

                return redirect('/care-rep-dashboard/')

            else:

                return redirect('/dashboard/')

        else:

            return render(
                request,
                'login.html',
                {
                    'error': 'Invalid Username or Password'
                }
            )

    return render(request, 'login.html')


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    representative = None
    caregiver = None
    volunteer = None

    # Get Care Representative
    connection = CareRepresentativeConnection.objects.filter(
        user=request.user
    ).first()

    if connection:
        representative = connection.representative

    # Get Caregiver
    caregiver_assignment = CaregiverAssignment.objects.filter(
        user=request.user
    ).first()

    if caregiver_assignment:
        caregiver = caregiver_assignment.caregiver

    # Get Volunteer
    volunteer_assignment = VolunteerAssignment.objects.filter(
        user=request.user
    ).first()

    if volunteer_assignment:
        volunteer = volunteer_assignment.volunteer

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'profile': profile,
            'representative': representative,
            'caregiver': caregiver,
            'volunteer': volunteer,
        }
    )


def profile(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(user=request.user)

    if profile.role == "Care Representative":

        return render(
            request,
            'dashboard/care_rep_profile.html',
            {
                'profile': profile,
                'pending_requests': CareRepresentativeRequest.objects.filter(
                    representative=request.user,
                    status='Pending'
                ),
                'connections': CareRepresentativeConnection.objects.filter(
                    representative=request.user
                )
            }
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


    
def care_representatives(request):

    if not request.user.is_authenticated:

        return redirect('/login/')


    profile = UserProfile.objects.get(
        user=request.user
    )


    message = ""


    if request.method == "POST":

        action = request.POST.get("action")


        # SEND REQUEST
        if action == "send":

            representative_id = request.POST.get(
                "representative_id"
            )


            try:

                representative = User.objects.get(
                    id=representative_id
                )


                already_exists = CareRepresentativeRequest.objects.filter(
                    requester=request.user,
                    representative=representative
                ).exists()


                if not already_exists:

                    CareRepresentativeRequest.objects.create(
                        requester=request.user,
                        representative=representative
                    )

                    message = "Request sent successfully."


                else:

                    message = "Request already exists."


            except User.DoesNotExist:

                message = "Care Representative not found."



        # ACCEPT REQUEST
        elif action == "accept":

            request_id = request.POST.get(
                "request_id"
            )


            try:

                req = CareRepresentativeRequest.objects.get(
                    id=request_id,
                    representative=request.user
                )


                req.status = "Accepted"
                req.save()


                CareRepresentativeConnection.objects.get_or_create(
                    user=req.requester,
                    representative=req.representative
                )


                message = "Request accepted."


            except CareRepresentativeRequest.DoesNotExist:

                message = "Request not found."



        # REJECT REQUEST
        elif action == "reject":

            request_id = request.POST.get(
                "request_id"
            )


            try:

                req = CareRepresentativeRequest.objects.get(
                    id=request_id,
                    representative=request.user
                )


                req.status = "Rejected"
                req.save()


                message = "Request rejected."


            except CareRepresentativeRequest.DoesNotExist:

                message = "Request not found."



    # SEARCH CARE REPRESENTATIVE

    search_query = request.GET.get(
        "search",
        ""
    ).strip()


    search_user = None
    search_profile = None
    searched = False


    if search_query:

        searched = True


        try:

            user = User.objects.get(
                username=search_query
            )


            user_profile = UserProfile.objects.get(
                user=user
            )


            if user_profile.role == "Care Representative":

                search_user = user
                search_profile = user_profile


        except (
            User.DoesNotExist,
            UserProfile.DoesNotExist
        ):

            pass



    # PENDING REQUESTS

    pending_requests = CareRepresentativeRequest.objects.filter(
        representative=request.user,
        status="Pending"
    )



    # CONNECTED REPRESENTATIVES

    connected = CareRepresentativeConnection.objects.filter(
        user=request.user
    )

    # MY REQUESTS

    my_requests = CareRepresentativeRequest.objects.filter(
         requester=request.user
          ).order_by('-created_at')

    return render(
        request,
        "dashboard/care_representatives.html",
        {
            "profile": profile,
            "message": message,
            "searched": searched,
            "search_query": search_query,
            "search_user": search_user,
            "search_profile": search_profile,
            "pending_requests": pending_requests,
            "connected": connected,
            "pending_requests": pending_requests,
            "my_requests": my_requests,
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


    pending_requests = CareRepresentativeRequest.objects.filter(
        representative=request.user,
        status="Pending"
    )


    connections = CareRepresentativeConnection.objects.filter(
        representative=request.user
    )


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
            "pending_requests": pending_requests,
            "connections": connections,
            "caregivers": caregivers,
            "volunteers": volunteers,
        }
    )

def assign_user(request, connection_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.role != "Care Representative":
        return redirect('/dashboard/')

    connection = get_object_or_404(
        CareRepresentativeConnection,
        id=connection_id
    )

    if request.method == "POST":

        caregiver_id = request.POST.get("caregiver")
        volunteer_id = request.POST.get("volunteer")

        # Nothing selected
        if not caregiver_id and not volunteer_id:

            messages.warning(
                request,
                "Please select at least one caregiver or volunteer."
            )

            return redirect('care_rep_dashboard')

        # -------------------------
        # Assign Caregiver
        # -------------------------

        if caregiver_id:

            if CaregiverAssignment.objects.filter(
                user=connection.user
            ).exists():

                messages.warning(
                    request,
                    "A caregiver has already been assigned to this user."
                )

            else:

                caregiver = User.objects.get(
                    id=caregiver_id
                )

                CaregiverAssignment.objects.create(

                    user=connection.user,

                    caregiver=caregiver,

                    assigned_by=request.user

                )

                messages.success(
                    request,
                    "Caregiver assigned successfully."
                )

        # -------------------------
        # Assign Volunteer
        # -------------------------

        if volunteer_id:

            if VolunteerAssignment.objects.filter(
                user=connection.user
            ).exists():

                messages.warning(
                    request,
                    "A volunteer has already been assigned to this user."
                )

            else:

                volunteer = User.objects.get(
                    id=volunteer_id
                )

                VolunteerAssignment.objects.create(

                    user=connection.user,

                    volunteer=volunteer,

                    assigned_by=request.user

                )

                messages.success(
                    request,
                    "Volunteer assigned successfully."
                )

    return redirect('care_rep_dashboard')

def accept_request(request, request_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method != "POST":
        return redirect('care_rep_dashboard')

    try:

        req = CareRepresentativeRequest.objects.get(
            id=request_id,
            representative=request.user
        )

        req.status = "Accepted"
        req.save()

        CareRepresentativeConnection.objects.get_or_create(
            user=req.requester,
            representative=req.representative
        )

        caregiver_id = request.POST.get("caregiver")
        volunteer_id = request.POST.get("volunteer")

        if caregiver_id:

            caregiver = User.objects.get(id=caregiver_id)

            CaregiverAssignment.objects.update_or_create(
                user=req.requester,
                defaults={
                    "caregiver": caregiver,
                    "assigned_by": request.user
                }
            )

        if volunteer_id:

            volunteer = User.objects.get(id=volunteer_id)

            VolunteerAssignment.objects.update_or_create(
                user=req.requester,
                defaults={
                    "volunteer": volunteer,
                    "assigned_by": request.user
                }
            )

        messages.success(
            request,
            "Caregiver and Volunteer assigned successfully."
        )

    except CareRepresentativeRequest.DoesNotExist:

        messages.error(
            request,
            "Request not found."
        )

    return redirect('care_rep_dashboard')

def reject_request(request, request_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    try:

        req = CareRepresentativeRequest.objects.get(
            id=request_id,
            representative=request.user
        )

        req.status = "Rejected"
        req.save()

        messages.success(
            request,
            "Request rejected successfully."
        )

    except CareRepresentativeRequest.DoesNotExist:

        messages.error(
            request,
            "Request not found."
        )

    return redirect('care_rep_dashboard')


def book_caregiver(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    caregivers = UserProfile.objects.filter(
        role="Caregiver"
    )

    booked_ids = DirectCaregiverBooking.objects.filter(
        user=request.user,
        status="Pending"
    ).values_list(
        'caregiver_id',
        flat=True
    )

    return render(
        request,
        'dashboard/book_caregiver.html',
        {
            'caregivers': caregivers,
            'booked_ids': booked_ids,
        }
    )

def confirm_caregiver_booking(request, caregiver_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    caregiver = User.objects.get(
        id=caregiver_id
    )

    existing_booking = DirectCaregiverBooking.objects.filter(
        user=request.user,
        caregiver=caregiver,
        status="Pending"
    ).first()

    if existing_booking:

        messages.warning(
            request,
            "You have already sent a booking request to this caregiver."
        )

        return redirect('book_caregiver')

    DirectCaregiverBooking.objects.create(

        user=request.user,

        caregiver=caregiver,

        status="Pending"

    )

    messages.success(
        request,
        "Booking request sent successfully."
    )

    return redirect('book_caregiver')

def my_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    bookings = DirectCaregiverBooking.objects.filter(
        user=request.user
    ).order_by('-booked_at')

    return render(
        request,
        'dashboard/my_bookings.html',
        {
            'bookings': bookings
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
        'dashboard/caregiver_dashboard.html',
        {
            'bookings': bookings
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

    # Update assignment status if this booking came from a Care Representative assignment
    try:
        assignment = CaregiverAssignment.objects.get(
            user=booking.user,
            caregiver=request.user
        )
        assignment.status = "Accepted"
        assignment.save()

    except CaregiverAssignment.DoesNotExist:
        pass

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

    # Update assignment status if this booking came from a Care Representative assignment
    try:
        assignment = CaregiverAssignment.objects.get(
            user=booking.user,
            caregiver=request.user
        )
        assignment.status = "Rejected"
        assignment.save()

    except CaregiverAssignment.DoesNotExist:
        pass

    messages.success(
        request,
        "Booking rejected."
    )

    return redirect('caregiver_dashboard')