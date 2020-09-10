from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from general.models import ExecuteModel

import os

import shutil

@login_required
def index(request):
    return render(request, 'home.html')
    
class MaintainView(View):
    def get(self, request, *arg, **kwargs):
        for objects in ExecuteModel.objects.all():
            objects.delete()
        return render(request, 'maintain/maintain_page.html')

class InitializeView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        username = request.user.get_username()
        finish = False
        for path in ['upload', 'output']:
            for method in ['DPView', 'k_Anonymity', 'l_Diversity', 't_Closeness']:
                temp_path = path+'/'+method+'/'+username+'/'
                for directory_path in os.listdir(temp_path):
                    shutil.rmtree(temp_path+directory_path)
        path = settings.DPVIEW_TEMP_ROOT+username+'/'
        for directory_path in os.listdir(path):
            shutil.rmtree(path+directory_path)
        finish = True
        return JsonResponse(finish, safe=False)