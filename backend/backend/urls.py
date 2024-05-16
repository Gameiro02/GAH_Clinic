from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import LoginView, BookAppointmentView, ProcessPaymentView, AppointmentStatusView, UserAppointmentsView, DoctorsView, ClinicLoginView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('book-appointment/', BookAppointmentView.as_view(), name="book_appointment"),
    path('payment/', ProcessPaymentView.as_view(), name="process_payment"),
    path('appointments/<uuid:appointment_id>/status', AppointmentStatusView.as_view(), name='appointment_status'),
    path("user/appointments/", UserAppointmentsView.as_view(), name="user_appointments"),
    path("doctors/", DoctorsView.as_view(), name="doctors"),
    path("clinic/login/", ClinicLoginView.as_view(), name="clinic_login"),
    
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)