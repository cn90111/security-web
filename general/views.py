from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.utils.translation import gettext

from general.machine_learning import MachineLearning
from general.function import Path
from general.exception import BreakProgramException

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
        if form.is_valid():
            for file in files:
                if self.more_than_file_size_limit(file, 1048576):
                    return JsonResponse({'message':gettext("檔案過大，不能超過 1 MB")}, status=415)
            mode = kwargs.get('mode')
            try:
                for file in files:
                    if mode == 'DPSyn':
                        check_result = self.dpsyn_check_file_limit(file)
                    if mode == 'json':
                        check_result = self.json_check_file_limit(file)
                    if check_result:
                        return check_result
                    self.handle_upload_file(request, file)
            except Exception as e:
                print(e)
                return JsonResponse({'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
            else:
                return HttpResponse(status=204)
            return JsonResponse({'message':gettext('有尚未捕捉到的例外，請回報服務人員，謝謝')}, status=404)
        else:
            return JsonResponse({'message':gettext('檔案格式錯誤')}, status=415)

    def json_check_file_limit(self, file):
        upload_form = FileModel()
        upload_form.file = file
        df = pd.read_csv(upload_form.file)
        if(df.shape[1] <= 4 and df.shape[0] <= 200):
            return None
        else:
            cln = str(df.shape[1])
            row = str(df.shape[0])
            return JsonResponse({'message':gettext('欄數限制最多為4, 列數限制最多為200\n文件欄數：'+ cln +', 列數：'+ row + ', 不符合標準')}, status=400)
    
    def dpsyn_check_file_limit(self, file):
        upload_form = FileModel()
        upload_form.file = file
        df = pd.read_csv(upload_form.file)
        if(df.shape[1] >= 3):
            return None
        else:
            cln = str(df.shape[1])
            return JsonResponse({"status":gettext("錯誤"),\
                "message":gettext("欄數限制最少為3\n文件欄數："+ cln +", 不符合標準")},\
                status=400)
            
    def handle_upload_file(self, request, f):
        path = Path()
        fs = FileSystemStorage()
        
        file_path = path.get_upload_path(request, f.name)
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, f)
        
    def more_than_file_size_limit(self, file, byte):
        if file.size > byte:
            return True
        return False

class AbstractExecuteView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        caller = path.get_caller(request)
        file_name = kwargs.get('csv_name')
        form = self.get_empty_form()
        
        request_dict = {}
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['form'] = form
        return render(request, caller+'/'+caller+'.html', request_dict)
        
    def get_empty_form(self):
        raise AttributeError('應藉由子類別實作此方法，return form()')

class AbstractMethodView(View):
    execute_pair = {}
    
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        username = request.user.get_username()
        file_name = str(request.GET.get('csv_name',None))
        form = self.get_form(request.GET)
        if username in self.execute_pair:
            return JsonResponse({'message':gettext('您正在執行另一個檔案，檔名為:'+self.execute_pair[username]+'，若想執行目前的檔案，請先把另一個檔案關閉')}, status=423)
        else:
            self.execute_pair[username] = file_name
            
        if form.is_valid():
            try:
                self.method_run(request)
            except BreakProgramException as e:
                print(e)
                self.execute_pair.pop(username, None)
                return JsonResponse({'message':gettext('程式已終止')}, status=404)
            except Exception as e:
                print(e)
                self.execute_pair.pop(username, None)
                return JsonResponse({'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
            else:
                self.execute_pair.pop(username, None)
                return HttpResponse(status=204)
            return JsonResponse({'message':gettext('有尚未捕捉到的例外，請回報服務人員，謝謝')}, status=404)
        else:
            return JsonResponse({'message':gettext('表單格式錯誤')}, status=400)
    
    def get_form(self, requestContent):
        raise AttributeError('應藉由子類別實作此方法，return form(requestContent)')
        
    def method_run(self, request):
        raise AttributeError('應藉由子類別實作此方法，method.run(request)')
        
    def get_method_template(self):
        raise AttributeError('應藉由子類別實作此方法，return template_url')

class AbstractBreakProgramView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        finish = False
        self.break_program()
        finish = True
        return JsonResponse(finish, safe=False)
        
    def break_program(self):
        raise AttributeError('應藉由子類別實作此方法，method.break_program()')

class DisplayCsvView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        method = kwargs.get('method').lower()
        file_name = request.GET.get('File', None)
        
        if method == 'output':
            file_path = path.get_output_path(request, file_name)
        elif method == 'upload':
            file_path = path.get_upload_path(request, file_name)
        else:
            raise AttributeError(gettext('無此method：') + method)
        df = pd.read_csv(file_path)
        tables = df.head(200).to_html()
        return JsonResponse(tables, safe=False)

class DownloadView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        directory_name = file_name.split('.')[-2]
        username = request.user.get_username()
        caller = path.get_caller(request)
        file_path = path.get_output_path(request, file_name)
        df = pd.read_csv(file_path)
        
        if caller == 'DPSyn':
            caller = 'DPView'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' %caller+'_'+directory_name+'_output.csv'
        df.to_csv(path_or_buf=response,index=False,decimal=',')
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
        machine_learning_method = request.GET.get('machine_learning_method', None)
        train_file_path = request.GET.get('train_file_path', None)
        test_file_path = request.GET.get('test_file_path', None)
        file_name = request.GET.get('csv_name', None)
        
        train_file_path = self.get_full_path(train_file_path, request, file_name)
        test_file_path = self.get_full_path(test_file_path, request, file_name)
        
        accuracy = 0
        try:
            ml = MachineLearning(machine_learning_method, train_file_path, test_file_path);
            ml.fit()
            accuracy = ml.score() * 100
        except Exception as e:
            print(e)
            return JsonResponse({'accuracy':accuracy, 'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
        else:
            return JsonResponse({'accuracy':accuracy}, status=200)
        return JsonResponse({'message':gettext('有尚未捕捉到的例外，請回報服務人員，謝謝')}, status=404)

    def get_full_path(self, file_path, request, file_name):
        path = Path()
        if file_path == 'output':
            return path.get_output_path(request, file_name)
        elif file_path == 'upload':
            return path.get_upload_path(request, file_name)
        else:
            raise AttributeError(gettext('無此file_path：') + file_path)

class TitleCheckView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = request.GET.get('csv_name', None)
        file_path = path.get_upload_path(request, file_name)
        
        try:
            df = pd.read_csv(file_path)
            result = self.title_check(df)
            if result:
                return result
        except Exception as e:
            print(e)
            return JsonResponse({'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
        else:
            return HttpResponse(status=204)
        return JsonResponse({'message':gettext('有尚未捕捉到的例外，請回報服務人員，謝謝')}, status=404)    
    
    def title_check(self, dataframe):
        for column_title in dataframe:
            element = set(dataframe.loc[:, column_title].values.tolist())
            if column_title in element:
                return JsonResponse({'message':gettext('經由系統偵測，此檔案沒有標題列，可能導致去識別化結果不如預期，若為系統誤判則不需理會')}, status=200)