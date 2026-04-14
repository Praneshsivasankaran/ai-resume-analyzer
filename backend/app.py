import os
import logging
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analysis_service import analyze_resume

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Analyzer API")

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# CORS — explicit origins
ALLOWED_ORIGINS = [
    "https://resumeanalyzer.org",
    "https://www.resumeanalyzer.org",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "AI Resume Analyzer API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), jd_text: str = Form(...)):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

    # Validate JD
    if not jd_text or len(jd_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short (min 50 chars)")

    # Read and validate size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 2MB limit")

    # Write to a secure temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    temp_path = temp_file.name
    try:
        temp_file.write(contents)
        temp_file.close()

        logger.info(f"Analyzing resume: {file.filename} ({len(contents)} bytes)")
        result = analyze_resume(temp_path, jd_text)
        logger.info(f"Analysis complete — score: {result.get('total_score')}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Analysis failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Always clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Could not remove temp file {temp_path}: {e}")