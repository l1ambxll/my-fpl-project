from django.db import models
from django.conf import settings
from django.utils import timezone


class Club(models.Model):
	"""
	Represents a Premier League club.
	Used for grouping players and showing team statistics for student analysis.
	"""
	fpl_team_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=150)
	short_name = models.CharField(max_length=50, blank=True)
	code = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.name


class UserTeam(models.Model):
	"""
	Represents a student's fantasy football team.
	Tracks the players they selected and league participation.
	Students earn points based on their selected players' real Premier League performance.
	"""
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teams')
	name = models.CharField(max_length=150)
	players = models.ManyToManyField('players.Player', blank=True)
	league = models.ForeignKey('leagues.League', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_teams')
	created_at = models.DateTimeField(auto_now_add=True)
	current_gameweek = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.name} ({self.owner.username})"
	
	def get_total_points(self):
		"""Calculate total points from all selected players"""
		return sum(player.total_points or 0 for player in self.players.all())
	
	def get_gameweek_points(self, gameweek=None):
		"""Calculate points for a specific gameweek"""
		if gameweek is None:
			gameweek = self.current_gameweek
		return sum(player.get_gameweek_score(gameweek) for player in self.players.all())
	
	def get_gameweek_transfers(self, gameweek=None):
		"""Get number of transfers used in current or specified gameweek"""
		if gameweek is None:
			gameweek = self.current_gameweek
		return self.transfers.filter(gameweek=gameweek).count()
	
	def can_make_transfer(self, gameweek=None):
		"""Check if team can make another transfer this gameweek (max 2)"""
		if gameweek is None:
			gameweek = self.current_gameweek
		return self.get_gameweek_transfers(gameweek) < 2


class Transfer(models.Model):
	"""
	Tracks player transfers (swaps) in teams.
	Limited to 2 transfers per gameweek per team.
	"""
	team = models.ForeignKey(UserTeam, on_delete=models.CASCADE, related_name='transfers')
	player_out = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='transfers_out')
	player_in = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='transfers_in')
	gameweek = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-gameweek', '-created_at']

	def __str__(self):
		return f"{self.team.name}: {self.player_out.web_name} → {self.player_in.web_name} (GW{self.gameweek})"


