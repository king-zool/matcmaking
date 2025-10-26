# Quick Deployment - AfCFTA Trade Matchmaker

## Option 1: Deploy to Render (Easiest - 5 minutes)

### Prerequisites
- GitHub account
- Render account (free at render.com)

### Steps

1. **Create GitHub Repository**
   ```bash
   cd /workspace/afcfta_matchmaker
   git init
   git add .
   git commit -m "AfCFTA Trade Matchmaker - Production Ready"
   # Create repo on GitHub and push
   git remote add origin https://github.com/YOUR_USERNAME/afcfta-matchmaker.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com and sign in
   - Click "New +" button → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Apply" and then "Create Web Service"
   - Wait 5-10 minutes for deployment

3. **Access Your Application**
   - Render will provide a URL like: `https://afcfta-matchmaker.onrender.com`
   - Open the URL in your browser
   - Login with admin credentials: `admin@afcfta.com` / `admin123`
   - **IMPORTANT**: Change the admin password immediately

### Post-Deployment
- Test all features
- Change default passwords
- Configure environment variables if needed

---

## Option 2: Deploy to Railway (Fastest - 3 minutes)

### Steps

1. **Prepare Repository**
   - Same as Option 1 (create GitHub repository)

2. **Deploy on Railway**
   - Go to https://railway.app and sign in
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys
   - Click on your service → "Settings" → "Generate Domain"

3. **Access Your Application**
   - Railway provides URL like: `https://afcfta-matchmaker.up.railway.app`
   - Test the application
   - Change admin credentials

---

## Option 3: PythonAnywhere (Most Stable)

### Steps

1. **Sign Up**
   - Go to https://pythonanywhere.com
   - Create free Beginner account

2. **Upload Code**
   - Open Bash console
   - Clone your GitHub repository:
     ```bash
     git clone https://github.com/YOUR_USERNAME/afcfta-matchmaker.git
     cd afcfta-matchmaker
     ```

3. **Setup Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 afcfta
   pip install -r requirements.txt
   python create_sample_data.py
   ```

4. **Configure Web App**
   - Go to Web tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set Source code: `/home/USERNAME/afcfta-matchmaker`
   - Set Working directory: `/home/USERNAME/afcfta-matchmaker`
   - Edit WSGI file:
     ```python
     import sys
     path = '/home/USERNAME/afcfta-matchmaker'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```
   - Set Virtualenv: `/home/USERNAME/.virtualenvs/afcfta`
   - Click "Reload"

5. **Access Your Application**
   - URL: `https://USERNAME.pythonanywhere.com`

---

## Environment Variables (Optional)

For production security, set these on your hosting platform:

```
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
DATABASE_URL=postgresql://... (if using PostgreSQL)
```

---

## Testing Checklist

After deployment, verify:

- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard displays matches
- [ ] AI Chat Assistant responds
- [ ] Trade Intelligence dashboard shows data
- [ ] Finance Calculator computes correctly
- [ ] Document upload works
- [ ] Admin login works (`/admin/login`)
- [ ] Admin can manage users
- [ ] All pages are responsive on mobile

---

## Default Credentials

**Admin Access:**
- Email: `admin@afcfta.com`
- Password: `admin123`
- URL: `https://your-app-url.com/admin/login`

**Sample User:**
- Email: `exporter1@afcfta.com`
- Password: `password123`

**CRITICAL**: Change all default passwords immediately after deployment!

---

## Troubleshooting

### Application Won't Start
- Check logs on hosting platform dashboard
- Verify Python version is 3.9+
- Ensure all dependencies installed

### Database Errors
- SQLite database created automatically
- For persistent data, consider PostgreSQL upgrade
- Check file permissions

### 500 Internal Server Error
- Check application logs
- Verify environment variables set correctly
- Test locally first: `python app.py`

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **PythonAnywhere Help**: https://help.pythonanywhere.com

---

## Next Steps After Deployment

1. Change admin password
2. Test all features thoroughly
3. Add your company/organization details
4. Invite real users to test
5. Monitor application logs
6. Set up domain name (optional)
7. Configure email notifications (future)
8. Set up database backups

---

**Estimated Time**: 5-15 minutes depending on platform
**Cost**: Free tier available on all recommended platforms
**Result**: Fully functional web application accessible globally
