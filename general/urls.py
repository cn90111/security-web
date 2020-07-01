from django.urls import path
from . import views

urlpatterns = [
    path('File_Upload/<str:mode>', views.FileView.as_view()),
    path('Download_Output/csv_name=<str:csv_name>/', views.DownloadView.as_view()),
    path('CSV_View_<str:method>/', views.DisplayCsvView.as_view()),
    path('check_utility/', views.CheckUtilityView.as_view()),
    path('title_check/', views.TitleCheckView.as_view()),
]