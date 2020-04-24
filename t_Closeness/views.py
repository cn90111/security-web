from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date,datetime
import os
today = date.today()
import logging
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')
from django.core.files.storage import FileSystemStorage
from .models import FileModel
from .forms import UploadFileForm
import pandas as pd

# Create your views here.
def index(request):
    return render(request, 't_Closeness/t_Closeness_home.html')

def t_Closeness(request):
    path = 'upload/t_Closeness/'
    files = os.listdir(path)
    s = []
    for filename in os.listdir(path):
        filepath = os.path.join(path,filename)
        if os.path.isdir(filepath):
            s.append(filename)
    return render(request, 't_Closeness/t_Closeness.html', locals())

def Web_View_CSV(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_form = FileModel()
            for file in request.FILES.getlist('file'):
                upload_form.file = file
                df = pd.read_csv(upload_form.file)
                if(df.shape[1] <= 4 and df.shape[0] <= 200):
                    tables = df.head(200).to_html()
                else:
                    cln = str(df.shape[1])
                    row = str(df.shape[0])
                    return JsonResponse({"status":"錯誤","message":"欄數限制最多為4, 列數限制最多為200\n文件欄數："+ cln +", 列數："+ row + ", 不符合標準"}, status=400)
        else:
            form = UploadFileForm()
    return JsonResponse(tables, safe=False)

def handle_upload_file(f):
    print(f.name.split("_")[0])
    if(f.name.split(".")[1] == 'json'):
        fs = FileSystemStorage()
        fs.save('upload/t_Closeness/'+f.name.replace("_dict",'').split(".")[-2]+'/'+f.name, f)
    else:
        fs = FileSystemStorage()
        fs.save('upload/t_Closeness/'+f.name.split(".")[-2]+'/'+f.name, f)

def File_Upload(request):
    saved = False
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        #print(str(form.is_valid()))
        #print(str(request.FILES))
        #print(str(files))
        if form.is_valid():
            for f in files:
                handle_upload_file(f)
            #myfile = form.cleaned_data['file']
            #print(str(form.cleaned_data['file']))
            #fs = FileSystemStorage()
            #fs.save('upload/t_Closeness/'+myfile.name.split(".")[-2]+'/'+myfile.name, myfile)
            saved = True
            return JsonResponse(saved, safe=False)
        else:
            form = UploadFileForm()

def File_List_Upload(request):
    path = 'upload/t_Closeness/'
    s = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in fileNames:
            file = os.path.join(dirPath, f)
            if not os.path.isdir(file):		#判斷是否是文件夾, 不是文件夾才開
                if(file.split(".")[1] == 'csv'):
                    s.append(os.path.join(dirPath, f).replace('\\','/'))
    return render(request, 't_Closeness/file_list_upload.html', locals())

def File_List_Output(request):
    path = 'output/t_Closeness/'
    s = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in fileNames:
            file = os.path.join(dirPath, f)
            if not os.path.isdir(file):		#判斷是否是文件夾, 不是文件夾才開
                if(file.split(".")[1] == 'csv'):
                    s.append(os.path.join(dirPath, f).replace('\\','/'))
    return render(request, 't_Closeness/file_list_output.html', locals())

def Download_Output(request):
    file = request.POST.get('File',None)	# 取得單選項的值
    name = request.POST.get('File',None).split("/")[-1]
    df = pd.read_csv(file)
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=%s' %name
    df.to_csv(path_or_buf=response,index=False,decimal=",")
    return response

def CSV_View_Output(request):
    path = 'output/t_Closeness/'
    s = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in fileNames:
            file = os.path.join(dirPath, f)
            if not os.path.isdir(file):		#判斷是否是文件夾, 不是文件夾才開
                if(file.split(".")[1] == 'csv'):
                    s.append(os.path.join(dirPath, f).replace('\\','/'))
    name = request.POST.get('File',None)	# 取得單選項的值
    df = pd.read_csv(name)
    tables = df.head(2000).to_html()
    #return HttpResponse(tables)
    return render(request, 't_Closeness/file_list_output.html', locals())

def CSV_View_Upload(request):
    path = 'upload/t_Closeness/'
    s = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in fileNames:
            file = os.path.join(dirPath, f)
            if not os.path.isdir(file):		#判斷是否是文件夾, 不是文件夾才開
                if(file.split(".")[1] == 'csv'):
                    s.append(os.path.join(dirPath, f).replace('\\','/'))
    name = request.POST.get('File',None)	# 取得單選項的值
    df = pd.read_csv(name)
    tables = df.head(2000).to_html()
    #return HttpResponse(tables)
    return render(request, 't_Closeness/file_list_upload.html', locals())