from django import forms

class ParameterForm(forms.Form):
	k = forms.IntegerField(label='K', initial=2)