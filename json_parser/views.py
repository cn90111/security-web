from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View

from .forms import UploadFileForm
from json_parser.json_parser import JsonParser
import json

class ParserView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        finish = False
        parser = JsonParser()
        file_path = str(request.GET.get('path', None))
        csv_file_name = json.loads(request.GET.get('csv_name', None))
        structure_mode = json.loads(request.GET.get('structure_mode', None))
        structure_dict = json.loads(request.GET.get('structure_dict', None))
        username = request.user.get_username()
        file_path = file_path+username+'/'
        try:
            for file in csv_file_name:
                parser.create_json_file(file_path, file,
                    structure_mode[file], structure_dict[file])
        except Exception as e:
            print(e)
        else:
            finish = True
        return JsonResponse(finish, safe=False)
    
class CustomView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        file_string_element_dict = {} # file_name - column_title - element
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        file_path = settings.UPLOAD_ROOT+caller+'/'+username+'/'
        file_name = kwargs.get('csv_name')
        request_dict = {}
        
        file_string_element_dict[file_name] = parser.get_file_string_element\
                (file_path+file_name.split(".")[-2]+'/'+file_name)
        request_dict['file_string_element_dict'] = file_string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        return render(request, 'general/parameter_custom.html', request_dict)