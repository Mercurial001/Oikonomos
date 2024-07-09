from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import authenticated_user
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from economics import settings


def index(request):

    return render(request, 'base.html', {

    })


@authenticated_user
def authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal-homepage', username=username)
        else:
            messages.error(request, "Invalid Form Data")

    return render(request, 'login.html', {

    })


def privacy_policy(request):
    privacy_policy_obj = PrivacyPolicy.objects.first()
    return render(request, 'privacy_policy.html', {
        'privacy_policy_obj': privacy_policy_obj,
    })


def terms_of_use(request):
    terms_statement = TermsOfService.objects.first()
    return render(request, 'terms_of_use.html', {
        'terms_statement': terms_statement,
    })


def about_us(request):
    about_statement = About.objects.first()
    return render(request, 'about.html', {
        'about_statement': about_statement,
    })


def contact_us_page(request):
    if request.method == 'POST':
        message = request.POST.get('contact-message')
        email_sender = request.POST.get('sender-email')
        email_authenticated = request.POST.get('sender-email-authenticated')
        subject = request.POST.get('subject')

        if request.user.is_authenticated:
            email = email_authenticated
        else:
            email = email_sender

        html_message = render_to_string('email.html', {
            'email': email,
            'message': message,
            'subject': subject
        })

        send_mail(
            subject,
            message,
            from_email=email,
            recipient_list=[settings.EMAIL_HOST_USER],
            html_message=html_message,
        )

        return redirect('contact-us')

    return render(request, 'contact_us.html', {

    })


def logout_user(request):
    logout(request)
    return redirect('homepage')


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists')
        else:
            if password1 == password2:
                hashed_password = make_password(password1)
                User.objects.create(
                    username=username,
                    password=hashed_password,
                    email=email
                )
                messages.success(request, f'Account {username} successfully created!')
                return redirect('login')
            else:
                messages.error(request, 'Passwords not the same')

    return render(request, 'registration.html', {

    })
