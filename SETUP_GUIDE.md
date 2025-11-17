# 🚀 Complete Setup Guide - RepoInsight AI

**For Non-Coders**: This guide will help you deploy the project WITHOUT coding knowledge!

---

## 📋 Prerequisites Checklist

Before starting, you need:

### Required Accounts (All FREE)
- [ ] GitLab account - [Sign up](https://gitlab.com)
- [ ] Anthropic Claude API key - [Get here](https://console.anthropic.com/)
- [ ] Render.com account - [Sign up](https://render.com) (for hosting)

### Optional
- [ ] Git installed on your computer (or use GitLab web interface)
- [ ] Text editor (VS Code, Notepad++, or even Notepad)

---

## 🎯 Step 1: Get Your API Key

### Anthropic Claude API ($5 free credit)

1. Go to https://console.anthropic.com/
2. Sign up with email
3. Verify your email
4. Go to "API Keys" section
5. Click "Create Key"
6. **Copy the key** - it looks like: `sk-ant-api03-xxxxx...`
7. **Save it somewhere safe** - you'll need it later!

---

## 📁 Step 2: Create Project Structure on Your Computer

### Windows Users:
1. Create a folder on Desktop called `repoinsight-ai`
2. Inside it, create these folders:
   - `backend`
   - `backend/services`
   - `frontend`
   - `frontend/src`
   - `frontend/src/components`

### Mac/Linux Users:
```bash
mkdir -p repoinsight-ai/{backend/services,frontend/src/components}
cd repoinsight-ai
```

---

## 📝 Step 3: Copy All Files

Now, copy each file I provided above into the correct location:

### Root Directory Files (`repoinsight-ai/`)
- `.gitlab-ci.yml`
- `docker-compose.yml`
- `.env.example`
- `README.md`
- `PROJECT_EXPLANATION.md`
- `SETUP_GUIDE.md` (this file)

### Backend Files (`repoinsight-ai/backend/`)
- `app.py`
- `requirements.txt`
- `Dockerfile`

### Backend Services (`repoinsight-ai/backend/services/`)
- `gitlab_service.py`
- `ai_service.py`

### Frontend Root (`repoinsight-ai/frontend/`)
- `package.json`
- `vite.config.js`
- `tailwind.config.js`
- `postcss.config.js`
- `index.html`
- `Dockerfile`
- `nginx.conf`

### Frontend Src (`repoinsight-ai/frontend/src/`)
- `App.jsx`
- `main.jsx`
- `index.css`

### Frontend Components (`repoinsight-ai/frontend/src/components/`)
- `Hero.jsx`
- `AnalysisForm.jsx`
- `LoadingSpinner.jsx`
- `ResultsDisplay.jsx`

---

## 🔑 Step 4: Configure Environment Variables

1. In the root folder, rename `.env.example` to `.env`
2. Open `.env` with a text editor
3. Paste your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
   ```
4. Save the file

---

## 🦊 Step 5: Upload to GitLab

### Option A: Using GitLab Web Interface (Easiest)

1. Go to https://gitlab.com
2. Click "New Project" → "Create blank project"
3. Name it: `repoinsight-ai`
4. Make it **Public**
5. Click "Create project"
6. Click "Upload File" button
7. Upload ALL your files (you can drag & drop folders!)
8. **Important**: Delete the `.env` file after upload (don't share API keys!)
9. Instead, we'll add the API key in GitLab settings

### Option B: Using Git Command Line

```bash
cd repoinsight-ai
git init
git add .
git commit -m "Initial commit"
git remote add origin https://gitlab.com/YOUR-USERNAME/repoinsight-ai.git
git push -u origin main
```

---

## 🔐 Step 6: Add Secret Variables in GitLab

**IMPORTANT**: Never commit API keys to the repository!

1. In your GitLab project, go to **Settings → CI/CD**
2. Expand **Variables** section
3. Click **Add Variable**
4. Add these variables:

   | Key | Value | Protect | Mask |
   |-----|-------|---------|------|
   | `ANTHROPIC_API_KEY` | Your API key | ✅ Yes | ✅ Yes |
   | `GITLAB_TOKEN` | (leave empty) | ✅ Yes | ✅ Yes |

5. Click **Add variable** for each

---

## 🚀 Step 7: Deploy on Render.com (FREE)

### Deploy Backend

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitLab account
4. Select `repoinsight-ai` repository
5. Configure:
   - **Name**: `repoinsight-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Plan**: `Free`
6. Add Environment Variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your API key
7. Click **Create Web Service**
8. Wait 5-10 minutes for deployment
9. **Copy the URL** (looks like: `https://repoinsight-backend-xxxx.onrender.com`)

### Deploy Frontend

1. Click "New +" → "Static Site"
2. Select `repoinsight-ai` repository
3. Configure:
   - **Name**: `repoinsight-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: Your backend URL (from step above)
5. Click **Create Static Site**
6. Wait 5-10 minutes
7. **Your app is live!** 🎉

---

## ✅ Step 8: Test Your Deployment

1. Open your frontend URL (from Render dashboard)
2. Paste a GitLab repository URL, for example:
   ```
   https://gitlab.com/gitlab-org/gitlab
   ```
3. Click "Analyze Repository"
4. Wait 15-30 seconds
5. You should see analysis results!

### Troubleshooting

**If analysis fails:**
1. Check Render backend logs for errors
2. Verify your API key is correct
3. Make sure the GitLab repository is public
4. Check that VITE_API_URL is correctly set

---

## 🎬 Step 9: Create Demo Video

### Tools You Can Use (All FREE)
- **Windows**: Xbox Game Bar (built-in - press Win+G)
- **Mac**: QuickTime Player (built-in)
- **Any OS**: OBS Studio (download free)

### Video Structure (2.5 minutes max)

**[0:00-0:30] Introduction**
```
"Hi! I'm [Your Name], and this is RepoInsight AI. 
Developers waste hours writing documentation. 
RepoInsight solves this with AI-powered analysis."
```

**[0:30-1:40] Demo**
1. Show the homepage
2. Paste a GitLab repository URL
3. Show the analysis process
4. Highlight key features:
   - Overview tab
   - Analysis results
   - Auto-generated documentation
   - Improvement suggestions

**[1:40-2:10] Technical Highlights**
```
"Built using GitLab's DevSecOps platform:
- GitLab API for repository data
- GitLab CI/CD for automated deployment
- Claude AI for intelligent analysis
- Deployed on AWS/Render"
```

**[2:10-2:30] Impact**
```
"RepoInsight saves 5-10 hours per project,
helps teams maintain better documentation,
and is open source for the community.
Thank you!"
```

### Recording Tips:
- Use a good microphone
- Record in a quiet space
- Show enthusiasm!
- Keep it under 2.5 minutes
- Upload to YouTube (unlisted is fine)

---

## 📤 Step 10: Submit to Hackathon

### What You Need:

1. **GitLab Repository URL**
   - Example: `https://gitlab.com/your-username/repoinsight-ai`
   - Make sure it's PUBLIC

2. **Demo Video** (under 2.5 minutes)
   - Upload to YouTube
   - Get the link
   - Example: `https://youtu.be/xxxxx`

3. **Submission Document**
   - Use the `PROJECT_EXPLANATION.md` file
   - Convert to PDF if needed

### Submission Checklist:
- [ ] Public GitLab repository with all code
- [ ] README.md is complete
- [ ] Demo video uploaded and linked
- [ ] Project explanation document ready
- [ ] Application is deployed and accessible
- [ ] .gitlab-ci.yml is configured and working

---

## 🎯 Final Checklist

Before submitting, verify:

- [ ] ✅ GitLab repository is public
- [ ] ✅ All code files are uploaded
- [ ] ✅ CI/CD pipeline runs successfully
- [ ] ✅ Backend is deployed and accessible
- [ ] ✅ Frontend is deployed and accessible
- [ ] ✅ Demo video is under 2.5 minutes
- [ ] ✅ Video shows actual working demo
- [ ] ✅ README.md is comprehensive
- [ ] ✅ PROJECT_EXPLANATION.md is complete
- [ ] ✅ No API keys or secrets in public code

---

## 🆘 Getting Help

### If Something Doesn't Work:

1. **Check Logs**
   - Render: Click on your service → "Logs" tab
   - GitLab: Go to CI/CD → Pipelines

2. **Common Issues**:

   **"API Key Invalid"**
   - Check if you copied the full key
   - Make sure no extra spaces

   **"Repository Not Found"**
   - Verify the URL is correct
   - Check if repository is public

   **"Build Failed"**
   - Check GitLab CI/CD logs
   - Verify all files are uploaded

3. **Need More Help?**
   - Create an issue in your GitLab repo
   - Check Render documentation
   - Search the error message on Google

---

## 🎉 Congratulations!

You've successfully:
- ✅ Created an AI-powered application
- ✅ Used GitLab's DevSecOps platform
- ✅ Deployed to production
- ✅ Created a demo video
- ✅ Prepared hackathon submission

**You're ready to submit!** 🚀

Good luck with the hackathon! 🏆

---

## 📚 Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Render Deployment Guide](https://render.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

<div align="center">

**Need help? Create an issue on GitLab!**

*Built for GitLab Hackathon Challenge 2025*

</div>