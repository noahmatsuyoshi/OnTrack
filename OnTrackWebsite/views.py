from django.shortcuts import render
from django.http import HttpResponse
#handling traffic on home page
#loading template
def home(request):
    return render(request, 'OnTrackWebsite/home.html', {'title': 'Home'})

def acknowledgements(request):
    return render(request, 'OnTrackWebsite/acknowledgements.html', {'title': ': Acknowledgements'})

def how_to_use_output(request):
    return render(request, 'OnTrackWebsite/how_to_use_output.html', {'title': ': how to use the output information'})

def how_it_calculates(request):
    return render(request, 'OnTrackWebsite/how_it_calculates.html', {'title': ': how it calculates'})

def checkin(request):
    return render(request, 'OnTrackWebsite/checkin.html', {'title': 'Check in!'})