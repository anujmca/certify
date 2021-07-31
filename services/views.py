from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User



def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # check if user has entered correct credentials
        user = authenticate(username=email, password=password)
        if user is not None and user.is_authenticated:
            django_login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else '/')
        else:
            return redirect('/login')


def logout(request):
    if request.user is not None and request.user.is_authenticated:
        django_logout(request)
    return redirect('/')


