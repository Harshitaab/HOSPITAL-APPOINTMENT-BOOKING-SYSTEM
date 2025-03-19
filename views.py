from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Patient, Doctor, Appointment, SupportMessage, Hospital
from .forms import PatientForm, SupportMessageForm
from django.shortcuts import render
from .models import Patient

def home_view(request):
    patient = Patient.objects.order_by("id").first()  # Fetch the first available patient
    return render(request, "home.html", {"patient": patient})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "signup.html")
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("home")
    return render(request, "signup.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def search_doctors(request):
    specialty = request.GET.get('specialty', '')
    doctors = Doctor.objects.filter(speciality__icontains=specialty) if specialty else Doctor.objects.all()
    return render(request, 'search_doctors.html', {'doctors': doctors})

def book_appointment(request):
    if request.method == "POST":
        patient_name = request.POST["name"]
        doctor_id = request.POST["doctor"]
        date = request.POST["date"]
        time = request.POST["time"]
        patient, _ = Patient.objects.get_or_create(name=patient_name)
        doctor = get_object_or_404(Doctor, id=doctor_id)
        appointment = Appointment.objects.create(
            patient=patient, 
            doctor=doctor, 
            appointment_date=f"{date} {time}", 
            status="Pending"
        )
        return render(request, "success.html", {"appointment": appointment})
    doctors = Doctor.objects.all()
    return render(request, "book_appointment.html", {"doctors": doctors})

def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'register_patient.html', {'form': form})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_support(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    group_patients = Patient.objects.filter(condition=patient.condition)
    messages_list = SupportMessage.objects.filter(patient=patient).order_by('-created_at')
    paginator = Paginator(messages_list, 5)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            support_message = form.save(commit=False)
            support_message.patient = patient
            support_message.save()
            return redirect('patient_support', patient_id=patient.id)
    else:
        form = SupportMessageForm()
    return render(request, 'patient_support.html', {
        'patient': patient,
        'group_patients': group_patients,
        'form': form,
        'messages': messages,
    })
