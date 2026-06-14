# HOW TO FIX THE 403 ERROR

## Step 1: Create a GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "SkillForge"
4. Select scope: **"public_repo"** (read-only access)
5. Click "Generate token"
6. Copy the token (you'll only see it once!)

## Step 2: Add the token to .env
Add this line to your backend/.env file:
```
GITHUB_TOKEN=ghp_your_token_here_paste_your_token
```

## Step 3: Restart the backend
Stop the Flask server and restart it:
```bash
python app.py
```

## What this does:
- Unauthenticated: 60 requests/hour → Rate limit exceeded after ~2-3 users
- Authenticated: 5000 requests/hour → Works reliably for many users

## Why the 403 error happened:
GitHub API rate limits unauthenticated requests to 60/hour. When multiple people use your app, you hit this limit quickly. Adding a token increases it to 5000/hour.

## Testing:
Once you add the token and restart:
1. Go to http://localhost:3000/
2. Switch to GitHub Profile tab
3. Enter a valid GitHub username like "torvalds" or "gvanrossum"
4. Enter a job description
5. Click "Analyze My Skills"
6. Should work without 403 error!
