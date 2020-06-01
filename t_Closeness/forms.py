from django import forms
from general.forms import AbstractForm

class ParameterForm(AbstractForm):
    k = forms.IntegerField(label='K', initial=2)
    t = forms.FloatField(label='T', initial=0.01)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        k = self.fields['k']
        t = self.fields['t']
        
        self._set_help_text(k, t)
        
    def _set_help_text(self, k, t):
        k.help_text = '去識別化後，在任意查詢條件下，至少會同時查到K筆資料'
        t.help_text = ''