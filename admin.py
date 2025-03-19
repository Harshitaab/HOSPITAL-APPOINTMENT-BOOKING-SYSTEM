from django.contrib import admin
from .models import Hospital, Doctor, Patient, Appointment

admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
