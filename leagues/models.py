from django.db import models
from django.conf import settings


LEAGUE_TYPES = [
	('year_group', 'Year Group'),
	('whole_school', 'Whole School'),
	('class', 'Class'),
	('other', 'Other'),
]

YEAR_GROUPS = [
	('7', 'Year 7'),
	('8', 'Year 8'),
	('9', 'Year 9'),
	('10', 'Year 10'),
	('11', 'Year 11'),
	('12', 'Year 12'),
	('13', 'Year 13'),
]


class League(models.Model):
	"""
	Represents a school or class fantasy football league.
	Teachers/admins create leagues, students join to compete with classmates.
	This enables friendly competition and creates discussion points during school hours.
	Supports whole school leagues and year group specific leagues.
	"""
	name = models.CharField(max_length=150)
	slug = models.SlugField(max_length=160, unique=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_leagues')
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='leagues', blank=True)
	league_type = models.CharField(max_length=20, choices=LEAGUE_TYPES, default='class', help_text='Type of league')
	year_group = models.CharField(max_length=2, choices=YEAR_GROUPS, blank=True, null=True, help_text='For year group leagues')
	created_at = models.DateTimeField(auto_now_add=True)
	about = models.TextField(blank=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		if self.league_type == 'year_group' and self.year_group:
			return f"{self.name} (Year {self.year_group})"
		elif self.league_type == 'whole_school':
			return f"{self.name} (Whole School)"
		return f"{self.name}"
	
	def get_league_type_display_full(self):
		"""Get full display of league type with year group if applicable"""
		type_name = self.get_league_type_display()
		if self.league_type == 'year_group' and self.year_group:
			type_name += f" - Year {self.year_group}"
		return type_name

