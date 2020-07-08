from django import forms
from general.forms import AbstractForm

class ParameterForm(AbstractForm):
    k = forms.IntegerField(label='K', initial=2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        k = self.fields['k']
        
        self._set_help_text(k)
        
    def _set_help_text(self, k):
        k.help_text = '去識別化後，在任意查詢條件下，至少會同時查到K筆資料'