# CodeLens AI

### Check Live Project
[Click Here](https://repoinsight-ai-frontend.onrender.com/)

> AI-Powered GitLab Repository Analysis & Documentation Generator

[![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/docs)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)


---

## Problem Statement

Developers spend countless hours:
- Writing and maintaining documentation
- Analyzing code quality and structure
- Identifying areas for improvement
- Understanding project architecture

**RepoInsight AI** solves this by providing instant, AI-powered analysis of any GitLab repository.

---

## Features

### **AI-Powered Analysis**
- Deep code structure analysis using Gemini AI
- Technology stack identification
- Code quality assessment
- Complexity scoring

### **Auto Documentation**
- Comprehensive README generation
- API documentation
- Architecture overview
- Installation & usage guides

### **Smart Suggestions**
- Actionable improvement recommendations
- Security & testing suggestions
- CI/CD optimization tips
- Best practices implementation

### **Lightning Fast**
- Results in 15-30 seconds
- Real-time processing
- Beautiful, intuitive UI

---

## Architecture

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
     └──────────────────► Gemini AI (Google)
```

---

## Technology Stack

### Frontend
- **React 18** - UI Framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **Python 3.11** - Runtime
- **Flask** - Web framework
- **Gemini** - AI Integration 
- **Requests** - HTTP client

### DevOps
- **GitLab CI/CD** - Automated pipelines
- **Docker** - Containerization
- **Nginx** - Frontend server
- **Gunicorn** - Python WSGI server

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)
- Gemini API Key ([Get one here](https://aistudio.google.com/app/api-keys))

### 1.Clone Repository
```bash
git clone https://gitlab.com/your-username/repoinsight-ai.git
cd repoinsight-ai
```

### 2️.Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3️.Run with Docker Compose (Easiest)
```bash
docker-compose up --build
```

Visit:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

### 4️.Manual Setup

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

## Development Approach

**"Build → Deploy → Enhance"**

This reflects real-world development:
1. **Build** locally with fast iteration
2. **Deploy** when MVP is solid
3. **Enhance** with CI/CD and security

This approach let us:
- ✅ Focus on product-market fit first
- ✅ Avoid premature optimization
- ✅ Add DevOps when architecture is stable
- ✅ Demonstrate both product AND platform skills

---

## GitLab Features Utilized

### DevSecOps Platform
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

## Usage

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

## Project Structure

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

## Deployment

### GitLab + Render (Free)
1. Push code to GitLab
2. Connect to Render.com
3. Deploy backend & frontend separately
4. Set environment variables

---

## License
feel free to use this project!

---

## Acknowledgments

- **GitLab** - For the amazing DevSecOps platform
- **Google AI Studio** - For providing free GEMINI_API_KEY 
---
