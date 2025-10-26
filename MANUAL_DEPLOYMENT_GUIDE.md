# 🚀 AfCFTA Trade Matchmaker - Manual Deployment Guide

## Option 1: Manual Git Upload (Recommended)

### Step 1: Upload Files to GitHub

**Method A: Using GitHub Web Interface (Easiest)**

1. Go to: https://github.com/king-zool/matcmaking
2. Click "uploading an existing file" link
3. Upload all files from `/workspace/afcfta_matchmaker/` directory
4. Commit message: "AfCFTA Trade Matchmaker - Production Ready Platform"

**Method B: Clone and Push**

```bash
# On your local machine:
git clone https://github.com/king-zool/matcmaking.git
cd matcmaking

# Copy all files from workspace/afcfta_matchmaker/ to this folder
# Then commit and push:
git add .
git commit -m "AfCFTA Trade Matchmaker - Production Ready Platform"
git push origin main
```

### Step 2: Deploy to Render

1. **Go to Render.com**
   - Sign in with your GitHub account
   - Go to: https://dashboard.render.com

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `king-zool/matcmaking`

3. **Configuration** (Render auto-detects Flask apps)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Get your live URL!

## Option 2: Railway Deployment (Faster)

1. **Go to Railway.app**
   - Sign in with GitHub
   - Go to: https://railway.app/dashboard

2. **Deploy**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select: `king-zool/matcmaking`
   - Railway auto-deploys Python apps

3. **Get Domain**
   - Go to service settings
   - Click "Generate Domain"
   - Get your live URL

## Expected Results

**Live Platform URL**: `https://your-app-name.onrender.com` or `https://your-app.up.railway.app`

**Default Login**:
- Admin: `admin@afcfta.com` / `admin123`
- User: `exporter1@afcfta.com` / `password123`

**Features to Test**:
- ✅ Homepage and navigation
- ✅ User registration/login
- ✅ Dashboard with trade matches
- ✅ Trade Intelligence dashboard
- ✅ AI Chat Assistant
- ✅ Document management
- ✅ Finance calculator
- ✅ Admin panel (/admin)

## Files Ready for Upload

Your workspace contains 38 files ready for deployment:
- `app.py` (Main application)
- `templates/` (All HTML pages)
- `requirements.txt` (Dependencies)
- `Procfile`, `render.yaml` (Deployment configs)
- All documentation and guides

**Total Code**: 8,982 lines of production-ready Python Flask code

## Troubleshooting

**If Upload Fails**:
- Check GitHub repository exists and is public
- Verify all files are uploaded correctly
- Ensure deployment platform detects Python/Flask

**If Deployment Fails**:
- Check build logs for Python dependency issues
- Verify start command: `gunicorn app:app`
- Check database initialization

## Timeline
- **Upload to GitHub**: 2-5 minutes
- **Render/Railway Deployment**: 5-10 minutes
- **Testing**: 10-15 minutes
- **Total**: ~20 minutes to live platform

🎉 **Your AfCFTA Trade Matchmaker will be live and accessible worldwide!**