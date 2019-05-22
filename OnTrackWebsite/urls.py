from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='OnTrack-home'),
    path('acknowledgements/', views.acknowledgements, name='OnTrack-acknowledgements'),
    path('pdf/', views.viewPDF, name='OnTrack-ViewPDF'),
]
