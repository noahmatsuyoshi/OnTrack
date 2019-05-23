from django.shortcuts import render
from django.http import HttpResponse
import io
from django.http import FileResponse
from django.conf import settings
from easy_pdf.views import PDFTemplateView
from OnTrackWebsite.CheckProgress import CheckProgress

class CalculatePDFView(PDFTemplateView):
    #template_name = 'templates/OnTrackWebsite/calculate.html'
    template_name = 'calculate.html'
    #base_url = 'html://' + settings.BASE_DIR
    download_filename = 'results.pdf'
    

    def dispatch(self, request, *args, **kwargs):
        request.session['GMFCSLevel'] = CheckProgress.GMFCSLevel
        request.session['age'] = CheckProgress.age
        request.session['scores'] = CheckProgress.scores
        GMFCSLevel = request.session.get('GMFCSLevel')
        age = request.session.get('age')
        scores = request.session.get('scores')
        self.results = CheckProgress.performCalculation(GMFCSLevel, age, scores)
        print(self.results)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(CalculatePDFView, self).get_context_data(
            pagesize='A4',
            results = self.results,

            **kwargs
        )

#handling traffic on home page
#loading template
def home(request):
    return render(request, 'OnTrackWebsite/home.html')

def acknowledgements(request):
    return render(request, 'OnTrackWebsite/acknowledgements.html')
