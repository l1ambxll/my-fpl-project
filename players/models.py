from django.db import models


POSITION_CHOICES = [
	(1, 'GK'),
	(2, 'DEF'),
	(3, 'MID'),
	(4, 'FWD'),
]


class Player(models.Model):
	fpl_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	web_name = models.CharField(max_length=100)
	position = models.IntegerField(choices=POSITION_CHOICES)
	team = models.ForeignKey('teams.Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
	now_cost = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
	total_points = models.IntegerField(default=0)
	minutes = models.IntegerField(default=0)

	class Meta:
		ordering = ['-total_points']

	def __str__(self):
		return f"{self.web_name} ({self.fpl_id})"

