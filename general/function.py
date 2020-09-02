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
            if request.resolver_match.app_names:
                caller = request.resolver_match.app_names[0] # get app_names
            return caller
        
    def get_output_path(self, request, file_name, caller=None):
        directory_name = file_name.split(".")[-2]
        return self.get_output_directory(request, file_name, caller=caller)\
                +directory_name+'_output.csv'
        
    def get_output_directory(self, request, file_name, caller=None):
        file_root = self.get_output_root(request, caller)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_upload_path(self, request, file_name, caller=None):
        return self.get_upload_directory(request, file_name, caller=caller)+file_name
        
    def get_upload_directory(self, request, file_name, caller=None):
        file_root = self.get_upload_root(request, caller)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_output_root(self, request, caller=None):
        return self._get_root('output', request, caller=caller)
    
    def get_upload_root(self, request, caller=None):
        return self._get_root('upload', request, caller=caller)
        
    def _get_root(self, mode, request, caller=None):
        if mode == 'upload':
            root = settings.UPLOAD_ROOT
        elif mode == 'output':
            root = settings.OUTPUT_ROOT
        if not caller:
            caller = self.get_caller(request)
        username = request.user.get_username()
        return root+caller+'/'+username+'/'

class ContentDetection():
    def get_item(self, item_list):
        if not item_list:
            return False
        for item in item_list:
            if not item:
                continue
            return item
        return False

    def is_string(self, item_list):
        item = self.get_item(item_list)
        if not item:
            return False
        try:
            float(item)
            return False
        except ValueError:
            return True
        
    def is_number(self, item_list):
        item = self.get_item(item_list)
        if not item:
            return False
        try:
            float(item)
            return True
        except ValueError:
            return False
    
    def is_float(self, item_list):
        if not self.is_number(item_list):
            return False
        item = self.get_item(item_list)
        if type(item) is float:
            return True
        if type(item) is str and item.find('.') != -1:
            return True
        return False

class NumberDataframe():
    def __init__(self, file_path):
        self.dataframe = pd.read_csv(file_path, keep_default_na=False)
        self.detection = ContentDetection()
    
    def get_number_title(self):
        number_title_list = []
        for column_title in self.dataframe:
            if self.detection.is_number(self.dataframe.loc[:, column_title].values.tolist()):
                number_title_list.append(column_title)
        return number_title_list
        
    def get_number_limit(self, number_title_list, number_type_pair=None):
        max_value_dict = {}
        min_value_dict = {}
        for number_title in number_title_list:
            data = self.dataframe.loc[:, number_title].values.tolist()
            data = list(filter(None, data))
            if number_type_pair:
                if(number_type_pair[number_title] == 'float'):
                    max_value_dict[number_title] = float(max(data))
                    min_value_dict[number_title] = float(min(data))
                elif(number_type_pair[number_title] == 'int'):
                    max_value_dict[number_title] = int(max(data))
                    min_value_dict[number_title] = int(min(data))
                else:
                    raise Exception('number_type_pair error')
            else:
                if self.detection.is_float(self.dataframe.loc[:, number_title].values.tolist()):
                    max_value_dict[number_title] = float(max(data))
                    min_value_dict[number_title] = float(min(data))
                else:
                    max_value_dict[number_title] = int(max(data))
                    min_value_dict[number_title] = int(min(data))
        return max_value_dict, min_value_dict
        
    def get_number_type_pair(self, number_title_list):
        number_type_pair = {}
        for number_title in number_title_list:
            data = self.dataframe.loc[:, number_title].values.tolist()
            data = list(filter(None, data))
            if self.detection.is_float(self.dataframe.loc[:, number_title].values.tolist()):
                number_type_pair[number_title] = 'float'
            else:
                number_type_pair[number_title] = 'int'
        return number_type_pair