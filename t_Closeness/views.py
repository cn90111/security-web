from django.shortcuts import render

def index(request):
    return render(request, 't_Closeness/t_Closeness_home.html')
