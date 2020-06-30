from django.urls import path
from . import views

urlpatterns = [
    path('File_Upload/<str:mode>', views.FileView.as_view()),
]