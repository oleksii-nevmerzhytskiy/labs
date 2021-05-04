from django import forms

class NameForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    date = forms.DateTimeField()
    telephone = forms.CharField(max_length=30)