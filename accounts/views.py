from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views import View

from accounts.forms import TwUserCreationForm

class SignUpView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
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
    
    

class LogInView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        username = request.POST.get('username', None)
        raw_password = request.POST.get('password1', None)
        user = auth.authenticate(username=username, password=raw_password)
        if user is None:
            return render(request, 'registration/login.html',\
                            {'form': form, 'error_message': '帳密錯誤'})
        if not user.is_active:
            return render(request, 'registration/login.html',\
                            {'form': form, 'error_message': '帳戶已被凍結'})
        auth.login(request, user)
        return redirect('home')
        
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