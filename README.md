# 🚀 RepoInsight AI

> AI-Powered GitLab Repository Analysis & Documentation Generator

[![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/docs)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)

Built for **GitLab Hackathon Challenge 2025** | i-Hack, E-Summit IIT Bombay | By [Ayush Hardeniya](https://linkedin.com/in/ayushHardeniya)

---

## 📋 Problem Statement

Developers spend countless hours:
- 📝 Writing and maintaining documentation
- 🔍 Analyzing code quality and structure
- 💡 Identifying areas for improvement
- 🏗️ Understanding project architecture

**RepoInsight AI** solves this by providing instant, AI-powered analysis of any GitLab repository.

---

## ✨ Features

### 🤖 **AI-Powered Analysis**
- Deep code structure analysis using Claude AI
- Technology stack identification
- Code quality assessment
- Complexity scoring

### 📚 **Auto Documentation**
- Comprehensive README generation
- API documentation
- Architecture overview
- Installation & usage guides

### 💡 **Smart Suggestions**
- Actionable improvement recommendations
- Security & testing suggestions
- CI/CD optimization tips
- Best practices implementation

### ⚡ **Lightning Fast**
- Results in 15-30 seconds
- Real-time processing
- Beautiful, intuitive UI

---

## 🏗️ Architecture

```
┌─────────────────┐
│   React + Vite  │  Frontend (Tailwind CSS)
│   Frontend      │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼────────┐
│  Flask Backend  │  Python API
│                 │
└────┬───────┬────┘
     │       │
     │       └──────────► GitLab API
     │
     └──────────────────► Claude AI (Anthropic)
```

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI Framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **Python 3.11** - Runtime
- **Flask** - Web framework
- **Anthropic SDK** - Claude AI integration
- **Requests** - HTTP client

### DevOps
- **GitLab CI/CD** - Automated pipelines
- **Docker** - Containerization
- **Nginx** - Frontend server
- **Gunicorn** - Python WSGI server

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

### 1️⃣ Clone Repository
```bash
git clone https://gitlab.com/your-username/repoinsight-ai.git
cd repoinsight-ai
```

### 2️⃣ Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3️⃣ Run with Docker Compose (Easiest)
```bash
docker-compose up --build
```

Visit:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

### 4️⃣ Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 GitLab Features Utilized

### ✅ DevSecOps Platform
1. **GitLab CI/CD**
   - Automated testing
   - Docker image building
   - Multi-stage deployment pipeline

2. **Container Registry**
   - Docker image storage
   - Version management

3. **GitLab API Integration**
   - Repository data fetching
   - File structure analysis
   - Commit history retrieval

4. **Security Features**
   - Secret management
   - Environment variables
   - Secure token handling

---

## 🎯 Usage

1. **Enter Repository URL**
   - Paste any public GitLab repository URL
   - Example: `https://gitlab.com/gitlab-org/gitlab`

2. **Click Analyze**
   - AI analyzes code structure
   - Generates comprehensive insights
   - Creates documentation

3. **Explore Results**
   - **Overview**: Project summary and metrics
   - **Analysis**: Code quality assessment
   - **Documentation**: Auto-generated docs
   - **Suggestions**: Improvement recommendations

---

## 🎬 Demo Video

[Link to demo video - Max 2.5 minutes]

### Video Highlights:
- Problem statement (0:00-0:30)
- Solution demo (0:30-1:40)
- GitLab integration (1:40-2:10)
- Impact & conclusion (2:10-2:30)

---

## 📁 Project Structure

```
repoinsight-ai/
├── .gitlab-ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Local development
├── README.md
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── services/
│       ├── gitlab_service.py
│       └── ai_service.py
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── components/
    ├── package.json
    ├── Dockerfile
    └── nginx.conf
```

---

## 🌐 Deployment

### Option 1: GitLab + Render (Free)
1. Push code to GitLab
2. Connect to Render.com
3. Deploy backend & frontend separately
4. Set environment variables

### Option 2: GitLab + AWS (Using Hackathon Credits)
1. Configure AWS credentials in GitLab CI/CD
2. Push to `main` branch
3. Pipeline auto-deploys to:
   - Backend → EC2/ECS
   - Frontend → S3 + CloudFront

---

## 🏆 Hackathon Submission

### ✅ Submission Checklist
- [x] Public GitLab repository
- [x] Complete source code
- [x] Working demo (deployed)
- [x] Demo video (< 2.5 mins)
- [x] Documentation
- [x] GitLab CI/CD configured

### 📄 Key Documents
- **README.md** - This file
- **PROJECT_EXPLANATION.md** - Detailed submission document
- **Demo Video** - Linked above

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open merge request

---

## 📝 License

MIT License - feel free to use this project!

---

## 👥 Team

Built for GitLab Hackathon Challenge 2025

- **Event**: i-Hack 2025, E-Summit
- **Organizer**: E-Cell, IIT Bombay
- **Track**: GitLab CodeForge

---

## 🙏 Acknowledgments

- **GitLab** - For the amazing DevSecOps platform
- **Google AI Studio** - For providing free GEMINI_API_KEY 
- 

---

## 📞 Support

For issues or questions:
- Create an issue in GitLab
- Email: [work@ayushhardeniya.site]

---

<div align="center">

**Built with ❤️ using GitLab, Gemini AI, React, and Python by [Ayush Hardeniya](https://github.com/ayushHardeniya)**

[Live Demo](#) | [Documentation](#) | [Video Demo](#)

</div>