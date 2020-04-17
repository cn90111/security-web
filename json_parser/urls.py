from django.urls import path
from . import views
from . import json_parser

urlpatterns = [
    path('File_Upload/', views.ParserView.File_Upload),
]
