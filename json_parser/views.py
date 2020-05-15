from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from general.views import FileView

from .forms import UploadFileForm
from json_parser.json_parser import JsonParser
import json

class ParserView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        finlish = False
        parser = JsonParser()
        file_path = str(request.GET.get('path', None))
        csv_file_name = json.loads(request.GET.get('csv_name', None))
        structure_mode = json.loads(request.GET.get('structure_mode', None))
        structure_dict = json.loads(request.GET.get('structure_dict', None))
        username = request.user.get_username()
        file_path = file_path+username+'/'
        for file in csv_file_name:
            parser.create_json_file(file_path, file,
                structure_mode[file], structure_dict[file])
        finlish = True
        return JsonResponse(finlish, safe=False)

class JsonFileView(FileView):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        file_string_element_dict = {} # file_name - column_title - element
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        file_path = settings.UPLOAD_ROOT+caller+'/'+username+'/'
        file_name = kwargs.get('csv_name')
        file_name = file_name.split(',')
        request_dict = {}
        
        for name in file_name:
            file_string_element_dict[name] = parser.get_file_string_element\
                    (file_path+name.split(".")[-2]+'/'+name)
        request_dict['file_string_element_dict'] = file_string_element_dict
        request_dict['caller'] = caller
        return render(request, 'json_parser/json_parser.html', request_dict)
    
    @method_decorator(login_required)
    def post(self, request):
        parser = JsonParser()
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        caller = referer.split('/')[3] # url like http://127.0.0.1:8000/[caller]/
        root_path = settings.UPLOAD_ROOT+caller+'/'+username+'/'
        finlish = True
        if form.is_valid():
            for f in files:
                self.handle_upload_file(f, root_path)
                element_dict = parser.get_file_string_element\
                    (root_path+f.name.split(".")[-2]+'/'+f.name)
                if element_dict:
                    finlish = False
            if finlish:
                for f in files:
                    parser.create_json_file(root_path, f.name, {}, {})
            return JsonResponse(finlish, safe=False)
        else:
            form = UploadFileForm()