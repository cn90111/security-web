from django.urls import path
from . import views

urlpatterns = [
    path('create_json/', views.ParserView.as_view()),
]
