from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.urls import reverse
from django.views import View

from general.function import NumberDataframe
from general.function import Path
from general.exception import PairLoopException

from .forms import UploadFileForm
from json_parser.json_parser import JsonParser
import json

class ParserView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        file_name = request.GET.get('csv_name', None)
        structure_mode = json.loads(request.GET.get('structure_mode', None))
        structure_dict = json.loads(request.GET.get('structure_dict', None))
        number_title_pair_dict = request.GET.get('number_title_pair_dict', None)
        interval_dict = request.GET.get('interval_dict', None)
        file_path = path.get_upload_root(request)
        try:
            for key in structure_mode:
                if structure_mode[key] == 'custom':
                    structure_dict[key] = self.pair_check(structure_dict[key])
            
            if number_title_pair_dict:
                number_title_pair_dict = json.loads(number_title_pair_dict)
                interval_dict = json.loads(interval_dict)
                parser.create_json_file(file_path, file_name,
                    structure_mode, structure_dict,
                    number_title_pair_dict=number_title_pair_dict,
                    interval_dict=interval_dict)
            else:
                parser.create_json_file(file_path, file_name,
                    structure_mode, structure_dict)
        except PairLoopException as e:
            print(e)
            return JsonResponse({"message":str(e)}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message":gettext("程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務")}, status=404)
        else:
            return HttpResponse(status=204)
        return JsonResponse({"message":gettext("有尚未捕捉到的例外，請回報服務人員，謝謝")}, status=404)
    
    def pair_check(self, pair_dict):
        for key in list(pair_dict.keys()):
            value = pair_dict[key]
            previous_value = value
            ancestor_set = set()
            ancestor_set.add(value)
            while value in pair_dict:
                value = pair_dict[value]
                if previous_value == value:
                    return pair_dict
                if value in ancestor_set:
                    temp = ""
                    for element in ancestor_set:
                        temp = temp + element + ', '
                    raise PairLoopException(gettext("配對關係出現循環，將導致程式無限執行，請重新配對：") + temp)
                previous_value = value
                ancestor_set.add(value)
            pair_dict[value] = value
        return pair_dict

class DPViewParserView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        file_path = str(request.GET.get('path', None))
        file_name = str(request.GET.get('csv_name',None))
        pair_dict = json.loads(request.GET.get('number_title_pair_dict', None))
        interval_dict = request.GET.get('interval_dict', None)
        file_path = path.get_upload_root(request)
        
        try:
            if interval_dict:
                interval_dict = json.loads(interval_dict)
                parser.create_DPView_json_file(file_path, file_name,
                    pair_dict, interval_dict=interval_dict)
            else:
                parser.create_DPView_json_file(file_path, file_name, pair_dict)
        except Exception as e:
            print(e)
            return JsonResponse({"message":gettext("程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務")}, status=404)
        else:
            return HttpResponse(status=204)
        return JsonResponse({"message":gettext("有尚未捕捉到的例外，請回報服務人員，謝謝")}, status=404)
        
class CustomView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        string_element_dict = {} # column_title - element
        
        file_name = kwargs.get('csv_name')
        if not file_name:
            return redirect('home')
        caller = path.get_caller(request)
        file_path = path.get_upload_path(request, file_name)
        string_element_dict = parser.get_file_string_element(file_path)
              
        request_dict = {}  
        request_dict = self.set_url_path(request_dict, caller, file_name)        
        request_dict['string_element_dict'] = string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        return render(request, 'general/parameter_custom.vue', request_dict)
        
    def set_url_path(self, request_dict, caller, file_name):
        request_dict['advanced_settings_url'] = reverse(caller+':advanced_settings', args=[file_name])
        request_dict['base_settings_url'] = reverse(caller+':custom')+file_name        
        request_dict['previous_page_url'] = reverse(caller+':home')
        request_dict['execute_url'] = reverse(caller+':execute_page', args=[file_name])
        request_dict['upload_display_url'] = reverse('display', args=['upload'])
        return request_dict

class AdvancedSettingsView(CustomView):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        number_data_frame = NumberDataframe()
        
        string_element_dict = {} # column_title - element
        username = request.user.get_username()
        caller = path.get_caller(request)
        file_name = kwargs.get('csv_name')
        
        file_path = path.get_upload_path(request, file_name)
        string_element_dict = parser.get_file_string_element(file_path)
        number_title_list = number_data_frame.get_number_title(file_path)
        max_value_dict, min_value_dict = number_data_frame.get_number_limit(file_path, number_title_list)
           
        request_dict = {}
        request_dict = self.set_url_path(request_dict, caller, file_name)  
        request_dict['string_element_dict'] = string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        request_dict['advanced_settings'] = True
        request_dict['number_title_list'] = number_title_list
        request_dict['max_value_dict'] = max_value_dict
        request_dict['min_value_dict'] = min_value_dict
        return render(request, 'general/parameter_custom.vue', request_dict)