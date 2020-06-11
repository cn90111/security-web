from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from t_Closeness import t_closeness
from t_Closeness.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView
from general.views import AbstractBreakProgramView

@login_required
def index(request):
    return render(request, 't_Closeness/t_Closeness_home.html')

class TClosenessView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        t_closeness.run(request)
        
    def get_method_template(self):
        return 't_Closeness/t_Closeness.html'
    
class BreakProgramView(AbstractBreakProgramView):
    def break_program(self):
        t_closeness.break_program()
    
class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()