from django.urls import path
from . import views
from . import k_anonymity

urlpatterns = [
	path('',views.index),
	path('Execute_k_Anonymity/', k_anonymity.k_anonymity),
	path('show_k_progress/', k_anonymity.show_progress),
	path('Execute_Page/',views.k_Anonymity),
	path('Web_View_CSV/', views.Web_View_CSV),
	path('File_Upload/', views.File_Upload),
	path('File_List_Upload/',views.File_List_Upload),
	path('File_List_Output/',views.File_List_Output),
	path('Download_Output/',views.Download_Output),
	path('CSV_View_Output/',views.CSV_View_Output),
	path('CSV_View_Upload/',views.CSV_View_Upload),
]