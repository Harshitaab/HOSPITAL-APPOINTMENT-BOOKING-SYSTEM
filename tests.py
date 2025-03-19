from django.test import TestCase
from django.contrib.auth.models import User
from .models import Patient, Doctor, Hospital, Appointment
from django.urls import reverse

class UserAuthTests(TestCase):
    def test_user_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after signup
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirects after login

class DoctorTests(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name="Test Hospital", location="City", speciality="General")
        self.doctor = Doctor.objects.create(name="Dr. John Doe", speciality="Cardiology", hospital=self.hospital)
    
    def test_doctor_creation(self):
        self.assertEqual(self.doctor.name, "Dr. John Doe")
        self.assertEqual(self.doctor.speciality, "Cardiology")
        self.assertEqual(self.doctor.hospital.name, "Test Hospital")

class AppointmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='patientuser', password='password123')
        self.patient = Patient.objects.create(user=self.user, name="John Doe")
        self.hospital = Hospital.objects.create(name="General Hospital", location="City", speciality="General")
        self.doctor = Doctor.objects.create(name="Dr. Smith", speciality="Dermatology", hospital=self.hospital)
    
    def test_appointment_creation(self):
        appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date="2025-03-12 10:00:00")
        self.assertEqual(appointment.patient.name, "John Doe")
        self.assertEqual(appointment.doctor.name, "Dr. Smith")

