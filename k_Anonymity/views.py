from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from k_Anonymity import k_anonymity
from k_Anonymity.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView
from general.views import AbstractBreakProgramView

@login_required
def index(request):
    request_dict = {}
    file_upload_url = reverse('file_upload', args=['json'])
    custom_url = reverse('k_Anonymity:custom')
    request_dict['file_upload_url'] = file_upload_url
    request_dict['custom_url'] = custom_url
    return render(request, 'k_Anonymity/k_Anonymity_home.vue', request_dict)
    
class KAnonymityView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        k_anonymity.run(request)
        
    def get_method_template(self):
        return 'k_Anonymity/k_Anonymity.vue'
        
class BreakProgramView(AbstractBreakProgramView):
    def break_program(self, file):
        k_anonymity.break_program(file)
        
class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()