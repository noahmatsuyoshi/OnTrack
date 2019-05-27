from django.shortcuts import render
from django.http import HttpResponse
from .forms import Firstinput
from django.http import HttpResponseRedirect
from .forms import Secondinput1
from .forms import Secondinput2
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
    
    if request.method == 'POST':
        form = Firstinput(request.POST)
        if form.is_valid():
            print (form.cleaned_data)
            request.session['GMFCSLevel'] = form.cleaned_data['GMFCS']
            request.session['ageMonth'] = form.cleaned_data['patient_age_mo']
            request.session['ageYear'] = form.cleaned_data['patient_age_yr']
            if (form.cleaned_data['GMFCS'] == "I" or form.cleaned_data['GMFCS'] == "II" or form.cleaned_data['GMFCS'] == "III"):
                return HttpResponseRedirect('/checkin1/')
            else:
                return HttpResponseRedirect('/checkin2/')     
    else:
        form = Firstinput()
    return render(request, 'OnTrackWebsite/checkin.html', {'title': 'Check in!', 'form' : form})


def checkin1(request):
    if request.method == 'POST':
        form = Secondinput1(request.POST)
        if form.is_valid():
            request.session['scores'] = form.cleaned_data
            print (form.cleaned_data)
            #return HttpResponseRedirect('/thanks/')
    else:
        form = Secondinput1()
    return render(request, 'OnTrackWebsite/checkin1.html', {'title': 'Check in!', 'form' : form})


def checkin2(request):
    if request.method == 'POST':
        form = Secondinput2(request.POST)
        if form.is_valid():
            request.session['scores'] = form.cleaned_data
            print (form.cleaned_data)
            #return HttpResponseRedirect('/thanks/')
    else:
        form = Secondinput2()
    return render(request, 'OnTrackWebsite/checkin2.html', {'title': 'Check in!', 'form' : form})




