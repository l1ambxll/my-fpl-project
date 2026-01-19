from django.db import models
from django.conf import settings


class League(models.Model):
	name = models.CharField(max_length=150)
	slug = models.SlugField(max_length=160, unique=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_leagues')
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='leagues', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	about = models.TextField(blank=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.name}"

