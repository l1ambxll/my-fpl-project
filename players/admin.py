from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ('web_name', 'fpl_id', 'team', 'position', 'total_points')
	list_filter = ('position', 'team')
	search_fields = ('web_name', 'first_name', 'last_name')

