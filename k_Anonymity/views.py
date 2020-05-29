from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from k_Anonymity import k_anonymity
from k_Anonymity.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView

@login_required
def index(request):
	return render(request, 'k_Anonymity/k_Anonymity_home.html')
    
class KAnonymityView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        k_anonymity.run(request)
        
    def get_method_template(self):
        return 'k_Anonymity/k_Anonymity.html'
        
class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()