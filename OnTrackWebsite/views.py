from django.shortcuts import render
from django.http import HttpResponse
from .forms import Firstinput
from django.http import HttpResponseRedirect
from .forms import Secondinput1
from .forms import Secondinput2
#handling traffic on home page
#loading template

import io
from django.http import FileResponse
from django.conf import settings
from wkhtmltopdf.views import PDFTemplateView
from OnTrackWebsite.CheckProgress import CheckProgress
from django.views.generic.base import TemplateView
import datetime
import Graphs

class CalculatePDFView(PDFTemplateView):
    #template_name = 'templates/OnTrackWebsite/calculate.html'
    template_name = 'calculate.html'
    #base_url = 'html://' + settings.BASE_DIR
    filename = None

    def dispatch(self, request, *args, **kwargs):
        #request.session['name'] = CheckProgress.name
        #request.session['GMFCSLevel'] = CheckProgress.GMFCSLevel
        #request.session['age'] = CheckProgress.age
        #request.session['scores'] = CheckProgress.scores
        #self.name = request.session.get('name')
        self.GMFCSLevel = request.session.get('GMFCSLevel')
        previousAgeYear = int(request.session.get('previousAgeYear'))
        previousAgeMonth = int(request.session.get('previousAgeMonth'))
        currentAgeYear = int(request.session.get('currentAgeYear'))
        currentAgeMonth = int(request.session.get('currentAgeMonth'))
        self.age = [
            [previousAgeYear, previousAgeMonth],
            [currentAgeYear, currentAgeMonth]
        ]
        scores = request.session.get('scores')
        scores = [
            [scores.get('ECAB1'), scores.get('ECAB2')],
            [scores.get('SMWT1'), scores.get('SMWT2')],
            [scores.get('SAROMM1'), scores.get('SAROMM2')],
            [scores.get('CEDLpar1'), scores.get('CEDLpar2')],
            [scores.get('CEDLsc1'), scores.get('CEDLsc2')],
            [scores.get('EASE1'), scores.get('EASE2')],
            [scores.get('FSA1'), scores.get('FSA2')],
            [scores.get('HEALTH1'), scores.get('HEALTH2')],
            [scores.get('GMFM1'), scores.get('GMFM2')]
        ]
        output = CheckProgress.performCalculation(self.GMFCSLevel, self.age, scores)
        self.progress = output.get("progress")
        self.scores = output.get("scores")
        self.percentiles = output.get("percentiles")
        self.results = [
            {
                "progress": self.progress[0],
                "title": "Balance",
                "description": "Early Clinical Assessment of Balance. Scored from 0 to 100 (higher score = better balance).",
                "score": self.scores[0]
            },
            {
                "progress": self.progress[1],
                "title": "Strength",
                "description": "Functional Strength Assessment. Scored from 1 to 5 (higher score = stronger).",
                "score": self.scores[1]
            },
            {
                "progress": self.progress[2],
                "title": "Range of Motion",
                "description": "Spinal Alignment and Range of Motion Measure. Scored from 0 to 4 (lower score = fewer limitations).",
                "score": self.scores[2]
            },
            {
                "progress": self.progress[3],
                "title": "Endurance",
                "description": "6-Minute Walk Test. Scored in feet (higher score = further distance).",
                "score": self.scores[3]
            },
            {
                "progress": self.progress[4],
                "title": "Endurance",
                "description": "Early Activity Scale for Endurance. Scored from 1 to 5 (higher score = more endurance).",
                "score": self.scores[4]
            },
            {
                "progress": self.progress[5],
                "title": "Overall Health",
                "description": "Child Health Conditions Questionnaire. Scored from 0 to 7 (lower score = better overall health).",
                "score": self.scores[5]
            },
            {
                "progress": self.progress[6],
                "title": "Participation in Family and Recreational Activities",
                "description": "Child Engagement in Daily Life Measure. Scored from 1 to 5 (higher score = more participation).",
                "score": self.scores[6]
            },
            {
                "progress": self.progress[7],
                "title": "Performance in Self-Care Activities",
                "description": "Child Engagement in Daily Life Measure. Scored from 1 to 5 (higher score = needs less help).",
                "score": self.scores[7]
            },
            {
                "progress": self.progress[8],
                "title": "Gross Motor Function Measure",
                "description": "Gross Motor Function Measure, Scored from 0 to 100 ( higher score = greater function).",
                "score": self.scores[8]
            },
        ]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(CalculatePDFView, self).get_context_data(
            pagesize='A4',
            results = self.results,
            age=self.age,
            GMFCSLevel=self.GMFCSLevel,
            #name=self.name,
            date=datetime.datetime.now()
        )

def checkin(request):   
    
    if request.method == 'POST':
        form = Firstinput(request.POST)
        if form.is_valid():
            request.session['GMFCSLevel'] = form.cleaned_data['GMFCS']
            request.session['previousAgeMonth'] = form.cleaned_data['patient_age_mo1']
            request.session['previousAgeYear'] = form.cleaned_data['patient_age_yr1']
            request.session['currentAgeMonth'] = form.cleaned_data['patient_age_mo2']
            request.session['currentAgeYear'] = form.cleaned_data['patient_age_yr2']
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
            return HttpResponseRedirect('/results/')
    else:
        form = Secondinput1()
    return render(request, 'OnTrackWebsite/checkin1.html', {'title': 'Check in!', 'form' : form})


def checkin2(request):
    if request.method == 'POST':
        form = Secondinput2(request.POST)
        if form.is_valid():
            request.session['scores'] = form.cleaned_data
            print (form.cleaned_data)
            return HttpResponseRedirect('/results/')
    else:
        form = Secondinput2()
    return render(request, 'OnTrackWebsite/checkin2.html', {'title': 'Check in!', 'form' : form})

def home(request):
    return render(request, 'OnTrackWebsite/home.html', {'title': 'Home'})

def acknowledgements(request):
    return render(request, 'OnTrackWebsite/acknowledgements.html', {'title': ': Acknowledgements'})

def how_to_use_output(request):
    return render(request, 'OnTrackWebsite/how_to_use_output.html', {'title': ': how to use the output information'})

def how_it_calculates(request):
    return render(request, 'OnTrackWebsite/how_it_calculates.html', {'title': ': how it calculates'})
