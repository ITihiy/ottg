from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth

from django.conf import settings
from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('accounts:login') + '?token=' + str(token.uid))
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        settings.EMAIL_HOST_USER,
        [email]
    )
    messages.success(request, 'Check your email, we\'ve sent you a link you can use to log in.')
    return redirect('lists:home')


def login(request):
    user = auth.authenticate(request, uid=request.GET.get('token'))
    if user is not None:
        auth.login(request, user)
    return redirect('lists:home')
