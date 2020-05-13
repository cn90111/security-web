from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views import View

from accounts.forms import TwUserCreationForm

class SignUpView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/signup.html', {'form': form})
               
    def get(self, request, *arg, **kwargs):
        form = TwUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    

class LogInView(View):
    def post(self, request, *arg, **kwargs):
        pass
    
class LogOutView(View):
    def post(self, request, *arg, **kwargs):
        pass