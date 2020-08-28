import pandas as pd
from django.conf import settings
from django.utils.html import escape
from general.models import ExecuteModel

class Path():        
    def get_caller(self, request):
        try:
            username = request.user.get_username()
            file = ExecuteModel.objects.get(user_name=username)
            return file.caller
        except Exception as e:
            referer = request.META.get('HTTP_REFERER')
            caller = referer.split('/')[4] # url like http://127.0.0.1:8000/language/[caller]/
            return caller
        
    def get_output_path(self, request, file_name):
        directory_name = file_name.split(".")[-2]
        return self.get_output_directory()+directory_name+'_output.csv'
        
    def get_output_directory(self, request, file_name):
        file_root = self.get_output_root(request)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_upload_path(self, request, file_name):
        return self.get_upload_directory(request, file_name)+file_name
        
    def get_upload_directory(self, request, file_name):
        file_root = self.get_upload_root(request)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_output_root(self, request):
        return self._get_root('output', request)
    
    def get_upload_root(self, request):
        return self._get_root('upload', request)
        
    def _get_root(self, mode, request):
        if mode == 'upload':
            root = settings.UPLOAD_ROOT
        elif mode == 'output':
            root = settings.OUTPUT_ROOT
        caller = self.get_caller(request)
        username = request.user.get_username()
        return root+caller+'/'+username+'/'

class NumberDataframe():
    def get_number_title(self, file_path):
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        number_title_list = []
        for column_title in dataframe:
            data = None
            i = 0
            while not data and i < dataframe.shape[0]:
                data = dataframe.loc[i, column_title]
                i = i + 1
            try:
                float(data)
                number_title_list.append(column_title)
            except ValueError:
                pass
        return number_title_list
        
    def get_number_limit(self, file_path, number_title_list):
        max_value_dict = {}
        min_value_dict = {}
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        for number_title in number_title_list:
            data = dataframe.loc[:, number_title].values.tolist()
            max_value_dict[number_title] = max(data)
            min_value_dict[number_title] = min(data)
        return max_value_dict, min_value_dict