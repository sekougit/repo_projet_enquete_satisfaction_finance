from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.decorators import login_required

from .models import SatisfactionSurvey
from .forms import CSVUploadForm
from .csv_loader import import_survey_csv


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['csv_file']
            result = import_survey_csv(file)

            return render(request, "survey/upload_csv.html", {
                "form": form,
                "result": result
            })

    else:
        form = CSVUploadForm()

    return render(request, "survey/upload_csv.html", {"form": form})


def preview_data(request):

    data = SatisfactionSurvey.objects.all().values()

    df = pd.DataFrame(data)

    preview_html = df.head(100).to_html(
        classes='table',
        index=False
    )

    return render(request, "survey/preview_data.html", {
        "preview": preview_html
    })

def export_csv(request):

    data = SatisfactionSurvey.objects.all().values()

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_export.csv"'

    df.to_csv(response, index=False)

    return response