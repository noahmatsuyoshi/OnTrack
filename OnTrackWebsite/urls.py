from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='OnTrack-home'),
    path('home/', views.home, name='OnTrack-home'),
    path('acknowledgements/', views.acknowledgements, name='OnTrack-acknowledgements'),
    path('how_to_use_output/', views.how_to_use_output, name='OnTrack-how_to_use_output'),
    path('how_it_calculates/', views.how_it_calculates, name='OnTrack-how_it_calculates'),
    path('checkin/', views.checkin, name='OnTrack-checkin'),
    path('checkin1/', views.checkin1, name='OnTrack-checkin1'),
    path('checkin2/', views.checkin2, name='OnTrack-checkin2'),
    path('results/', views.CalculatePDFView.as_view(), name='OnTrack-results')
]
