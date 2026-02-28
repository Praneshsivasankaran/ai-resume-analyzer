import React, { useState } from "react";
import UploadForm from "../components/UploadForm";
import ScoreDashboard from "../components/ScoreDashboard";

function Home() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: "60px 20px" }}>
      
      {/* HERO SECTION */}
      <div style={{ textAlign: "center", marginBottom: "40px" }}>
        <h1
          style={{
            fontSize: "42px",
            fontWeight: "700",
            color: "white",
            marginBottom: "10px"
          }}
        >
          AI Resume Analyzer
        </h1>
        <p style={{ color: "#E0E7FF", fontSize: "18px" }}>
          Intelligent ATS Scoring & Resume Optimization
        </p>
      </div>

      {/* MAIN CARD */}
      <div
        style={{
          maxWidth: "1100px",
          margin: "auto",
          background: "white",
          padding: "40px",
          borderRadius: "20px",
          boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
          transition: "all 0.3s ease"
        }}
      >
        <UploadForm setResult={setResult} />
        {result && <ScoreDashboard result={result} />}
      </div>
    </div>
  );
}

export default Home;