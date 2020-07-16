from django.urls import path
from . import views

urlpatterns = [
    path('create_json/', views.ParserView.as_view(), name = 'create_json'),
    path('create_DPView_json/', views.DPViewParserView.as_view(), name = 'create_DPView_json'),
]
