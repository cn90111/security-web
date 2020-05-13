from django.shortcuts import render
from django.http import JsonResponse
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.conf import settings
from .models import FileModel
from .forms import UploadFileForm
import os
import logging
import pandas as pd

today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

class FileView(View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        root_path = settings.UPLOAD_ROOT+caller+'/'
        finlish = False
        if form.is_valid():
            for f in files:
                self.handle_upload_file(f, root_path) 
            finlish = True
            return JsonResponse(finlish, safe=False)
        else:
            form = UploadFileForm()
                
    def handle_upload_file(self, f, root_path):
        fs = FileSystemStorage()
        directory_path = root_path+f.name.split(".")[-2]+'/'
        file_path = directory_path+f.name
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, f)
        
class ExecuteView(View):
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        path =  settings.UPLOAD_ROOT+caller+'/'
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
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        method = kwargs.get('method')
        name = request.GET.get('File', None)
        directory_name = name.split(".")[-2]    
        if method == 'Output':
            file_path = settings.OUTPUT_ROOT+caller+'/'+directory_name+'/'+directory_name+'_output.csv'
        elif method == 'Upload':
            file_path = settings.UPLOAD_ROOT+caller+'/'+directory_name+'/'+name
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
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        path = method+'/'+caller
        url = 'general/file_list_'+method+'.html'
        s = []
        for directory_name in os.listdir(path):
            s.append(directory_name+'.csv')
        return render(request, url, {'s':s,'caller':caller})
        
class DownloadView(View):
    def get(self, request, *arg, **kwargs):
        name = request.GET.get('File',None)
        directory_name = name.split(".")[-2]
        name = directory_name + '_output.csv'
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        file_path = settings.OUTPUT_ROOT+caller+'/'+directory_name+'/'+name
        df = pd.read_csv(file_path)
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' %caller+'_'+name
        df.to_csv(path_or_buf=response,index=False,decimal=",")
        return response