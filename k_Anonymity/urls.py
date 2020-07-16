from django.urls import path
from . import views
from general import views as general_views
from json_parser import views as json_parser_views
from . import k_anonymity

app_name = 'k_Anonymity'
urlpatterns = [
    path('', views.index, name = 'home'),
    path('execute', views.KAnonymityView.as_view(), name = 'execute'),
    path('break_program/', views.BreakProgramView.as_view(), name = 'break_program'),
    path('show_progress/', k_anonymity.show_progress, name = 'show_progress'),
    path('execute_page/<str:csv_name>/', views.ExecuteView.as_view(), name = 'execute_page'),
    path('custom/', json_parser_views.CustomView.as_view(), name = 'custom'),
    path('custom/<str:csv_name>/', json_parser_views.CustomView.as_view()),
    path('finish/<str:csv_name>/', general_views.FinishView.as_view(), name = 'finish'),
    path('utility_page/<str:csv_name>/', general_views.UtilityPageView.as_view(), name = 'utility_page'),
    path('advanced_settings/<str:csv_name>/', json_parser_views.AdvancedSettingsView.as_view(), name = 'advanced_settings'),
]