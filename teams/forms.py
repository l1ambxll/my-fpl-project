from django import forms
from .models import UserTeam
from players.models import Player


class PlayerSelectionForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = team

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data.get('player')

        if not player or not self.team:
            return cleaned_data

        # Check if player already in team
        if self.team.players.filter(pk=player.pk).exists():
            raise forms.ValidationError("Player already in this team.")

        # Check maximum 3 players from same club
        if player.team:
            club_count = self.team.players.filter(team=player.team).count()
            if club_count >= 3:
                raise forms.ValidationError(
                    f"Maximum 3 players from {player.team.name} already in team."
                )

        return cleaned_data


class AddPlayerForm(forms.Form):
    """Form to search and add players to team"""
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Player',
        help_text='Choose a player to add to your team'
    )

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = team

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data.get('player')

        if not player or not self.team:
            return cleaned_data

        # Check if player already in team
        if self.team.players.filter(pk=player.pk).exists():
            raise forms.ValidationError("Player already in this team.")

        # Check maximum 3 players from same club
        if player.team:
            club_count = self.team.players.filter(team=player.team).count()
            if club_count >= 3:
                raise forms.ValidationError(
                    f"Maximum 3 players from {player.team.name} already in team."
                )

        return cleaned_data


