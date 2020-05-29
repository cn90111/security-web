from django import forms

class ParameterForm(forms.Form):
	k = forms.IntegerField(label='K', initial=2)
	t = forms.FloatField(label='T', initial=0.01)