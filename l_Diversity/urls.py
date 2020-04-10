from django.urls import path
from . import views
from . import l_diversity

urlpatterns = [
	path('',views.index),
	path('Execute_l_diversity/', l_diversity.l_diversity),
	path('show_l_progress/', l_diversity.show_progress),
	path('Execute_Page/',views.l_Diversity),
	path('Web_View_CSV/', views.Web_View_CSV),
	path('File_Upload/', views.File_Upload),
	path('File_List_Upload/',views.File_List_Upload),
	path('File_List_Output/',views.File_List_Output),
	path('Download_Output/',views.Download_Output),
	path('CSV_View_Output/',views.CSV_View_Output),
	path('CSV_View_Upload/',views.CSV_View_Upload),
]