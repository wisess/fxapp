from django.urls import path
from . import views

urlpatterns = [
    path('weekly-comfort-zones/', views.WeeklyComfortZoneAPIView.as_view()),
]
