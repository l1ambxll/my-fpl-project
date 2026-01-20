from django.db import models


# Position choices for students to understand player roles
POSITION_CHOICES = [
	(1, 'GK'),      # Goalkeeper
	(2, 'DEF'),     # Defender
	(3, 'MID'),     # Midfielder
	(4, 'FWD'),     # Forward
]


class Player(models.Model):
	"""
	Represents a Premier League player that students can select for their teams.
	Data is synced from the Premier League API for real-world accuracy.
	"""
	fpl_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	web_name = models.CharField(max_length=100)
	position = models.IntegerField(choices=POSITION_CHOICES)
	team = models.ForeignKey('teams.Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
	now_cost = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
	total_points = models.IntegerField(default=0)
	minutes = models.IntegerField(default=0)
	gameweek_scores = models.JSONField(default=dict, blank=True)

	class Meta:
		ordering = ['-total_points']

	def __str__(self):
		return f"{self.web_name} ({self.fpl_id})"
	
	def get_gameweek_score(self, gameweek):
		"""Get points for a specific gameweek"""
		return self.gameweek_scores.get(str(gameweek), 0)

