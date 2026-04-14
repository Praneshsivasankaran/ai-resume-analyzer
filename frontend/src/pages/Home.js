import React, { useState } from "react";
import UploadForm from "../components/UploadForm";
import ScoreDashboard from "../components/ScoreDashboard";
import "./Home.css";

function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="home">
      {/* HERO */}
      <section className="hero">
        <div className="hero-badge">
          <span className="hero-badge-dot" />
          ATS-OPTIMIZED · FREE · PRIVATE
        </div>

        <h1 className="hero-title">
          beat the bots.
          <br />
          <span className="hero-title-gradient">land the interview.</span>
        </h1>

        <p className="hero-mono">
          <span className="hero-mono-prefix">~/analyze</span>
          <span className="hero-mono-arrow">→</span>
          <span>see how recruiters' ATS ranks your resume</span>
        </p>

        <p className="hero-subtitle">
          Upload your resume, paste any job description, and get an instant
          breakdown of how an Applicant Tracking System would score you.
        </p>
      </section>

      {/* CARD */}
      <section className="main-card-wrapper">
        <div className="main-card">
          <div className="main-card-label">
            <span className="main-card-label-dot" />
            resume.analyzer
          </div>

          <UploadForm setResult={setResult} />
          {result && <ScoreDashboard result={result} />}
        </div>
      </section>

      {/* HOW IT WORKS */}
      {!result && (
        <section className="how-it-works">
          <div className="how-step">
            <div className="how-step-num">01</div>
            <div className="how-step-title">Upload</div>
            <div className="how-step-desc">
              Drop your resume in PDF or DOCX. It never leaves your session.
            </div>
          </div>
          <div className="how-connector" />
          <div className="how-step">
            <div className="how-step-num">02</div>
            <div className="how-step-title">Analyze</div>
            <div className="how-step-desc">
              Our NLP engine matches your resume against the job description
              using semantic similarity.
            </div>
          </div>
          <div className="how-connector" />
          <div className="how-step">
            <div className="how-step-num">03</div>
            <div className="how-step-title">Score</div>
            <div className="how-step-desc">
              Get a detailed ATS score plus actionable feedback on what to fix.
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default Home;