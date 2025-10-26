# AfCFTA Trade Matchmaker - Deployment Checklist

## Pre-Deployment Verification

### Files Check
- [x] app.py (main application)
- [x] create_sample_data.py (database initialization)
- [x] requirements.txt (dependencies)
- [x] Procfile (process configuration)
- [x] runtime.txt (Python version)
- [x] render.yaml (Render config)
- [x] railway.json (Railway config)
- [x] .gitignore (Git ignore rules)
- [x] .slugignore (deployment optimization)
- [x] All templates (15 HTML files)
- [x] Documentation (5 MD files)

### Application Check
- [x] Database schema defined
- [x] Sample data script ready
- [x] All routes implemented
- [x] Admin panel functional
- [x] AI features working
- [x] Environment variable support
- [x] Production configuration ready

---

## Deployment Steps (Choose One Platform)

### Option A: Render Deployment

#### Step 1: Prepare Repository
- [ ] Create GitHub account (if needed)
- [ ] Create new repository: `afcfta-matchmaker`
- [ ] Initialize Git in project folder
- [ ] Add all files to Git
- [ ] Commit with message: "Initial deployment"
- [ ] Push to GitHub

**Commands:**
```bash
cd /workspace/afcfta_matchmaker
git init
git add .
git commit -m "AfCFTA Trade Matchmaker - Initial deployment"
git remote add origin https://github.com/YOUR_USERNAME/afcfta-matchmaker.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy to Render
- [ ] Go to https://render.com
- [ ] Sign up / Login
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub account
- [ ] Select `afcfta-matchmaker` repository
- [ ] Render auto-detects configuration from `render.yaml`
- [ ] Click "Apply" then "Create Web Service"
- [ ] Wait 5-10 minutes for deployment

#### Step 3: Verify Deployment
- [ ] Open provided URL (e.g., `https://afcfta-matchmaker.onrender.com`)
- [ ] Homepage loads correctly
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard displays
- [ ] All features accessible

#### Step 4: Security Setup
- [ ] Login to admin panel: `/admin/login`
- [ ] Use credentials: `admin@afcfta.com` / `admin123`
- [ ] Navigate to Settings
- [ ] Change admin password
- [ ] Update admin email
- [ ] Save changes

---

### Option B: Railway Deployment

#### Step 1: Prepare Repository
- [ ] Same as Render Step 1 (create GitHub repository)

#### Step 2: Deploy to Railway
- [ ] Go to https://railway.app
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose `afcfta-matchmaker` repository
- [ ] Railway auto-detects and deploys
- [ ] Click on service → Settings
- [ ] Click "Generate Domain"

#### Step 3: Verify & Secure
- [ ] Open provided URL
- [ ] Test all features
- [ ] Login to admin panel
- [ ] Change default passwords

---

### Option C: PythonAnywhere Deployment

#### Step 1: Account Setup
- [ ] Go to https://pythonanywhere.com
- [ ] Create Beginner account (free)
- [ ] Verify email

#### Step 2: Upload Code
- [ ] Open Bash console on PythonAnywhere
- [ ] Clone repository or upload files
```bash
git clone https://github.com/YOUR_USERNAME/afcfta-matchmaker.git
cd afcfta-matchmaker
```

#### Step 3: Environment Setup
- [ ] Create virtual environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 afcfta
pip install -r requirements.txt
```

#### Step 4: Initialize Database
```bash
python create_sample_data.py
```

#### Step 5: Configure Web App
- [ ] Go to Web tab
- [ ] Click "Add a new web app"
- [ ] Choose "Manual configuration"
- [ ] Select Python 3.10
- [ ] Set source code path: `/home/USERNAME/afcfta-matchmaker`
- [ ] Set working directory: `/home/USERNAME/afcfta-matchmaker`
- [ ] Edit WSGI configuration file
- [ ] Set virtualenv: `/home/USERNAME/.virtualenvs/afcfta`
- [ ] Click "Reload"

#### Step 6: Verify & Secure
- [ ] Open `https://USERNAME.pythonanywhere.com`
- [ ] Test features
- [ ] Change admin password

---

## Post-Deployment Testing

### Functional Testing
- [ ] **Homepage**: Loads without errors
- [ ] **Registration**: New user can register
- [ ] **Login**: User can login successfully
- [ ] **Dashboard**: Shows trade matches
- [ ] **Profile**: Can edit and save profile
- [ ] **Trade Intelligence**: Dashboard displays analytics
- [ ] **AI Chat**: Assistant responds to queries
- [ ] **Finance Calculator**: Calculations work correctly
- [ ] **Documents**: Can upload documents
- [ ] **Logout**: User can logout successfully

### Admin Testing
- [ ] **Admin Login**: Can access `/admin/login`
- [ ] **Admin Dashboard**: Shows statistics
- [ ] **User Management**: Can view all users
- [ ] **User Verification**: Can verify users
- [ ] **User Toggle**: Can activate/deactivate users
- [ ] **Document Review**: Can see uploaded documents
- [ ] **Document Verification**: Can approve documents
- [ ] **Settings**: Can update configurations
- [ ] **Activity Logs**: Shows admin actions

### Mobile Testing
- [ ] **Responsive Design**: Works on mobile devices
- [ ] **Navigation**: Mobile menu works
- [ ] **Forms**: Can fill forms on mobile
- [ ] **Tables**: Data tables are scrollable

### Performance Testing
- [ ] **Page Load**: All pages load within 3 seconds
- [ ] **Database**: Queries execute quickly
- [ ] **Matching Algorithm**: Returns results promptly
- [ ] **No Errors**: Check browser console for errors

---

## Security Checklist

### Immediate Actions (Required)
- [ ] Change admin password
- [ ] Change admin email
- [ ] Update SECRET_KEY environment variable
- [ ] Verify HTTPS is enabled (automatic on most platforms)

### Recommended Actions
- [ ] Review all default sample accounts
- [ ] Delete or update sample user passwords
- [ ] Configure session timeout
- [ ] Set up application monitoring
- [ ] Enable error logging
- [ ] Configure database backups (if using PostgreSQL)

---

## Environment Variables Setup

### Required for Production (Set on hosting platform)

**Render:**
- Go to Dashboard → Environment
- Add variables:
  - `SECRET_KEY`: Generate random string
  - `FLASK_ENV`: `production`

**Railway:**
- Go to Variables tab
- Add same variables as Render

**PythonAnywhere:**
- Not required (uses .env file or defaults)

---

## Monitoring & Maintenance

### Daily
- [ ] Check application is running
- [ ] Review any error logs
- [ ] Monitor user registrations

### Weekly
- [ ] Review admin activity logs
- [ ] Check pending document verifications
- [ ] Analyze platform statistics

### Monthly
- [ ] Update dependencies (security patches)
- [ ] Review and optimize database
- [ ] Analyze user feedback
- [ ] Plan feature enhancements

---

## Troubleshooting Guide

### Application Won't Start
**Check:**
- [ ] Logs on hosting platform
- [ ] Python version matches runtime.txt
- [ ] All dependencies installed
- [ ] Environment variables set correctly

**Solution:**
- Review logs for specific error
- Verify requirements.txt is complete
- Test locally first: `python app.py`

### Database Errors
**Check:**
- [ ] Database file created
- [ ] Write permissions
- [ ] Sample data loaded

**Solution:**
- Run `python create_sample_data.py`
- Check file permissions
- Review database connection string

### Features Not Working
**Check:**
- [ ] JavaScript console for errors
- [ ] Network tab for failed requests
- [ ] Application logs for backend errors

**Solution:**
- Clear browser cache
- Test in incognito mode
- Check API endpoints are accessible

### Slow Performance
**Check:**
- [ ] Database query optimization
- [ ] Number of records in database
- [ ] Hosting platform resources

**Solution:**
- Add database indexes
- Upgrade hosting plan
- Implement caching

---

## Success Criteria

### Deployment Successful When:
- [x] Application accessible via public URL
- [x] All pages load without errors
- [x] Users can register and login
- [x] Trade matching algorithm works
- [x] Admin panel fully functional
- [x] All enhanced features operational
- [x] HTTPS enabled
- [x] Mobile responsive

---

## Next Steps After Deployment

### Immediate (Day 1)
1. [ ] Share deployment URL with team
2. [ ] Create initial test accounts
3. [ ] Verify all features work
4. [ ] Document any issues found

### Short-term (Week 1)
1. [ ] Invite beta users
2. [ ] Collect feedback
3. [ ] Monitor usage patterns
4. [ ] Address bugs if any

### Medium-term (Month 1)
1. [ ] Analyze user behavior
2. [ ] Optimize performance
3. [ ] Plan feature enhancements
4. [ ] Consider custom domain
5. [ ] Set up email notifications
6. [ ] Upgrade to PostgreSQL (if needed)

---

## Support Resources

### Documentation
- **README.md** - Full project documentation
- **DEPLOYMENT_GUIDE.md** - Detailed deployment instructions (353 lines)
- **QUICK_DEPLOY.md** - Quick start guide (197 lines)
- **DEPLOYMENT_PACKAGE.md** - Complete deployment package info

### Platform Help
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app  
- **PythonAnywhere**: https://help.pythonanywhere.com

### Flask Resources
- **Flask Docs**: https://flask.palletsprojects.com
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **Gunicorn**: https://docs.gunicorn.org

---

## Completion Confirmation

I confirm that:
- [ ] I have chosen a hosting platform
- [ ] Repository is created and code pushed
- [ ] Application is deployed successfully
- [ ] All features have been tested
- [ ] Default passwords have been changed
- [ ] Application is accessible via public URL
- [ ] Documentation has been reviewed
- [ ] Monitoring is in place

**Deployment URL**: _______________________________

**Admin Email**: _______________________________

**Deployment Date**: _______________________________

---

## Estimated Timeline

| Phase | Duration |
|-------|----------|
| Create GitHub Repository | 2 minutes |
| Push Code to GitHub | 1 minute |
| Setup Hosting Account | 2 minutes |
| Deploy Application | 5-10 minutes |
| Test All Features | 10 minutes |
| Change Passwords | 2 minutes |
| **TOTAL** | **20-30 minutes** |

---

**Status**: Ready for deployment
**Difficulty**: Easy (follow step-by-step guide)
**Result**: Live web application accessible globally

---

*Use this checklist to track your deployment progress. Check off items as you complete them.*
