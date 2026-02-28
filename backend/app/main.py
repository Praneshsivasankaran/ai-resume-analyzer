from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from app.analysis_service import analyze_resume

app = FastAPI()

# 🔥 CORS (Important for Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "AI Resume Analyzer API Running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), jd_text: str = Form(...)):
    try:
        temp_path = f"temp_{file.filename}"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = analyze_resume(temp_path, jd_text)

        os.remove(temp_path)

        return result

    except Exception as e:
        return {"error": str(e)}