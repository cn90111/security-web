from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('initialize/', views.InitializeView.as_view()),
]