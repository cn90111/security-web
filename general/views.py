from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.utils.translation import gettext
from django.urls import reverse

from general.machine_learning import MachineLearning
from general.function import Path
from general.function import ContentDetection
from general.exception import BreakProgramException
from pandas.io.parsers import ParserError
from general.models import ExecuteModel

from .models import FileModel
from .forms import UploadFileForm
from datetime import date, datetime

import urllib.parse

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
                if file.name.find(' ') != -1:
                    if file.name.split(' ')[-1] == '.csv':
                        return JsonResponse({'message':gettext("檔名不能以空白結尾")}, status=415)
                if self.more_than_file_size_limit(file, 4194304):
                    return JsonResponse({'message':gettext("檔案過大，不能超過 4 MB")}, status=415)
            mode = kwargs.get('mode')
            try:
                for file in files:
                    if mode == 'DPView':
                        check_result = self.dpsyn_check_file_limit(request, file)
                    elif mode == 'json':
                        check_result = self.json_check_file_limit(request, file)
                    elif mode == 't_Closeness':
                        check_result = self.t_Closeness_check_file_limit(request, file)
                    if check_result:
                        return check_result
            except Exception as e:
                print(e)
                return JsonResponse({'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
            else:
                return HttpResponse(status=204)
            return JsonResponse({'message':gettext('有尚未捕捉到的例外，請回報服務人員，謝謝')}, status=404)
        else:
            return JsonResponse({'message':gettext('檔案格式錯誤')}, status=415)
    
    def domain_check(self, dataframe):
        detection = ContentDetection()
        for column_title in dataframe:
            column = dataframe.loc[:, column_title].values.tolist()
            if detection.is_string(column):
                if len(list(filter(None, list(set(column))))) > 50:
                    return JsonResponse({'message':column_title + gettext(' 欄位 domain 過大，domain 大小限制在 50 以下')}, status=400)
                    
    def json_check_file_limit(self, request, file):
        upload_form = FileModel()
        upload_form.file = file
        try:
            df = pd.read_csv(upload_form.file, dtype=str)
            if df.iloc[0].name != 0:
                raise ParserError()
            if df.isnull().values.any():
                return JsonResponse({'message':gettext('此方法檔案中不能有空欄，請改為使用 DPView 進行去識別化')}, status=400)
        except ParserError as e:
            return JsonResponse({'message':gettext('檔案讀取錯誤，請確保檔案內容中沒有半形逗號存在')}, status=400)
        except UnicodeDecodeError as e:
            return JsonResponse({'message':gettext('檔案編碼錯誤，請確保檔案由UTF-8編碼')}, status=400)
        if(df.shape[1] <= 4 and df.shape[0] <= 200):
            check_result = self.domain_check(df)
            if check_result:
                return check_result
            self.handle_upload_file(request, file, df)
        else:
            cln = str(df.shape[1])
            row = str(df.shape[0])
            return JsonResponse({'message':gettext('欄數限制最多為4、列數限制最多為200，文件欄數：'+ cln +'、列數：'+ row + ', 不符合標準')}, status=400)
    
    def t_Closeness_check_file_limit(self, request, file):
        upload_form = FileModel()
        upload_form.file = file
        try:
            df = pd.read_csv(upload_form.file, dtype=str)
            if df.iloc[0].name != 0:
                raise ParserError()
            if df.isnull().values.any():
                return JsonResponse({'message':gettext('此方法檔案中不能有空欄，請改為使用 DPView 進行去識別化')}, status=400)
        except ParserError as e:
            return JsonResponse({'message':gettext('檔案讀取錯誤，請確保檔案內容中沒有半形逗號存在')}, status=400)
        except UnicodeDecodeError as e:
            return JsonResponse({'message':gettext('檔案編碼錯誤，請確保檔案由UTF-8編碼')}, status=400)
        if(df.shape[1] >= 3):
            check_result = self.domain_check(df)
            if check_result:
                return check_result
            self.handle_upload_file(request, file, df)
        else:
            cln = str(df.shape[1])
            return JsonResponse({"status":gettext("錯誤"),\
                "message":gettext("欄數限制最少為3，當前文件欄數為"+ cln +"，不符合標準")},\
                status=400)
                
    def dpsyn_check_file_limit(self, request, file):
        upload_form = FileModel()
        upload_form.file = file
        try:
            df = pd.read_csv(upload_form.file, dtype=str)
            if df.iloc[0].name != 0:
                raise ParserError()
        except ParserError as e:
            return JsonResponse({'message':gettext('檔案讀取錯誤，請確保檔案內容中沒有半形逗號存在')}, status=400)
        except UnicodeDecodeError as e:
            return JsonResponse({'message':gettext('檔案編碼錯誤，請確保檔案由UTF-8編碼')}, status=400)
        if(df.shape[1] >= 3):
            check_result = self.domain_check(df)
            if check_result:
                return check_result
            self.handle_upload_file(request, file, df)
        else:
            cln = str(df.shape[1])
            return JsonResponse({"status":gettext("錯誤"),\
                "message":gettext("欄數限制最少為3，當前文件欄數為"+ cln +"，不符合標準")},\
                status=400)
            
    def handle_upload_file(self, request, file, dataframe):
        path = Path()
        fs = FileSystemStorage()
        
        file_path = path.get_upload_path(request, file.name)
        directory_path = path.get_upload_directory(request, file.name)
        
        if fs.exists(file_path):
            fs.delete(file_path)
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        dataframe.to_csv(file_path, index=False)
        
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
        request_dict = self.set_url_path(request_dict, caller, file_name)
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['form'] = form
        return render(request, caller+'/'+caller+'.html', request_dict)
        
    def get_empty_form(self):
        raise AttributeError('應藉由子類別實作此方法，return form()')
        
    def set_url_path(self, request_dict, caller, file_name):
        request_dict['break_program_url'] = reverse(caller+':break_program')
        request_dict['show_progress_url'] = reverse(caller+':show_progress')
        request_dict['execute_url'] = reverse(caller+':execute')
        request_dict['finish_url'] = reverse(caller+':finish', args=[file_name])
        return request_dict

class AbstractMethodView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        caller = path.get_caller(request)
        username = request.user.get_username()
        file_name = str(request.GET.get('csv_name',None))
        form = self.get_form(request.GET)
        if ExecuteModel.objects.filter(user_name=username).exists():
            return JsonResponse({'message':gettext('您正在執行另一個檔案，檔名為:'+ExecuteModel.objects.get(user_name=username).file_name+'，若想執行目前的檔案，請先把另一個檔案關閉')}, status=423)
        else:
            ExecuteModel.objects.create(user_name=username, file_name=file_name, caller=caller, finish=False)
        if form.is_valid():
            try:
                self.method_run(request)
            except BreakProgramException as e:
                print(e)
                ExecuteModel.objects.filter(user_name=username).delete()
                return JsonResponse({'message':gettext('程式已終止')}, status=404)
            except Exception as e:
                print(e)
                ExecuteModel.objects.filter(user_name=username).delete()
                return JsonResponse({'message':gettext('程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務')}, status=404)
            else:
                ExecuteModel.objects.filter(user_name=username).update(finish=True)
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

class CheckFileStatus(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        username = request.user.get_username()
        try:
            file = ExecuteModel.objects.get(user_name=username)
            caller = file.caller
            request_dict = {}
            request_dict['finish'] = file.finish
            if file.finish:
                request_dict['url'] = reverse(caller+':finish', args=[file.file_name])
            if not file.finish:
                request_dict['url'] = reverse(caller+':execute_page', args=[file.file_name])
                request_dict['break_url'] = reverse(caller+':break_program')
            return JsonResponse(request_dict)
        except Exception as e:
            return JsonResponse(None, safe=False)

class AbstractBreakProgramView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        finish = False
        username = request.user.get_username()
        
        try:
            file = ExecuteModel.objects.get(user_name=username)
            self.break_program(file)
            file.delete()
            finish = True
            return JsonResponse(finish, safe=False)
        except Exception as e:
            return JsonResponse(finish, safe=False)
        
    def break_program(self, file):
        raise AttributeError('應藉由子類別實作此方法，method.break_program(file)')

class DisplayCsvView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        method = kwargs.get('method').lower()
        file_name = request.GET.get('File', None)
        caller = path.get_caller(request)
        
        if method == 'output':
            file_path = path.get_output_path(request, file_name, caller=caller)
        elif method == 'upload':
            file_path = path.get_upload_path(request, file_name, caller=caller)
        else:
            raise AttributeError(gettext('無此method：') + method)
        df = pd.read_csv(file_path, keep_default_na=False)
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
        df = pd.read_csv(file_path, keep_default_na=False)
        
        if caller == 't_Closeness':
            caller = 'k_Anonymity'
            
        download_name = caller+'_'+directory_name+'_output.csv'
        download_name = urllib.parse.quote(download_name)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=\"%s\"; filename*=utf-8''%s" %(download_name, download_name)
        df.to_csv(path_or_buf=response, index=False, decimal=',')
        return response
        
class FinishView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        caller = path.get_caller(request)
        username = request.user.get_username()
        ExecuteModel.objects.filter(user_name=username).delete()
        
        request_dict = {}
        request_dict = self.set_url_path(request_dict, caller, file_name)
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        return render(request, 'general/execute_finish.html', request_dict)
        
    def set_url_path(self, request_dict, caller, file_name):
        request_dict['download_output_url'] = reverse(caller+':download_output', args=[file_name])
        request_dict['utility_page_url'] = reverse(caller+':utility_page', args=[file_name])
        request_dict['execute_page_url'] = reverse(caller+':execute_page', args=[file_name])
        request_dict['upload_display_url'] = reverse(caller+':display', args=['upload'])
        request_dict['output_display_url'] = reverse(caller+':display', args=['output'])
        return request_dict
        
class UtilityPageView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')
        caller = path.get_caller(request)
        
        request_dict = {}
        request_dict = self.set_url_path(request_dict, caller, file_name)
        request_dict['file_name'] = file_name
        request_dict['caller'] = caller
        request_dict['machine_learning_list'] = MachineLearning.SUPPORT_LIST
        return render(request, 'general/utility.html', request_dict)
         
    def set_url_path(self, request_dict, caller, file_name):
        request_dict['download_output_url'] = reverse(caller+':download_output', args=[file_name])
        request_dict['check_utility_url'] = reverse(caller+':check_utility')
        return request_dict
        
class CheckUtilityView(View):        
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        path = Path()
        
        caller = path.get_caller(request)
        machine_learning_method = request.GET.get('machine_learning_method', None)
        machine_learning_mode = request.GET.get('machine_learning_mode', None)
        train_file_path = request.GET.get('train_file_path', None)
        test_file_path = request.GET.get('test_file_path', None)
        file_name = request.GET.get('csv_name', None)
        
        train_file_path = self.get_full_path(train_file_path, request, file_name)
        test_file_path = self.get_full_path(test_file_path, request, file_name)
        
        accuracy = 0
        try:
            ml = MachineLearning(machine_learning_method, machine_learning_mode, train_file_path, test_file_path);
            ml.fit()
            if machine_learning_mode == 'classification': 
                accuracy = ml.score() * 100
            elif machine_learning_mode == 'regression': 
                accuracy = ml.score()
        except ValueError as e:
            print(e)
            return JsonResponse({'accuracy':accuracy, 'message':gettext('程式執行失敗，請嘗試切換模型預測目標，若仍然失敗，請聯絡服務人員為您服務')}, status=404)
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
        caller = path.get_caller(request)
        file_path = path.get_upload_path(request, file_name,caller=caller)
        
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
        if dataframe.shape[1] == 1:
            return JsonResponse({'message':gettext('經由系統偵測，此檔案分隔符號錯誤，CSV檔案應由逗號分隔資料，請藉由另存新檔選CSV，以符合CSV應有的格式')}, status=200)
        for column_title in dataframe:
            element = set(dataframe.loc[:, column_title].values.tolist())
            if column_title in element:
                return JsonResponse({'message':gettext('經由系統偵測，此檔案沒有標題列，可能導致去識別化結果不如預期，若為系統誤判則不需理會')}, status=200)
                
class UpdateLogView(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'general/update_log.html', {})