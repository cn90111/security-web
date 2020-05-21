from django.urls import path
from . import views
from general import views as general_views
from json_parser import views as json_parser_views
from . import k_anonymity

urlpatterns = [
    path('',views.index),
    path('Execute_k_Anonymity/', k_anonymity.k_anonymity),
    path('show_k_progress/', k_anonymity.show_progress),
    path('Execute_Page/', general_views.ExecuteView.as_view()),
    path('File_List_<str:method>/', general_views.FileListView.as_view()),
    path('Download_Output/', general_views.DownloadView.as_view()),
    path('CSV_View_<str:method>/', general_views.DisplayCsvView.as_view()),
    path('delete_file_<str:method>/', general_views.DeleteFileView.as_view()),
    path('custom/csv_name=<str:csv_name>/', json_parser_views.CustomView.as_view()),
]