import React, { useState } from "react";
import { analyzeResume } from "../services/api";

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

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "40px" }}>
      <div style={{ marginBottom: "15px" }}>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ddd",
            width: "100%"
          }}
        />
      </div>

      <textarea
        placeholder="Paste Job Description"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        rows="6"
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #ddd",
          resize: "vertical",
          marginBottom: "15px"
        }}
      />

      <button
  type="submit"
  className="analyze-btn"
  disabled={loading}
>
  {loading ? (
    <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
      <span className="spinner"></span>
      Analyzing...
    </span>
  ) : (
    "Analyze Resume"
  )}
</button>
    </form>
  );
}

export default UploadForm;