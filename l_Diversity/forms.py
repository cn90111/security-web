from django import forms
from general.forms import AbstractForm

class ParameterForm(AbstractForm):
    k = forms.IntegerField(label='K', initial=2)
    l = forms.IntegerField(label='L', initial=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        k = self.fields['k']
        l = self.fields['l']
        
        self._set_help_text(k, l)
        
    def _set_help_text(self, k, l):
        k.help_text = '去識別化後，在任意查詢條件下，至少會同時查到K筆資料'
        l.help_text = '去識別化後，K筆資料中，將至少有L筆資料將完全相同(包含沒去識別化的最後一欄)'