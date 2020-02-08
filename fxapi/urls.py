from django.urls import path
from . import views

urlpatterns = [
    path('cabs/', views.CabsAPIView.as_view()),
]
