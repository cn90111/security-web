from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from l_Diversity import l_diversity
from l_Diversity.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView
from general.views import AbstractBreakProgramView

@login_required
def index(request):
	return render(request, 'l_Diversity/l_Diversity_home.html')
    
class LDiversityView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        l_diversity.run(request)
        
    def get_method_template(self):
        return 'l_Diversity/l_Diversity.html'

class BreakProgramView(AbstractBreakProgramView):
    def break_program(self):
        l_diversity.break_program()

class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()