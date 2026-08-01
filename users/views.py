from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import UserProfile


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

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'profile': profile
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