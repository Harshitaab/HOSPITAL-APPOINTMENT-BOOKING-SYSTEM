from django.db import models
from django.contrib.auth.models import User

# Hospital Model
class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255, default="General")
    open_hours = models.CharField(max_length=100, default="Not Available")

    def __str__(self):
        return self.name

# Doctor Model
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    languages_spoken = models.CharField(max_length=255, default="English")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors")

    def __str__(self):
        return f"{self.name} - {self.speciality}"

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default="Unknown Patient")
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    medical_history = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')

    def __str__(self):
        return f"{self.patient.name} -> {self.doctor.name} on {self.appointment_date}"

# Support Message Model
class SupportMessage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.patient.name} - {self.message[:30]}..."
