from django.urls import path
from .views import (
    home_view, login_view, signup_view, logout_view,
    search_doctors, book_appointment, register_patient,
    patient_list, patient_support
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('search_doctors/', search_doctors, name='search_doctors'),
    path('logout/', logout_view, name='logout'),
    path('book_appointment/', book_appointment, name='book_appointment'),
    path('register_patient/', register_patient, name='register_patient'),
    path('patients/', patient_list, name='patient_list'),
    path('patients/<int:patient_id>/support/', patient_support, name='patient_support'),
]
