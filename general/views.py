from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage
from django.views import View
from .models import FileModel
from .forms import UploadFileForm
import os
import logging
import pandas as pd

today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

# Create your views here.
class ExecuteView(View):
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-2] # url like 127.0.0.1:8000/[caller]/
        path = 'upload/'+caller+'/'
        files = os.listdir(path)
        s = []
        for filename in os.listdir(path):
            filepath = os.path.join(path,filename)
            if os.path.isdir(filepath):
                s.append(filename)
        return render(request, caller+'/'+caller+'.html', {'s':s})
        
class PreviewCsvView(View):
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-3] # url like 127.0.0.1:8000/[caller]/[upload/output]
        method = referer.split('/')[-2]
        method = method.split('_')[-1].lower() # File_List_Output/File_List_Upload
        name = request.GET.get('File', None)
        directory_name = name.split(".")[-2]    
        if method == 'output':
            file_path = method+'/'+caller+'/'+directory_name+'/'+directory_name+'_output.csv'
        elif method == 'upload':
            file_path = method+'/'+caller+'/'+directory_name+'/'+name
        else:
            print("Exception")
        df = pd.read_csv(file_path)
        tables = df.head(2000).to_html()
        return JsonResponse(tables, safe=False)
        
    def post(self, request, *arg, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_form = FileModel()
            for file in request.FILES.getlist('file'):
                upload_form.file = file
                df = pd.read_csv(upload_form.file)
                if(df.shape[1] <= 4 and df.shape[0] <= 200):
                    tables = df.head(200).to_html()
                    return JsonResponse(tables, safe=False)
                else:
                    cln = str(df.shape[1])
                    row = str(df.shape[0])
                    return JsonResponse({"status":"錯誤","message":"欄數限制最多為4, 列數限制最多為200\n文件欄數："+ cln +", 列數："+ row + ", 不符合標準"}, status=400)
        form = UploadFileForm()
        return JsonResponse({"status":"錯誤","message":"表單格式錯誤"}, status=400)
    
class FileListView(View):
    def get(self, request, *arg, **kwargs):
        method = kwargs.get('method')
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-2] # url like 127.0.0.1:8000/[caller]/
        path = method+'/'+caller
        url = caller+'/file_list_'+method+'.html'
        s = []
        for directory_name in os.listdir(path):
            s.append(directory_name+'.csv')
        return render(request, url, {'s':s})
        
class DownloadView(View):
    def get(self, request, *arg, **kwargs):
        name = request.GET.get('File',None)
        directory_name = name.split(".")[-2]
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-3] # url like 127.0.0.1:8000/[caller]/[upload/output]
        file_path = 'output/'+caller+'/'+directory_name+'/'+directory_name+'_output.csv'
        df = pd.read_csv(file_path)
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' %name
        df.to_csv(path_or_buf=response,index=False,decimal=",")
        return response