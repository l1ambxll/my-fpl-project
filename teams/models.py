from django.db import models
from django.conf import settings


class Club(models.Model):
	fpl_team_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=150)
	short_name = models.CharField(max_length=50, blank=True)
	code = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.name


class UserTeam(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teams')
	name = models.CharField(max_length=150)
	players = models.ManyToManyField('players.Player', blank=True)
	league = models.ForeignKey('leagues.League', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_teams')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} ({self.owner.username})"

