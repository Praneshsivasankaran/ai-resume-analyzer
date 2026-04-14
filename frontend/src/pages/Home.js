import React, { useState } from "react";
import UploadForm from "../components/UploadForm";
import ScoreDashboard from "../components/ScoreDashboard";
import "./Home.css";

function Home() {
  const [result, setResult] = useState(null);

  const handleReset = () => {
    setResult(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="home">
      {/* HERO */}
      <section className="hero">
        <h1 className="hero-title">
          <span className="hero-title-gradient">resume analyzer.</span>
        </h1>

        <p className="hero-subtitle">
           Upload your resume, paste your job description, and get an instant
           breakdown of how an ATS would score you.
        </p>
      </section>

      {/* CARD */}
      <section className="main-card-wrapper">
        <div className="main-card">
          <div className="main-card-label">
            <span className="main-card-label-dot" />
            resume.analyzer
          </div>

          {!result && <UploadForm setResult={setResult} />}
          {result && <ScoreDashboard result={result} onReset={handleReset} />}
        </div>
      </section>

      {/* HOW IT WORKS */}
      {!result && (
        <section className="how-it-works-section">
          <div className="how-heading">
            <span className="how-heading-mono">how it works</span>
            <h2 className="how-heading-title">From upload to insight in seconds.</h2>
          </div>

          <div className="how-it-works">
            <div className="how-step">
              <div className="how-step-num">01</div>
              <div className="how-step-title">Upload</div>
              <div className="how-step-desc">
                Drop your resume in PDF or DOCX. Never stored on our servers.
              </div>
            </div>

            <div className="how-step">
              <div className="how-step-num">02</div>
              <div className="how-step-title">Paste JD</div>
              <div className="how-step-desc">
                Add any job description to compare your resume against.
              </div>
            </div>

            <div className="how-step">
              <div className="how-step-num">03</div>
              <div className="how-step-title">Parse</div>
              <div className="how-step-desc">
                We extract every skill, section, and metric from your resume.
              </div>
            </div>

            <div className="how-step">
              <div className="how-step-num">04</div>
              <div className="how-step-title">Match</div>
              <div className="how-step-desc">
                Semantic similarity matches your resume to the role using NLP embeddings.
              </div>
            </div>

            <div className="how-step">
              <div className="how-step-num">05</div>
              <div className="how-step-title">Score</div>
              <div className="how-step-desc">
                Get a detailed breakdown with actionable fixes to boost your ATS score.
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default Home;