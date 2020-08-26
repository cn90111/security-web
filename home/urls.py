from django.urls import path
from . import views
from general import views as general_views

urlpatterns = [
    path('', views.index, name='home'),
    path('initialize/', views.InitializeView.as_view(), name='initialize'),
    path('update_log/', general_views.UpdateLogView.as_view(), name = 'update_log'),
]