from django.shortcuts import render
from django.http import HttpResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from easy_pdf.views import PDFTemplateView

class CalculatePDFView(PDFTemplateView):
    #template_name = 'templates/OnTrackWebsite/calculate.html'
    template_name = 'calculate.html'
    #base_url = 'html://' + settings.BASE_DIR
    download_filename = 'results.pdf'

    def get_context_data(self, **kwargs):
        return super(CalculatePDFView, self).get_context_data(
            pagesize='A4',
            title='Hi there!',
            **kwargs
        )

#handling traffic on home page
#loading template
def home(request):
    return render(request, 'OnTrackWebsite/home.html')

def acknowledgements(request):
    return render(request, 'OnTrackWebsite/acknowledgements.html')

def viewPDF(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, filename='hello.pdf')