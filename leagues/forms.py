from django import forms
from .models import LEAGUE_TYPES, YEAR_GROUPS


class LeagueCreateForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label='League Name',
        help_text='e.g., "Year 9 Fantasy Football" or "School-wide Competition"'
    )
    league_type = forms.ChoiceField(
        choices=LEAGUE_TYPES,
        label='League Type',
        help_text='Select the type of league'
    )
    year_group = forms.ChoiceField(
        choices=[('', '--- Select Year Group ---')] + list(YEAR_GROUPS),
        label='Year Group (for year group leagues)',
        required=False,
        help_text='Only select if creating a year group league'
    )
    about = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='About (optional)',
        help_text='Add description or rules for the league'
    )

    def clean(self):
        cleaned_data = super().clean()
        league_type = cleaned_data.get('league_type')
        year_group = cleaned_data.get('year_group')

        # If year group league, year group must be selected
        if league_type == 'year_group' and not year_group:
            self.add_error('year_group', 'Please select a year group for this league type.')

        return cleaned_data
