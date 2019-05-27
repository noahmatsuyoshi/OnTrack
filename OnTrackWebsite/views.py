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

class CalculatePDFView(PDFTemplateView):
    #template_name = 'templates/OnTrackWebsite/calculate.html'
    template_name = 'calculate.html'
    #base_url = 'html://' + settings.BASE_DIR
    filename = None

    def dispatch(self, request, *args, **kwargs):
        request.session['GMFCSLevel'] = CheckProgress.GMFCSLevel
        request.session['age'] = CheckProgress.age
        request.session['scores'] = CheckProgress.scores
        GMFCSLevel = request.session.get('GMFCSLevel')
        age = request.session.get('age')
        scores = request.session.get('scores')
        progress = CheckProgress.performCalculation(GMFCSLevel, age, scores)
        self.results = [
            {
                "progress": progress[0],
                "title": "Balance",
                "description": "Early Clinical Assessment of Balance. Scored from 0 to 100 (higher score = better balance).",
                "score": scores[0]
            },
            {
                "progress": progress[1],
                "title": "Strength",
                "description": "Functional Strength Assessment. Scored from 1 to 5 (higher score = stronger).",
                "score": scores[1]
            },
            {
                "progress": progress[2],
                "title": "Range of Motion",
                "description": "Spinal Alignment and Range of Motion Measure. Scored from 0 to 4 (lower score = fewer limitations).",
                "score": scores[2]
            },
            {
                "progress": progress[3],
                "title": "Endurance",
                "description": "6-Minute Walk Test. Scored in feet (higher score = further distance).",
                "score": scores[3]
            },
            {
                "progress": progress[4],
                "title": "Endurance",
                "description": "Early Activity Scale for Endurance. Scored from 1 to 5 (higher score = more endurance).",
                "score": scores[4]
            },
            {
                "progress": progress[5],
                "title": "Overall Health",
                "description": "Child Health Conditions Questionnaire. Scored from 0 to 7 (lower score = better overall health).",
                "score": scores[5]
            },
            {
                "progress": progress[6],
                "title": "Participation in Family and Recreational Activities",
                "description": "Child Engagement in Daily Life Measure. Scored from 1 to 5 (higher score = more participation).",
                "score": scores[6]
            },
            {
                "progress": progress[7],
                "title": "Performance in Self-Care Activities",
                "description": "Child Engagement in Daily Life Measure. Scored from 1 to 5 (higher score = needs less help).",
                "score": scores[7]
            },
            {
                "progress": progress[8],
                "title": "Gross Motor Function Measure",
                "description": "Gross Motor Function Measure, Scored from 0 to 100 ( higher score = greater function).",
                "score": scores[8]
            },
        ]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(CalculatePDFView, self).get_context_data(
            pagesize='A4',
            results = self.results,


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




