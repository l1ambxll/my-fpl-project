# School Fantasy Football League - Setup Guide

## Project Overview

This is an educational Fantasy Football League web application designed specifically for schools and children. It's built with Django and integrates with the Premier League API to provide:

- **Simple, intuitive interface** for students
- **Authentic fantasy football mechanics** with real player data
- **Data analysis tools** to help students learn analytical skills
- **Classroom engagement** through friendly competition
- **Points tracking system** to understand real fantasy football scoring

**Purpose:** Help increase student engagement through fantasy football gameplay while developing their analytical thinking skills.

## Project Structure
```
my-fpl-project/
├── fpl_project/              # Main project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── views.py             # Project-level views
├── players/                  # PL player management app
├── leagues/                  # School/class league management
├── teams/                    # Student team management
├── accounts/                 # Student authentication & profiles
├── templates/               # Student-friendly HTML templates
│   ├── base.html           # Base template with school-appropriate theme
│   └── home.html           # Home page
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css       # Bicolor UI stylesheet (school-ready)
│   └── js/
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── venv/                   # Virtual environment
```

## Installation & Setup

### 1. Activate Virtual Environment
```bash
cd /workspaces/my-fpl-project
source venv/bin/activate
```

### 2. Verify Django Installation
```bash
python -m django --version
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Then visit: `http://localhost:8000/`

## Installed Packages
- **Django 6.0.1** - Web framework
- **djangorestframework** - REST API support
- **requests** - HTTP library for Premier League API
- **python-decouple** - Environment variable management

## Next Steps

### 1. Customize Models
Edit the models in `players/models.py`, `leagues/models.py`, and `teams/models.py` to define your data structure.

Example (in `players/models.py`):
```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20)
    team = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    
    def __str__(self):
        return self.name
```

### 2. Create Model Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Register Models in Admin
Edit `players/admin.py`:
```python
from django.contrib import admin
from .models import Player

admin.site.register(Player)
```

### 4. Create API Views (Optional)
Use Django REST Framework to create APIs for your frontend.

### 5. API Integration
Use the `requests` library to fetch data from the Premier League API and populate your database.

## Bicolor UI Theme
The website uses a professional bicolor theme:
- **Primary Color**: Dark Blue (#1a2332)
- **Secondary Color**: Gold (#f39c12)

Customize in `static/css/style.css` by modifying the CSS variables:
```css
:root {
    --primary-color: #1a2332;
    --secondary-color: #f39c12;
}
```

## Available Commands
```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files (production)
python manage.py collectstatic

# Django shell (interactive Python with Django context)
python manage.py shell
```

## Environment Variables (Optional)
Create a `.env` file for sensitive data:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FPL_API_KEY=your_premier_league_api_key
```

Then load with python-decouple:
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

## Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Requests Library](https://requests.readthedocs.io/)

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate
```

### Issue: Port 8000 already in use
**Solution**: Run server on different port
```bash
python manage.py runserver 8080
```

### Issue: Static files not loading
**Solution**: Run collectstatic
```bash
python manage.py collectstatic --noinput
```

---

Happy coding! 🚀
