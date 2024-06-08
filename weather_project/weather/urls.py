from django.urls import path
from .views import WeatherView  # Import the WeatherView class

urlpatterns = [
    path('', WeatherView.as_view(), name='get_weather'),  # Use as_view() for class-based views
]
