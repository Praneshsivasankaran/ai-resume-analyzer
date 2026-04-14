import React, { useState } from "react";
import { analyzeResume } from "../services/api";
import UploadZone from "./UploadZone";
import "./UploadForm.css";

function UploadForm({ setResult }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jobDescription) return;

    setLoading(true);

    try {
      const data = await analyzeResume(file, jobDescription);
      setResult(data);
    } catch (error) {
      console.error("Error analyzing resume:", error);
      alert("Error analyzing resume");
    }

    setLoading(false);
  };

  const charCount = jobDescription.length;
  const minChars = 200;
  const charCountValid = charCount >= minChars;

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <div className="form-field">
        <label className="form-label">
          <span className="form-label-mono">01</span>
          Upload resume
        </label>
        <UploadZone file={file} onFileSelect={setFile} />
      </div>

      <div className="form-field">
        <label className="form-label">
          <span className="form-label-mono">02</span>
          Paste job description
        </label>
        <div className="textarea-wrapper">
          <textarea
            className="jd-textarea"
            placeholder="Paste the full job description here. Include responsibilities, required skills, and qualifications for the best analysis..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows="7"
          />
          <div className={`char-counter ${charCountValid ? "char-counter--valid" : ""}`}>
            {charCount < minChars ? (
              <>
                <span className="char-counter-num">{charCount}</span>
                <span className="char-counter-hint">/ {minChars} min for best results</span>
              </>
            ) : (
              <>
                <span className="char-counter-check">✓</span>
                <span>{charCount} characters</span>
              </>
            )}
          </div>
        </div>
      </div>

      <button type="submit" className="analyze-btn" disabled={loading || !file || !jobDescription}>
        {loading ? (
          <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
            <span className="spinner"></span>
            Analyzing...
          </span>
        ) : (
          <>Analyze resume →</>
        )}
      </button>
    </form>
  );
}

export default UploadForm;