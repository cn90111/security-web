from django.urls import path
from . import views

urlpatterns = [
    path('file_upload/<str:mode>', views.FileView.as_view(), name = 'file_upload'),
    path('download_output/<str:csv_name>/', views.DownloadView.as_view(), name = 'download_output'),
    path('display_<str:method>/', views.DisplayCsvView.as_view(), name = 'display'),
    path('check_utility/', views.CheckUtilityView.as_view(), name = 'check_utility'),
    path('title_check/', views.TitleCheckView.as_view(), name = 'title_check'),
    path('update_log/', views.UpdateLogView.as_view(), name = 'update_log'),
    path('check_file_status/', views.CheckFileStatus.as_view(), name = 'check_file_status'),
]