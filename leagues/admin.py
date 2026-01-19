from django.contrib import admin
from .models import League


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'created_at')
	prepopulated_fields = {'slug': ('name',)}
	search_fields = ('name', 'owner__username')
	filter_horizontal = ('members',)

