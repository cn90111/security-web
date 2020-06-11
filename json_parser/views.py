from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from general.function import NumberDataframe
from general.function import Path

from .forms import UploadFileForm
from json_parser.json_parser import JsonParser
import json

class ParserView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        
        file_path = str(request.GET.get('path', None))
        file_name = json.loads(request.GET.get('csv_name', None))
        structure_mode = json.loads(request.GET.get('structure_mode', None))
        structure_dict = json.loads(request.GET.get('structure_dict', None))
        number_dict = request.GET.get('number_dict', None)
        username = request.user.get_username()
        file_path = file_path+username+'/'
        try:
            for file in file_name:
                if number_dict:
                    number_dict = json.loads(number_dict)
                    parser.create_json_file(file_path, file,
                        structure_mode[file], structure_dict[file], number_dict=number_dict)
                else:
                    parser.create_json_file(file_path, file,
                        structure_mode[file], structure_dict[file])
        except Exception as e:
            print(e)
            return JsonResponse({"message":"程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務"}, status=404)
        else:
            return HttpResponse(status=204)
        return JsonResponse({"message":"有尚未捕捉到的例外，請回報服務人員，謝謝"}, status=404)
    
class CustomView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        file_string_element_dict = {} # file_name - column_title - element
        caller = path.get_caller(request)
        file_name = kwargs.get('csv_name')
        request_dict = {}
        
        file_path = path.get_upload_path(request, file_name)
        file_string_element_dict[file_name] \
            = parser.get_file_string_element(file_path)
                
        request_dict['file_string_element_dict'] = file_string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        return render(request, 'general/parameter_custom.html', request_dict)
        
class AdvancedSettingsView(CustomView):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        number_data_frame = NumberDataframe()
        
        file_string_element_dict = {} # file_name - column_title - element
        username = request.user.get_username()
        caller = path.get_caller(request)
        file_name = kwargs.get('csv_name')
        request_dict = {}
        
        file_path = path.get_upload_path(request, file_name)
        file_string_element_dict[file_name] \
            = parser.get_file_string_element(file_path)
        number_title_list = number_data_frame.get_number_title(file_path)
        max_value_dict, min_value_dict = number_data_frame.get_number_limit(file_path, number_title_list)
        max_interval_quantity_dict = number_data_frame.get_max_interval_quantity(max_value_dict, min_value_dict)
            
        request_dict['file_string_element_dict'] = file_string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        request_dict['advanced_settings'] = True
        request_dict['number_title_list'] = number_title_list
        request_dict['max_value_dict'] = max_value_dict
        request_dict['min_value_dict'] = min_value_dict
        request_dict['max_interval_quantity_dict'] = max_interval_quantity_dict
        return render(request, 'general/parameter_custom.html', request_dict)