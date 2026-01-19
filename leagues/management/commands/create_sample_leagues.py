from django.core.management.base import BaseCommand
from django.utils.text import slugify

from django.contrib.auth import get_user_model
from leagues.models import League


class Command(BaseCommand):
    help = 'Create sample leagues for testing (uses first user as owner)'

    def handle(self, *args, **options):
        User = get_user_model()
        owner = User.objects.first()
        if not owner:
            self.stdout.write(self.style.ERROR('No users found. Create a user or superuser first.'))
            return

        samples = [
            {'name': 'Friends League'},
            {'name': 'Office League'},
            {'name': 'Champions League'},
        ]

        created = 0
        for s in samples:
            slug = slugify(s['name'])
            league, created_flag = League.objects.get_or_create(
                slug=slug,
                defaults={'name': s['name'], 'owner': owner, 'about': 'Sample league created by management command.'}
            )
            if created_flag:
                league.members.add(owner)
                created += 1

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created {created} sample leagues.'))
        else:
            self.stdout.write('Sample leagues already exist.')
