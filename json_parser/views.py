from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.http import JsonResponse

from .forms import UploadFileForm
from json_parser.json_parser import JsonParser
import json

# Create your views here.
class ParserView(View):
    def get(self, request, *arg, **kwargs):
        finlish = False
        parser = JsonParser()
        file_path = str(request.GET.get('path', None))
        csv_file_name = json.loads(request.GET.get('csv_name', None))
        structure_mode = json.loads(request.GET.get('structure_mode', None))
        structure_dict = json.loads(request.GET.get('structure_dict', None))
        for file in csv_file_name:
            parser.create_json_file(file_path, file,
                structure_mode[file], structure_dict[file])
        finlish = True
        return JsonResponse(finlish, safe=False)
        

class FileView(View):
    def get(self, request, *arg, **kwargs):
        parser = JsonParser()
        file_string_element_dict = {} # file_name - column_title - element
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-2] # url like 127.0.0.1:8000/[caller]/
        file_path = 'upload/'+caller+'/'        
        file_name = kwargs.get('csv_name')
        file_name = file_name.split(',')
        request_dict = {}
        
        for name in file_name:
            file_string_element_dict[name] = parser.get_file_string_element\
                    (file_path+name.split(".")[-2]+'/'+name)
                    
        request_dict['file_string_element_dict'] = file_string_element_dict
        request_dict['caller'] = caller
        return render(request, 'json_parser/json_parser.html', request_dict)
    
    def post(self, request):
        parser = JsonParser()
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        referer = request.META.get('HTTP_REFERER')
        caller = referer.split('/')[-2] # url like 127.0.0.1:8000/[caller]/
        file_path = 'upload/'+caller+'/'
        finlish = True
        if form.is_valid():
            for f in files:
                self.handle_upload_file(f, file_path)
                element_dict = parser.get_file_string_element\
                    (file_path+f.name.split(".")[-2]+'/'+f.name)
                if element_dict:
                    finlish = False
            if finlish:
                csv_file_name = []
                structure_mode = {}
                structure_dict = {}
                for f in files:
                    csv_file_name.append(f.name)
                parser.create_json_file(file_path, csv_file_name, structure_mode, structure_dict)
            return JsonResponse(finlish, safe=False)
        else:
            form = UploadFileForm()
                
    def handle_upload_file(self, f, file_path):
        fs = FileSystemStorage()
        fs.save(file_path+f.name.split(".")[-2]+'/'+f.name, f)