from django.urls import path
from . import views
from general import views as general_views
from . import l_diversity

urlpatterns = [
    path('',views.index),
    path('Execute_l_diversity/', l_diversity.l_diversity),
    path('show_l_progress/', l_diversity.show_progress),
    path('Execute_Page/', general_views.ExecuteView.as_view()),
    path('Web_View_CSV/', general_views.PreviewCsvView.as_view()),
    path('File_List_<str:method>/', general_views.FileListView.as_view()),
    path('Download_Output/', general_views.DownloadView.as_view()),
    path('CSV_View_<str:method>/', general_views.PreviewCsvView.as_view()),
    path('delete_file_<str:method>/', general_views.DeleteFileView.as_view()),
]