from django.shortcuts import render
from json_parser import JsonParser

# Create your views here.

class ParserView():
    def File_Upload(request):
        parser = JsonParser()
        saved = False
        column_element_list = []
        referer = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            files = request.FILES.getlist('file')
            if form.is_valid():
                for f in files:
                    handle_upload_file(f)
                    column_element_list.append(parser.get_column_element(f))
                saved = True
                return render(request, 'json_parser/json_parser.html', locals())
            else:
                form = UploadFileForm()
                
    def handle_upload_file(f):
        if(f.name.split(".")[1] == 'json'):
            fs = FileSystemStorage()
            fs.save('upload/json_parser/'+f.name.replace("_dict",'').split(".")[-2]+'/'+f.name, f)
        else:
            fs = FileSystemStorage()
            fs.save('upload/json_parser/'+f.name.split(".")[-2]+'/'+f.name, f)