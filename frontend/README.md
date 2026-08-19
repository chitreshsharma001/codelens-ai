# CodeLens AI

### Check Live Project
[Click Here](https://codelens-ai-frontend.onrender.com/)

> AI-Powered GitLab Repository Analysis & Documentation Generator

[![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/docs)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)

A college mini-project by [Chitresh Sharma].

---

## Problem Statement

Developers spend countless hours:
- Writing and maintaining documentation
- Analyzing code quality and structure
- Identifying areas for improvement
- Understanding project architecture

**CodeLens AI** solves this by providing instant, AI-powered analysis of any GitLab repository.

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
┌─────────────────┐
│ Frontend │ React + Vite │ Frontend (Tailwind CSS)
└────────┬────────┘
│
│ HTTP/REST
│
┌────────▼────────┐
│ Flask Backend │ Python API
└────┬───────┬────┘
│ │
│ └────────────► GitLab API
│
└────────────────────► Gemini AI (Google)

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
- GitLab Personal Access Token (`read_api` scope)

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/codelens-ai.git
cd codelens-ai
```

### 2. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and GITLAB_TOKEN
```

### 3. Run with Docker Compose (Easiest)
```bash
docker compose up --build
```

Visit:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

### 4. Manual Setup

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

codelens-ai/
├── docker-compose.yml # Local development
├── README.md
├── backend/
│ ├── app.py # Flask application
│ ├── requirements.txt
│ ├── Dockerfile
│ └── services/
│ ├── gitlab_service.py
│ └── ai_service.py
└── frontend/
├── src/
│ ├── App.jsx
│ ├── main.jsx
│ └── components/
├── package.json
├── Dockerfile
└── nginx.conf

---

## SDG Alignment

This project aligns with **SDG 9: Industry, Innovation and Infrastructure**, by contributing to innovation in developer tooling and improving software development infrastructure/productivity. It also supports **SDG 4: Quality Education**, by helping developers learn and understand unfamiliar codebases through auto-generated documentation.

---

## Credits & Acknowledgments

- **GitLab** - For the DevSecOps platform
- **Google AI Studio** - For providing free Gemini API access

---

## License

MIT License - feel free to use this project!

---

<div align="center">

**Built with Gemini AI, React, and Python**

</div>