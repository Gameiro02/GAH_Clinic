from django.urls import path
from .views import MYTokenObtainPairView

urlpatterns = [
    path('login/', MYTokenObtainPairView.as_view(), name='token_obtain_pair'),
]