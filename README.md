🚀 AI Resume Analyzer

An AI-powered ATS Resume Screening System that analyzes resumes against job descriptions and generates a score out of 100 with actionable improvement suggestions.
Built using FastAPI + React + NLP + ML, deployed on Netlify & Render.


🏗️ Architecture
User → Frontend (React)
       ↓
Backend (FastAPI)
       ↓
Resume Parser + NLP Engine
       ↓
Scoring Engine
       ↓
Score + Suggestions Dashboard


⚙️ Tech Stack
Frontend: React / Next.js
Backend: FastAPI
NLP: spaCy, TF-IDF, Sentence Transformers
Parsing: pdfplumber, python-docx
Deployment: Netlify + Render

📊 Scoring Model (100 Points)
Keyword Match – 35
ATS Compliance – 20
Impact Score – 15
Skills – 10
Structure – 10
Grammar – 10

🎯 Key Features
Resume & JD matching
Missing keyword detection
ATS formatting checks
Semantic similarity scoring
Actionable improvement suggestions

👨‍💻 Author
Pranesh
