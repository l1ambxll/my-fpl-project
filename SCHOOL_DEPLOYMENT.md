# 🏫 School Deployment & Administration Guide

## Introduction

This guide is designed for teachers, IT administrators, and headteachers who want to deploy and manage the School Fantasy Football League application in their school environment.

---

## 📋 System Requirements

### Minimum Requirements
- **Operating System:** Windows, macOS, or Linux
- **Python:** 3.8 or higher
- **RAM:** 512MB (minimum), 2GB+ recommended
- **Storage:** 2GB for application and database
- **Network:** Internet connection for Premier League API sync

### Recommended Setup
- **Server:** Ubuntu 20.04 LTS or similar Linux distribution
- **Python:** 3.10 or higher
- **RAM:** 4GB+
- **Storage:** 10GB+ (allows for growth)
- **Database:** SQLite initially (easy to upgrade to PostgreSQL later)

---

## 🚀 Quick Deployment (School Computer Lab / Single Server)

### Step 1: Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### Step 2: Download & Setup Application
```bash
# Navigate to your desired location
cd /opt/school-fpl/

# Clone or extract the application
# (Assuming you have the files ready)

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
# Apply database migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 4: Run the Application
```bash
# Start development server
python manage.py runserver 0.0.0.0:8000

# The application will be available at:
# http://localhost:8000/ (from the server)
# http://<server-ip>:8000/ (from other computers on the network)
```

### Step 5: Configure Network Access
If students are accessing from other computers:
```bash
# Find your server's IP address
hostname -I

# Students can then visit: http://<your-ip>:8000/
```

---

## 👩‍💼 Teacher/Admin Setup

### Creating the Admin Account
When you first run `python manage.py createsuperuser`, you'll be prompted for:
- **Username:** Create something memorable (e.g., `admin`, `hudson`, or your name)
- **Email:** Your school email address
- **Password:** Create a strong password and save it securely

### Accessing the Admin Panel
1. Visit: `http://localhost:8000/admin/`
2. Login with your admin credentials
3. You'll see the admin dashboard where you can:
   - Create leagues
   - Manage students
   - Add Premier League players
   - Monitor activity

---

## 🎓 Creating Your First School League

### Option 1: Through Admin Panel (Easiest)
1. Login to admin panel: `http://localhost:8000/admin/`
2. Click "Leagues" in the left menu
3. Click "+ Add League"
4. Fill in:
   - **Name:** e.g., "Year 9 English Class Fantasy League"
   - **Slug:** Auto-generates (e.g., "year-9-english-class-fantasy-league")
   - **Owner:** Select your admin account
   - **Description:** Optional information about the league

5. Click "Save"
6. Add students:
   - Go back to the league
   - Scroll to "Members"
   - Click "Add another Member"
   - Select students from the list

### Option 2: Import Existing Leagues
If you have a CSV file with league data, we can create a custom script to import it.

---

## 👥 Student Enrollment Process

### Method 1: Self-Registration
Students can register themselves:
1. Visit: `http://<your-server>:8000/register/`
2. Create account with username and password
3. Login
4. Navigate to Leagues to join existing leagues

### Method 2: Batch Registration
For teacher-controlled enrollment:
1. Teacher creates accounts through admin panel
2. Provide students with login credentials
3. Students login and join assigned leagues

### Method 3: Self-Service with Codes
(Advanced) Generate league access codes for students to join automatically

---

## 🔄 Data Management

### Syncing Premier League Data

The application includes a command to sync real Premier League player data:

```bash
# Activate virtual environment first
source venv/bin/activate

# Sync Premier League data
python manage.py sync_fpl

# This fetches:
# - Player names and positions
# - Current prices
# - Teams assignments
# - Historical statistics
```

**Recommendation:** Run this sync weekly (Tuesdays recommended - after Premier League gameweek ends)

### Automating Weekly Syncs

#### Option 1: Using Cron (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add this line to run every Tuesday at 11 PM:
0 23 * * 2 cd /opt/school-fpl && source venv/bin/activate && python manage.py sync_fpl
```

#### Option 2: Using Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Name: "FPL Data Sync"
4. Trigger: Weekly on Tuesday at 11:00 PM
5. Action: Run program
   - Program: `python.exe`
   - Arguments: `manage.py sync_fpl`
   - Start in: `C:\path\to\my-fpl-project\`

### Backing Up Data

**Important:** Regularly backup your database to prevent data loss.

```bash
# Backup SQLite database
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# This creates: db.sqlite3.backup.20260120
```

**Recommendation:** Backup weekly before syncing data

---

## 🛡️ Security Best Practices

### 1. Admin Account Security
- Use a strong password (12+ characters, mixed case, numbers, special characters)
- Change password regularly
- Only share with authorized staff

### 2. Student Privacy
- Only collect necessary information
- Don't require real names if not needed
- Consider GDPR/COPPA compliance for your jurisdiction

### 3. Database Security
- Keep backups in secure location
- Consider encrypting database file
- Restrict file permissions: `chmod 600 db.sqlite3`

### 4. Network Security
- If accessible over internet, use HTTPS (requires SSL certificate)
- Use strong passwords for all accounts
- Restrict access to admin panel by IP if possible

### 5. Data Protection
```bash
# Restrict database file permissions (Linux/macOS)
chmod 600 db.sqlite3

# Restrict manage.py permissions
chmod 700 manage.py
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused" when accessing application
**Solution:**
- Check that server is running: `python manage.py runserver 0.0.0.0:8000`
- Check correct IP address: `hostname -I`
- Try: `http://localhost:8000/` from server computer

### Issue: Students can't access from other computers
**Solution:**
- Use server's IP address instead of localhost
- Check Windows Firewall is allowing Python
- Check school network allows traffic on port 8000

### Issue: "ModuleNotFoundError" when running commands
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# If still not working, reinstall requirements
pip install -r requirements.txt
```

### Issue: League not appearing after creation
**Solution:**
- Refresh the browser (Ctrl+F5 or Cmd+Shift+R)
- Clear browser cache
- Try different browser

### Issue: Students can't join league
**Solution:**
- Make sure student account is created first
- Check student hasn't already joined league
- Add member through admin panel

---

## 📈 Monitoring & Analytics

### Viewing Activity

**Through Admin Panel:**
1. Login to `http://localhost:8000/admin/`
2. Click on "Leagues" to see all leagues
3. Click on "Users" to see student accounts
4. Click on "User Teams" to see team selections

### Reports You Can Generate

1. **League Leaderboard**
   - See which students are winning
   - Identify engagement levels

2. **Player Usage**
   - See which players are selected most
   - Understand student analysis patterns

3. **Student Participation**
   - Check which students have active teams
   - Identify students who haven't joined yet

---

## 🚀 Performance Optimization

### For Large School (100+ Students)

1. **Database Optimization**
   - Create database indexes
   - Monitor database size
   - Consider SQLite to PostgreSQL migration

2. **Server Configuration**
   - Use gunicorn/uwsgi for production
   - Add caching layer (Redis)
   - Distribute load across multiple processes

3. **Scheduled Tasks**
   - Use Celery for background data syncs
   - Prevent data sync from slowing down student access

---

## 🔧 Production Deployment

For deploying to a real web server accessible beyond your school network:

### Using Gunicorn (Production Server)
```bash
# Install gunicorn
pip install gunicorn

# Run application
gunicorn fpl_project.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)
```bash
# Build Docker image
docker build -t school-fpl .

# Run container
docker run -p 8000:8000 school-fpl
```

### SSL/HTTPS (For Internet-Facing)
- Obtain SSL certificate (Let's Encrypt recommended for free)
- Configure in Django settings
- Use reverse proxy (Nginx/Apache)

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

**Daily:**
- Monitor server is running
- Check for error logs

**Weekly:**
- Sync Premier League data (Tuesdays)
- Backup database
- Check student engagement

**Monthly:**
- Review logs for errors
- Update system packages
- Check database size

### Getting Help

If you encounter issues:
1. Check [README.md](README.md) - General overview
2. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation help
3. Review Django documentation: https://docs.djangoproject.com/
4. Check Premier League API documentation

---

## 🎓 Educational Outcomes to Track

### Engagement Metrics
- Number of students who registered
- Number actively participating
- Student login frequency

### Learning Outcomes
- Quality of team selections (do they align with data?)
- Student discussions in class
- Understanding of analytical concepts

### Discussion Points
- Have students brought up fantasy football in non-classroom contexts?
- Are they using data to support arguments?
- Do they understand value propositions?

---

## 📋 Compliance Checklist

Before deploying in your school:

- [ ] GDPR/Privacy compliance reviewed
- [ ] IT department approval obtained
- [ ] Network administrator notified
- [ ] Backup procedures established
- [ ] Admin password securely stored
- [ ] Student data collection minimized
- [ ] Acceptable use policy in place
- [ ] Staff training conducted

---

## 🎯 Success Tips

1. **Start Small:** Begin with one class or year group
2. **Communicate:** Explain the benefits to students and colleagues
3. **Engage:** Participate in discussions about fantasy teams
4. **Monitor:** Track engagement and learning outcomes
5. **Iterate:** Get feedback and improve the experience
6. **Celebrate:** Recognize student achievements in the league
7. **Document:** Keep notes on what works and what doesn't

---

## 📄 Document Version

- **Created:** January 2026
- **For:** School Fantasy Football League
- **Version:** 1.0

Last updated: January 20, 2026
