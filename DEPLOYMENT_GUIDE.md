# AfCFTA Trade Matchmaker - Complete Deployment Guide

## Overview
This guide provides step-by-step instructions to deploy the AfCFTA Trade Matchmaker Flask application to various hosting platforms.

## Application Features
- User Management (Importers/Exporters/Admins)
- AI-Powered Trade Matching Algorithm
- Trade Intelligence Dashboard
- AI Trade Assistant Chat
- Finance Calculator
- Document Management System
- Comprehensive Admin Panel

## Prerequisites
- Git installed on your computer
- GitHub account (or GitLab/Bitbucket)
- Account on chosen hosting platform

---

## Option 1: Render (Recommended - Free Tier Available)

### Step 1: Prepare Repository
1. Create a new GitHub repository
2. Upload all files from `/workspace/afcfta_matchmaker/` to the repository

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: afcfta-matchmaker
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variables:
   - `SECRET_KEY`: (generate a random string)
   - `FLASK_ENV`: production
6. Click "Create Web Service"

### Step 3: Database Initialization
- The SQLite database will be created automatically on first run
- Note: Free tier uses ephemeral storage (data resets on redeploy)
- For persistent data, upgrade to paid plan

**Deployment Time**: 5-10 minutes
**URL Format**: `https://afcfta-matchmaker.onrender.com`

---

## Option 2: Railway (Easy Deployment)

### Step 1: Prepare Repository
1. Create a GitHub repository with all application files

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Click on your service → Settings → Generate Domain

**Deployment Time**: 3-5 minutes
**URL Format**: `https://afcfta-matchmaker.up.railway.app`

---

## Option 3: PythonAnywhere (Stable for Flask Apps)

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free Beginner account

### Step 2: Upload Application
1. Open a Bash console
2. Clone or upload your repository:
   ```bash
   git clone https://github.com/yourusername/afcfta-matchmaker.git
   cd afcfta-matchmaker
   ```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 afcfta-env
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to Web tab → Add a new web app
2. Choose "Manual configuration" → Python 3.10
3. Set Source code: `/home/yourusername/afcfta-matchmaker`
4. Set Working directory: `/home/yourusername/afcfta-matchmaker`
5. Edit WSGI file:
```python
import sys
path = '/home/yourusername/afcfta-matchmaker'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
6. Set Virtualenv: `/home/yourusername/.virtualenvs/afcfta-env`
7. Click Reload

**URL Format**: `https://yourusername.pythonanywhere.com`

---

## Option 4: Heroku (Classic Platform)

### Step 1: Install Heroku CLI
Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Deploy
```bash
cd afcfta_matchmaker
heroku login
heroku create afcfta-matchmaker
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Step 3: Initialize Database
```bash
heroku run python
>>> from app import db
>>> db.create_all()
>>> exit()
```

**URL Format**: `https://afcfta-matchmaker.herokuapp.com`

---

## Option 5: Google Cloud Run (Scalable)

### Step 1: Create Dockerfile
Create `Dockerfile` in project root:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT app:app
```

### Step 2: Deploy
```bash
gcloud init
gcloud run deploy afcfta-matchmaker --source .
```

---

## Post-Deployment Setup

### 1. Access Admin Panel
- URL: `https://your-app-url.com/admin/login`
- Default credentials:
  - Email: `admin@afcfta.com`
  - Password: `admin123`

### 2. Change Admin Password
1. Login to admin panel
2. Go to Settings
3. Update admin credentials

### 3. Create Test Accounts
The system includes sample data with demo accounts:
- Exporter: `exporter1@afcfta.com` / `password123`
- Importer: `importer1@afcfta.com` / `password123`

### 4. Verify Features
Test all features:
- [ ] User registration and login
- [ ] Dashboard and trade matching
- [ ] AI Trade Assistant
- [ ] Trade Intelligence Dashboard
- [ ] Finance Calculator
- [ ] Document Management
- [ ] Admin panel functionality

---

## Database Considerations

### SQLite (Current)
- **Pros**: Simple, no configuration
- **Cons**: Not suitable for high traffic, ephemeral on some platforms
- **Best for**: Testing, small deployments

### PostgreSQL (Production Recommended)
For production use, migrate to PostgreSQL:

1. **Update requirements.txt**:
```
psycopg2-binary==2.9.9
```

2. **Update app.py**:
```python
import os
database_url = os.environ.get('DATABASE_URL', 'sqlite:///afcfta_trades.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```

3. **Add PostgreSQL database** on your hosting platform

---

## Security Recommendations

### 1. Environment Variables
Move sensitive data to environment variables:
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
```

### 2. HTTPS
Ensure hosting platform uses HTTPS (most do by default)

### 3. Change Default Passwords
Immediately change all default passwords after deployment

### 4. Database Backups
Set up regular backups if using persistent database

---

## Troubleshooting

### Application Won't Start
1. Check logs on hosting platform
2. Verify all dependencies in requirements.txt
3. Ensure Python version matches runtime.txt

### Database Errors
1. Check if database file has write permissions
2. Verify database migrations ran successfully
3. Consider switching to PostgreSQL

### Static Files Not Loading
1. Check Flask static folder configuration
2. Verify file paths in templates
3. Ensure hosting platform serves static files

---

## Monitoring & Maintenance

### Log Monitoring
- Check application logs regularly
- Monitor error rates and response times
- Track user activity through admin panel

### Performance Optimization
- Enable caching for trade matches
- Optimize database queries
- Consider CDN for static assets

### Regular Updates
- Update dependencies regularly
- Apply security patches
- Backup database before updates

---

## Cost Estimates

| Platform | Free Tier | Paid Plans Start At |
|----------|-----------|---------------------|
| Render | Yes (750 hrs/month) | $7/month |
| Railway | $5 credit/month | $5/month |
| PythonAnywhere | Yes (limited) | $5/month |
| Heroku | No (eco dynos $5/month) | $5/month |
| Google Cloud Run | Yes (2M requests/month) | Pay per use |

---

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Test locally first: `python app.py`
4. Verify all environment variables are set

---

## Quick Start Commands

### Test Locally
```bash
cd afcfta_matchmaker
pip install -r requirements.txt
python app.py
# Access at http://localhost:5000
```

### Create Database
```bash
python create_sample_data.py
```

### Production Server
```bash
gunicorn app:app
```

---

## Architecture Summary

```
afcfta_matchmaker/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Procfile                 # Process configuration
├── runtime.txt              # Python version
├── render.yaml              # Render configuration
├── railway.json             # Railway configuration
├── instance/
│   └── afcfta_trades.db     # SQLite database
├── templates/               # HTML templates
│   ├── admin/              # Admin panel templates
│   └── *.html              # User-facing templates
└── static/                 # CSS, JS, images (if any)
```

---

## Next Steps

1. Choose a hosting platform based on your needs
2. Follow the deployment steps for that platform
3. Access the deployed application
4. Change default admin password
5. Test all features
6. Share the URL with users

**Estimated Total Deployment Time**: 10-30 minutes (depending on platform)

---

*This application is ready for production deployment. All features have been implemented and tested locally.*
