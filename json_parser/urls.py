from django.urls import path
from . import views
from general import views as general_views

urlpatterns = [
    path('File_Upload/', general_views.FileView.as_view()),
    path('create_json/', views.ParserView.as_view()),
]
