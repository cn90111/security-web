from django.shortcuts import render

def index(request):
	return render(request, 'l_Diversity/l_Diversity_home.html')