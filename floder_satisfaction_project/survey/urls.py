
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('preview/', views.preview_data, name='preview_data'),
    path('export/', views.export_csv, name='export_csv')
]