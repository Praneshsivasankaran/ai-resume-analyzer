from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from analysis_service import analyze_resume

app = FastAPI()

# ---- Allowed File Types and Size Limit ----
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


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

        # ---- Validate File Extension ----
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {"error": "Only PDF and DOCX files are allowed"}

        # ---- Read File ----
        contents = await file.read()

        # ---- Validate File Size ----
        if len(contents) > MAX_FILE_SIZE:
            return {"error": "File size exceeds 2MB limit"}

        temp_path = f"temp_{file.filename}"

        # ---- Save File ----
        with open(temp_path, "wb") as buffer:
            buffer.write(contents)

        # ---- Run Analysis ----
        result = analyze_resume(temp_path, jd_text)

        # ---- Remove Temp File ----
        os.remove(temp_path)

        return result

    except Exception as e:
        return {"error": str(e)}