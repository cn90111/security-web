from django.urls import path
from . import views
from general import views as general_views
from . import k_anonymity

urlpatterns = [
    path('',views.index),
    path('Execute_k_Anonymity/', k_anonymity.k_anonymity),
    path('show_k_progress/', k_anonymity.show_progress),
    path('Execute_Page/', general_views.ExecuteView.as_view()),
    path('Web_View_CSV/', general_views.PreviewCsvView.as_view()),
    path('File_List_<str:method>/', general_views.FileListView.as_view()),
    path('Download_Output/', general_views.DownloadView.as_view()),
    path('CSV_View_Output/', general_views.PreviewCsvView.as_view()),
    path('CSV_View_Upload/', general_views.PreviewCsvView.as_view()),
]