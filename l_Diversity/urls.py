from django.urls import path
from . import views
from general import views as general_views
from json_parser import views as json_parser_views
from . import l_diversity

urlpatterns = [
    path('',views.index),
    path('Execute/', views.LDiversityView.as_view()),
    path('break_program/', views.BreakProgramView.as_view()),
    path('show_progress/', l_diversity.show_progress),
    path('Execute_Page/csv_name=<str:csv_name>/', views.ExecuteView.as_view()),
    path('File_List_<str:method>/', general_views.FileListView.as_view()),
    path('Download_Output/csv_name=<str:csv_name>/', general_views.DownloadView.as_view()),
    path('CSV_View_<str:method>/', general_views.DisplayCsvView.as_view()),
    path('custom/csv_name=<str:csv_name>/', json_parser_views.CustomView.as_view()),
    path('finish/csv_name=<str:csv_name>/', general_views.FinishView.as_view()),
    path('utility_page/csv_name=<str:csv_name>/', general_views.UtilityPageView.as_view()),
    path('check_utility/', general_views.CheckUtilityView.as_view()),
    path('advanced_settings/csv_name=<str:csv_name>/', json_parser_views.AdvancedSettingsView.as_view()),
    path('title_check/', general_views.TitleCheckView.as_view()),
]