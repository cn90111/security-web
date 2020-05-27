from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from general.machine_learning import MachineLearning
from .models import FileModel
from .forms import UploadFileForm
from datetime import date, datetime

import os
import logging
import pandas as pd

today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

class FileView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        root_path = settings.UPLOAD_ROOT+caller+'/'+username+'/'
        finish = False
        if form.is_valid():
            try:
                for file in files:
                    check_result = self.check_file_limit(file)
                    if check_result:
                        return check_result
                    self.handle_upload_file(file, root_path)
            except Exception as e:
                print(e)
            else:
                finish = True
            return JsonResponse(finish, safe=False)
        else:
            form = UploadFileForm()
            return JsonResponse({"status":"錯誤","message":"表單格式錯誤"}, status=400)

    def check_file_limit(self, file):
        upload_form = FileModel()
        upload_form.file = file
        df = pd.read_csv(upload_form.file)
        if(df.shape[1] <= 4 and df.shape[0] <= 200):
            return None
        else:
            cln = str(df.shape[1])
            row = str(df.shape[0])
            return JsonResponse({"status":"錯誤","message":"欄數限制最多為4, 列數限制最多為200\n文件欄數："+ cln +", 列數："+ row + ", 不符合標準"}, status=400)

    def handle_upload_file(self, f, root_path):
        fs = FileSystemStorage()
        directory_path = root_path+f.name.split(".")[-2]+'/'
        file_path = directory_path+f.name
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, f)
        

class ExecuteView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        path = settings.UPLOAD_ROOT+caller+'/'+username+'/'
        file_name = kwargs.get('csv_name')
        
        request_dict = {}
        request_dict['file_name'] = file_name
        return render(request, caller+'/'+caller+'.html', request_dict)

class DisplayCsvView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        method = kwargs.get('method').lower()
        name = request.GET.get('File', None)
        directory_name = name.split(".")[-2]
        if method == 'output':
            file_path = settings.OUTPUT_ROOT+caller+'/'+username+'/'+directory_name+'/'+directory_name+'_output.csv'
        elif method == 'upload':
            file_path = settings.UPLOAD_ROOT+caller+'/'+username+'/'+directory_name+'/'+name
        else:
            raise AttributeError("無此method：" + method)
        df = pd.read_csv(file_path)
        tables = df.head(200).to_html()
        return JsonResponse(tables, safe=False)

class FileListView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        method = kwargs.get('method').lower()
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        path = method+'/'+caller+'/'+username+'/'
        url = 'general/file_list_'+method+'.html'
        s = []
        for directory_name in os.listdir(path):
            s.append(directory_name+'.csv')
        
        request_dict = {}
        request_dict['s'] = s
        request_dict['caller'] = caller
        return render(request, url, request_dict)

class DownloadView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        directory_name = file_name.split(".")[-2]
        file_name = directory_name + '_output.csv'
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        file_path = settings.OUTPUT_ROOT+caller+'/'+username+'/'+directory_name+'/'+file_name
        df = pd.read_csv(file_path)
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' %caller+'_'+file_name
        df.to_csv(path_or_buf=response,index=False,decimal=",")
        return response
        
class FinishView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        
        request_dict = {}
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        return render(request, 'general/execute_finish.html', request_dict)
        
class UtilityPageView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        request_dict = {}
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        request_dict['machine_learning_list'] = MachineLearning.SUPPORT_LIST
        return render(request, 'general/utility.html', request_dict)
        
class CheckUtilityView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        username = request.user.get_username()
        
        file_name = request.GET.get('csv_name',None)
        directory_name = file_name.split(".")[-2]
        machine_learning_method = request.GET.get('machine_learning_method',None)
        file_path = request.GET.get('file_path',None)
        
        if file_path == 'output':
            file_path = file_path+"/"+caller+"/"+username+"/"+directory_name+"/"+directory_name+"_output.csv"
        elif file_path == 'upload':
            file_path = file_path+"/"+caller+"/"+username+"/"+directory_name+"/"+file_name
        else:
            raise AttributeError("無此file_path：" + file_path)
        
        finish = False
        accuracy = 0
        try:
            ml = MachineLearning(machine_learning_method, file_path);
            ml.fit()
            accuracy = ml.score() * 100
        except Exception as e:
            print(e)
        else:
            finish = True
        return JsonResponse({'finish':finish,'accuracy':accuracy})