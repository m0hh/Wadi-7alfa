from django import forms

class ClientForm(forms.Form):
    your_name = forms.CharField(max_length=200)
    api_pk = forms.CharField(max_length=200)
    team_id = forms.IntegerField()