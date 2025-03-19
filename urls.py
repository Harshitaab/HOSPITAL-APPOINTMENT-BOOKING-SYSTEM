from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')  # Redirects to login page first

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='start'),  # Redirect all users to login first
    path('home/', include('appointments.urls')),  # Home page will be available after login
]

