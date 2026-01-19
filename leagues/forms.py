from django import forms


class LeagueCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label='League name')
    about = forms.CharField(widget=forms.Textarea, required=False, label='About (optional)')
