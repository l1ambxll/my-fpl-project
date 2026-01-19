# Django Installation & Project Setup - Complete ✅

## What Was Installed & Setup

### ✅ Django & Dependencies Installed
- **Django 6.0.1** - Web framework
- **Django REST Framework** - REST API support
- **Requests** - For Premier League API integration
- **python-decouple** - Environment management
- **SQLite Database** - Ready to use

### ✅ Project Structure Created
```
my-fpl-project/
├── fpl_project/          # Main project
├── players/              # App for player management
├── leagues/              # App for league management
├── teams/                # App for team management
├── templates/            # HTML templates
├── static/css/           # Bicolor UI stylesheet
├── venv/                 # Virtual environment
└── manage.py             # Django CLI
```

### ✅ Bicolor UI Theme Setup
- **Primary Color**: Dark Blue (#1a2332)
- **Secondary Color**: Gold (#f39c12)
- **Responsive Design**: Mobile-friendly
- **Professional Styling**: Cards, buttons, grid layout

### ✅ Server Status
- Django development server is running
- Visit: **http://localhost:8000/**
- Admin panel: **http://localhost:8000/admin/**

---

## Quick Start Commands

### 1. Access the Virtual Environment
```bash
cd /workspaces/my-fpl-project
source venv/bin/activate
```

### 2. Create Admin User
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### 3. Run the Server
```bash
python manage.py runserver
```

### 4. Access the Application
- **Frontend**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

---

## Next: Build Your Fantasy Football Features

### Step 1: Define Player Model
Edit `players/models.py`:
```python
from django.db import models

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]
    
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.team})"
```

### Step 2: Create Migrations
```bash
python manage.py makemigrations players
python manage.py migrate players
```

### Step 3: Register in Admin
Edit `players/admin.py`:
```python
from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'position', 'price', 'points')
    list_filter = ('position', 'team')
    search_fields = ('name',)
```

### Step 4: Create Views
Edit `players/views.py`:
```python
from django.shortcuts import render
from .models import Player

def player_list(request):
    players = Player.objects.all()
    return render(request, 'players/player_list.html', {'players': players})
```

### Step 5: Setup URLs
Create `players/urls.py` and configure routes.

---

## API Integration Example

Use the Requests library to fetch Premier League data:

```python
import requests
from .models import Player

def sync_players_from_api():
    """Fetch players from Premier League API"""
    response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    data = response.json()
    
    for player_data in data['elements']:
        Player.objects.update_or_create(
            id=player_data['id'],
            defaults={
                'name': player_data['first_name'] + ' ' + player_data['second_name'],
                'team': player_data['team'],
                'position': player_data['element_type'],
                'price': player_data['now_cost'] / 10,
                'points': player_data['total_points'],
            }
        )
```

---

## Django Commands You'll Use

```bash
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django interactive shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files (production)
python manage.py collectstatic
```

---

## File Locations

| File | Purpose |
|------|---------|
| `fpl_project/settings.py` | Django configuration |
| `fpl_project/urls.py` | URL routing |
| `players/models.py` | Database models |
| `players/views.py` | View logic |
| `templates/base.html` | Base template |
| `static/css/style.css` | Bicolor UI styling |

---

## Customizing the Bicolor Theme

Edit `static/css/style.css` to change colors:

```css
:root {
    --primary-color: #1a2332;      /* Dark Blue */
    --secondary-color: #f39c12;    /* Gold */
    --text-light: #ffffff;
    --text-dark: #1a2332;
}
```

---

## Troubleshooting

**Port already in use?**
```bash
python manage.py runserver 8080
```

**Database errors?**
```bash
python manage.py migrate --run-syncdb
```

**Static files not loading?**
```bash
python manage.py collectstatic --noinput
```

---

**You're all set!** Start building your Fantasy Football League 🚀
