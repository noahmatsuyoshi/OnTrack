from django.shortcuts import render
from django.http import HttpResponse
#handling traffic on home page
#loading template
def home(request):
    return render(request, 'OnTrackWebsite/home.html')

def acknowledgements(request):
    return render(request, 'OnTrackWebsite/acknowledgements.html')

def how_to_use_output(request):
    return render(request, 'OnTrackWebsite/how_to_use_output.html')

def how_it_calculates(request):
    return render(request, 'OnTrackWebsite/how_it_calculates.html')

def checkin(request):
    return render(request, 'OnTrackWebsite/checkin.html')