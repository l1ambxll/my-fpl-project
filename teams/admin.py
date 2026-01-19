from django.contrib import admin
from .models import Club, UserTeam


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
	list_display = ('name', 'fpl_team_id', 'short_name')
	search_fields = ('name', 'short_name')


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'league', 'created_at')
	search_fields = ('name', 'owner__username')
	filter_horizontal = ('players',)

