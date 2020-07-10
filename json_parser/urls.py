from django.urls import path
from . import views

urlpatterns = [
    path('create_json/', views.ParserView.as_view()),
    path('create_DPView_json/', views.DPViewParserView.as_view()),
]
