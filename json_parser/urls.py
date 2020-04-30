from django.urls import path
from . import views

urlpatterns = [
    path('File_Upload/', views.JsonFileView.as_view()),
    path('string_pair/csv_name=<str:csv_name>/', views.JsonFileView.as_view()),
    path('create_json/', views.ParserView.as_view()),
]
