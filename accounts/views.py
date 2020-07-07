from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views import View
from django.conf import settings
from django.utils.translation import gettext
from accounts.forms import TwUserCreationForm
import os
import shutil

class SignUpView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            self.accounts_init(username)
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/signup.html', {'form': form})
               
    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = TwUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    def accounts_init(self, username):
        function_name = ['DPSyn', 'k_Anonymity', 'l_Diversity', 't_Closeness']
        for name in function_name:
            os.makedirs(settings.UPLOAD_ROOT+name+'/'+username+'/')
            os.makedirs(settings.OUTPUT_ROOT+name+'/'+username+'/')
        os.makedirs(settings.DPSYN_TEMP_ROOT+username+'/')
        
class LogInView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        username = request.POST.get('username', None)
        raw_password = request.POST.get('password1', None)
        referer = request.META.get('HTTP_REFERER')
        
        user = auth.authenticate(username=username, password=raw_password)
        if user is None:
            return render(request, 'registration/login.html',\
                {'form': form, 'error_message': gettext('帳密錯誤')})
        if not user.is_active:
            return render(request, 'registration/login.html',\
                {'form': form, 'error_message': gettext('帳戶已被凍結')})
        auth.login(request, user)
        
        next_page = 'home'
        if referer.find('next') != -1:
            next_page = referer.split('next=')[-1]
        return redirect(next_page)
        
    def get(self, request, *arg, **kwargs):
        next_page = request.GET.get('next', 'home')
        if request.user.is_authenticated:
            return redirect(next_page)
        form = TwUserCreationForm()
        return render(request, 'registration/login.html', {'form': form})
    
class LogOutView(View):
    def get(self, request, *arg, **kwargs):
        auth.logout(request)
        return redirect('login')
        
class DeleteAccountView(View):
    def get(self, request, *arg, **kwargs):
        user = request.user
        password = request.GET.get('password', None)
        username = user.get_username()
        check = auth.authenticate(username=username, password=password)
        if check is None:
            return JsonResponse({'message':gettext('密碼錯誤，刪除動作已取消')}, status=401)
            
        function_name = ['DPSyn', 'k_Anonymity', 'l_Diversity', 't_Closeness']
        for name in function_name:
            shutil.rmtree(settings.UPLOAD_ROOT+name+'/'+username+'/')
            shutil.rmtree(settings.OUTPUT_ROOT+name+'/'+username+'/')
        shutil.rmtree(settings.DPSYN_TEMP_ROOT+username+'/')
        user.delete()
        return HttpResponse(status=204)