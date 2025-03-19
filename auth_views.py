from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor, Patient

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_type = request.POST["user_type"]  # "doctor" or "patient"

        user = User.objects.create_user(username=username, password=password)

        if user_type == "doctor":
            Doctor.objects.create(user=user)
        else:
            Patient.objects.create(user=user)

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "appointments/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "appointments/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
