from django.core.management.base import BaseCommand
import requests
from players.models import Player
from teams.models import Club


FPL_BOOTSTRAP = 'https://fantasy.premierleague.com/api/bootstrap-static/'


def _map_position(element_type):
    # FPL element_type: 1=GK,2=DEF,3=MID,4=FWD
    return int(element_type)


class Command(BaseCommand):
    help = 'Sync players and teams from the Premier League API (bootstrap-static)'

    def handle(self, *args, **options):
        self.stdout.write('Fetching FPL bootstrap data...')
        resp = requests.get(FPL_BOOTSTRAP, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        teams = data.get('teams', [])
        for t in teams:
            club, _ = Club.objects.update_or_create(
                fpl_team_id=t['id'],
                defaults={
                    'name': t.get('name') or t.get('short_name'),
                    'short_name': t.get('short_name') or '',
                    'code': t.get('code') or '',
                }
            )

        elements = data.get('elements', [])
        for p in elements:
            team_obj = None
            team_id = p.get('team')
            if team_id:
                try:
                    team_obj = Club.objects.get(fpl_team_id=team_id)
                except Club.DoesNotExist:
                    team_obj = None

            Player.objects.update_or_create(
                fpl_id=p['id'],
                defaults={
                    'first_name': p.get('first_name') or '',
                    'last_name': p.get('second_name') or '',
                    'web_name': p.get('web_name') or '',
                    'position': _map_position(p.get('element_type') or p.get('element_type')),
                    'team': team_obj,
                    'now_cost': (p.get('now_cost') or 0) / 10.0,
                    'total_points': p.get('total_points') or 0,
                    'minutes': p.get('minutes') or 0,
                }
            )

        self.stdout.write(self.style.SUCCESS('FPL sync complete.'))
