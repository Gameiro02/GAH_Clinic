"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import BookAppointmentView, ProcessPaymentView, AppointmentStatusView, UserAppointmentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('book-appointment/', BookAppointmentView.as_view(), name="book_appointment"),
    path('payment/', ProcessPaymentView.as_view(), name="process_payment"),
    path('appointments/<uuid:appointment_id>/status', AppointmentStatusView.as_view(), name='appointment_status'),
    path("user/appointments/", UserAppointmentsView.as_view(), name="user_appointments"),
]
