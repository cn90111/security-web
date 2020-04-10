from django.urls import path
from . import views
from . import t_closeness

urlpatterns = [
	path('',views.index),
	path('Execute_t_closeness/', t_closeness.t_closeness),
	path('show_t_closeness/', t_closeness.show_progress),
	path('Execute_Page/',views.t_Closeness),
	path('Web_View_CSV/', views.Web_View_CSV),
	path('File_Upload/', views.File_Upload),
	path('File_List_Upload/',views.File_List_Upload),
	path('File_List_Output/',views.File_List_Output),
	path('Download_Output/',views.Download_Output),
	path('CSV_View_Output/',views.CSV_View_Output),
	path('CSV_View_Upload/',views.CSV_View_Upload),
]