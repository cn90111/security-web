from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings

from general.machine_learning import MachineLearning
from general.function import Path

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
    def post(self, request, *arg, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        
        finish = False
        if form.is_valid():
            try:
                for file in files:
                    check_result = self.check_file_limit(file)
                    if check_result:
                        return check_result
                    self.handle_upload_file(request, file)
            except Exception as e:
                print(e)
            else:
                finish = True
            return JsonResponse(finish, safe=False)
        else:
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

    def handle_upload_file(self, request, f):
        path = Path()
        fs = FileSystemStorage()
        
        file_path = path.get_upload_path(request, f.name)
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, f)
        

class AbstractExecuteView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        username = request.user.get_username()
        caller = path.get_caller(request)
        file_name = kwargs.get('csv_name')
        form = self.get_empty_form()
        
        request_dict = {}
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['form'] = form
        return render(request, caller+'/'+caller+'.html', request_dict)
        
    def get_empty_form(self):
        raise AttributeError("應藉由子類別實作此方法，return form()")

class AbstractMethodView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        username = request.user.get_username()
        file_name = str(request.GET.get('csv_name',None))
        form = self.get_form(request.GET)
        
        finish = False
        if form.is_valid():
            try:
                self.method_run(request)
            except Exception as e:
                print(e)
            else:
                finish = True
            return JsonResponse(finish, safe=False)
        else:
            return JsonResponse(finish, safe=False)
    
    def get_form(self, requestContent):
        raise AttributeError("應藉由子類別實作此方法，return form(requestContent)")
        
    def method_run(self, request):
        raise AttributeError("應藉由子類別實作此方法，method.run(request)")
        
    def get_method_template(self):
        raise AttributeError("應藉由子類別實作此方法，return template_url")

class DisplayCsvView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        username = request.user.get_username()
        caller = path.get_caller(request)
        method = kwargs.get('method').lower()
        file_name = request.GET.get('File', None)
        
        if method == 'output':
            file_path = path.get_output_path(request, file_name)
        elif method == 'upload':
            file_path = path.get_upload_path(request, file_name)
        else:
            raise AttributeError("無此method：" + method)
        df = pd.read_csv(file_path)
        tables = df.head(200).to_html()
        return JsonResponse(tables, safe=False)

class FileListView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        method = kwargs.get('method').lower()
        username = request.user.get_username()
        caller = path.get_caller(request)
        s = []
        
        url = 'general/file_list_'+method+'.html'
        root = method+'/'+caller+'/'+username+'/'
        for directory_name in os.listdir(root):
            s.append(directory_name+'.csv')
        
        request_dict = {}
        request_dict['s'] = s
        request_dict['caller'] = caller
        return render(request, url, request_dict)

class DownloadView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        directory_name = file_name.split(".")[-2]
        username = request.user.get_username()
        caller = path.get_caller(request)
        file_path = path.get_output_path(request, file_name)
        df = pd.read_csv(file_path)
        
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' %caller+'_'+directory_name+'_output.csv'
        df.to_csv(path_or_buf=response,index=False,decimal=",")
        return response
        
class FinishView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        caller = path.get_caller(request)
        
        request_dict = {}
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        return render(request, 'general/execute_finish.html', request_dict)
        
class UtilityPageView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        caller = path.get_caller(request)
        
        request_dict = {}
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        request_dict['machine_learning_list'] = MachineLearning.SUPPORT_LIST
        return render(request, 'general/utility.html', request_dict)
        
class CheckUtilityView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        caller = path.get_caller(request)
        machine_learning_method = request.GET.get('machine_learning_method',None)
        file_path = request.GET.get('file_path',None)
        file_name = request.GET.get('csv_name',None)
        
        if file_path == 'output':
            file_path = path.get_output_path(request, file_name)
        elif file_path == 'upload':
            file_path = path.get_upload_path(request, file_name)
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