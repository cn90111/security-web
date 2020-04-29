from django.shortcuts import render

def index(request):
	return render(request, 'k_Anonymity/k_Anonymity_home.html')