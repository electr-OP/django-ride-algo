from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.RideMatchingView.as_view(), name='ride_request'),
    path('navigation/', views.RideNavigationView.as_view(), name='ride_navigation'),
]