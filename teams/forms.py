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

        # Check team capacity by position
        current_players = self.team.players.all()
        position_counts = {
            1: current_players.filter(position=1).count(),  # GK
            2: current_players.filter(position=2).count(),  # DEF
            3: current_players.filter(position=3).count(),  # MID
            4: current_players.filter(position=4).count(),  # FWD
        }

        position_limits = {1: 1, 2: 4, 3: 3, 4: 3}  # GK, DEF, MID, FWD limits

        if position_counts[player.position] >= position_limits[player.position]:
            pos_name = dict(player.POSITION_CHOICES).get(player.position, 'Unknown')
            raise forms.ValidationError(
                f"Team limit for {pos_name} ({position_limits[player.position]}) reached."
            )

        return cleaned_data
