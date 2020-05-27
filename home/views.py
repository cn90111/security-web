from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views import View
from django.http import JsonResponse

import os

import shutil

@login_required
def index(request):
	return render(request, 'home.html')
    
class InitializeView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        username = request.user.get_username()
        finish = False
        for path in ['upload', 'output']:
            for method in ['DPSyn', 'k_Anonymity', 'l_Diversity', 't_Closeness']:
                temp_path = path+'/'+method+'/'+username+'/'
                for directory_path in os.listdir(temp_path):
                    shutil.rmtree(temp_path+directory_path)
        path = settings.DPSYN_TEMP_ROOT+username
        for directory_path in os.listdir(path):
            shutil.rmtree(path+directory_path)
        finish = True
        return JsonResponse(finish, safe=False)