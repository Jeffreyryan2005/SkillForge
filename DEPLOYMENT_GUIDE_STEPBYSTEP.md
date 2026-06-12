# 🚀 SkillForge Deployment Guide - Step by Step

**Goal**: Deploy backend to Render + frontend to Vercel  
**Time**: ~20 minutes  
**Difficulty**: Easy ⭐

---

## ✅ PRE-DEPLOYMENT CHECKLIST

- [x] GitHub repository is public
- [x] Code committed to main branch
- [x] Both backend and frontend working locally
- [x] All tests passing

---

## 📋 PART 1: Deploy Backend to Render (10 minutes)

### Step 1: Create Render Account
1. Go to **https://render.com**
2. Click **"Sign Up"** (top right)
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub account
5. Click **"Skip for now"** on welcome screens

### Step 2: Create New Web Service
1. Click **"New +"** button (top navigation)
2. Select **"Web Service"**
3. In the dialog, find your **"SkillForge"** repo (or type to search)
4. Click **"Connect"**

### Step 3: Configure Deployment Settings

**Basic Settings:**
- **Name**: `skillforge-backend`
- **Environment**: Select **"Python 3"**
- **Region**: Select closest to you (e.g., `us-east-1`)
- **Branch**: `main` ✓

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
gunicorn app:app --chdir backend --bind 0.0.0.0:$PORT --workers 2
```

**Root Directory:** (Leave blank - it will auto-detect)

### Step 4: Add Environment Variables

Click **"Add Environment Variable"**:

**Variable 1:**
- Key: `GROQ_API_KEY`
- Value: (Get from next step)

**Variable 2:**
- Key: `FLASK_ENV`
- Value: `production`

### Step 5: Get Groq API Key (2 minutes)

1. Go to **https://console.groq.com**
2. Sign up or log in with Google/GitHub
3. Go to **"API Keys"** menu (left sidebar)
4. Click **"Create API Key"**
5. Copy the key
6. Paste it in Render as `GROQ_API_KEY`

### Step 6: Deploy Backend

1. Scroll down on Render page
2. Click **"Create Web Service"** (purple button)
3. **Wait 3-5 minutes** for deployment to complete
4. Look for ✅ **"Live"** status and a green checkmark

### Step 7: Copy Backend URL

1. When deployment is done, you'll see a URL like:
   ```
   https://skillforge-backend.onrender.com
   ```
2. **Copy this URL** - you'll need it for frontend

### Step 8: Test Backend (verify it works)

Open this URL in browser:
```
https://skillforge-backend.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile"
}
```

✅ If you see this, backend is deployed successfully!

---

## 📋 PART 2: Deploy Frontend to Vercel (10 minutes)

### Step 1: Create Vercel Account
1. Go to **https://vercel.com**
2. Click **"Sign Up"** (top right)
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account
5. Click through welcome screens

### Step 2: Import Project

1. Click **"Import Project"** or **"New Project"**
2. Under "Import Git Repository", paste:
   ```
   https://github.com/Jeffreyryan2005/SkillForge
   ```
3. Click **"Continue"**

### Step 3: Configure Project

**Project Name**: `skillforge-frontend` (auto-filled)

**Framework Preset**: Select **"Next.js"** explicitly (even if it's auto-detected).

**Root Directory**: Click to change, select **`frontend/`** folder.

### Step 4: Add Environment Variables

Click **"Environment Variables"** section:

**Add Variable:**
- Key: `NEXT_PUBLIC_API_URL`
- Value: (Paste the Render backend URL from Part 1, Step 7)
  ```
  https://skillforge-backend.onrender.com
  ```
- Click **"Add"**

### Step 5: Deploy Frontend

1. Scroll down
2. Click **"Deploy"** (blue button)
3. **Wait 2-3 minutes** for build and deployment

### Step 6: Verify Deployment Success

When complete, you'll see a screen with:
- ✅ **"Deployment Successful"** message
- A URL like: `https://skillforge-frontend.vercel.app`
- **Copy this URL** - this is your live app!

### Step 7: Test Live Application

1. Open the Vercel URL in browser:
   ```
   https://skillforge-frontend.vercel.app
   ```

2. Try the features:
   - Click **"✨ Try Sample"** - should populate form
   - Click **"🚀 Analyze My Skills"** - should call backend
   - Wait 5-10 seconds for analysis
   - ✅ Should see match score and learning plan

---

## 🎯 FINAL VERIFICATION

### Backend Checklist ✅
- [x] Deploy to Render succeeded
- [x] Health endpoint returns 200 OK
- [x] API key configured
- [x] Backend URL noted

### Frontend Checklist ✅
- [x] Deploy to Vercel succeeded
- [x] Environment variable set correctly
- [x] Can load home page without errors
- [x] Can click buttons and see responses
- [x] Learning plan displays correctly

### End-to-End Test ✅
1. Open live frontend URL
2. Click "Try Sample"
3. Click "Analyze My Skills"
4. ✅ Should show 60% match score
5. ✅ Should show learning plan with 4 weeks

---

## 🆘 TROUBLESHOOTING

### Issue: "Failed to connect to backend"
**Solution:**
1. Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
2. Verify backend is "Live" on Render
3. Test `/api/health` endpoint directly
4. Redeploy frontend (click "Redeploy" in Vercel)

### Issue: "API key error"
**Solution:**
1. Verify `GROQ_API_KEY` is set on Render
2. Get new key from https://console.groq.com
3. Update in Render environment variables
4. Redeploy backend (Render auto-deploys on env var change)

### Issue: "Frontend not building"
**Solution:**
1. Check `frontend/` is set as root directory
2. Verify no TypeScript errors locally: `npm run build` in frontend
3. Check `.env.local` is NOT committed to git
4. Redeploy in Vercel dashboard

### Issue: "Timeout connecting to Groq"
**Solution:**
1. This is normal - backend has fallback mock data
2. It will still show analysis results
3. Try again in a few minutes
4. Or skip Groq and use mock data for testing

---

## 📊 DEPLOYMENT LINKS

After successful deployment, you'll have:

**Frontend (User-facing):**
- https://skillforge-frontend.vercel.app

**Backend (API):**
- https://skillforge-backend.onrender.com

**GitHub Repository:**
- https://github.com/Jeffreyryan2005/SkillForge

---

## 🔗 MONITORING & MANAGEMENT

### Monitor Backend (Render)
1. Go to https://render.com
2. Click on "skillforge-backend" service
3. View logs, redeploy, or update settings

### Monitor Frontend (Vercel)
1. Go to https://vercel.com
2. Click on "skillforge-frontend" project
3. View deployments, analytics, or environment variables

---

## 🎉 YOU'RE DONE!

Your SkillForge application is now **live on the internet**! 🚀

### Share with others:
```
Try my AI skill analyzer: https://skillforge-frontend.vercel.app
```

### Next Steps (Optional):
- [ ] Add custom domain (Vercel/Render support this)
- [ ] Set up monitoring/alerts
- [ ] Configure auto-deploys on git push
- [ ] Add analytics tracking
- [ ] Submit to hackathon

---

## ⚡ QUICK REFERENCE

| Component | Deployed On | URL | Status |
|-----------|------------|-----|--------|
| Backend API | Render | https://skillforge-backend.onrender.com | ✅ |
| Frontend UI | Vercel | https://skillforge-frontend.vercel.app | ✅ |
| Code | GitHub | https://github.com/Jeffreyryan2005/SkillForge | ✅ |

---

**Questions?** Check troubleshooting section or revisit any step above. Good luck! 🎯
