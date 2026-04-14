import React, { useEffect, useState } from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import "./ScoreDashboard.css";

// Tier colors
const TIER = {
  excellent: { min: 85, label: "Excellent", color: "#22c55e", glow: "rgba(34, 197, 94, 0.35)" },
  strong:    { min: 70, label: "Strong",    color: "#22d3ee", glow: "rgba(34, 211, 238, 0.35)" },
  moderate:  { min: 50, label: "Moderate",  color: "#f59e0b", glow: "rgba(245, 158, 11, 0.35)" },
  weak:      { min: 0,  label: "Needs work", color: "#ef4444", glow: "rgba(239, 68, 68, 0.35)" },
};

const getTier = (score) => {
  if (score >= 85) return TIER.excellent;
  if (score >= 70) return TIER.strong;
  if (score >= 50) return TIER.moderate;
  return TIER.weak;
};

const TIER_DESC = {
  excellent: "Excellent alignment. Minor refinements may further strengthen it.",
  strong:    "Strongly aligned with this role — a few areas could still be improved.",
  moderate:  "Moderate alignment. Address missing skills and keywords to become more competitive.",
  weak:      "Significant improvement needed to match this job description effectively.",
};

const BREAKDOWN_LABELS = {
  keyword:   "Keyword match",
  ats:       "ATS compatibility",
  impact:    "Impact & metrics",
  skills:    "Skills coverage",
  structure: "Structure",
};


// ============ Circular Score Gauge ============
function ScoreGauge({ score, color, glow }) {
  const [displayScore, setDisplayScore] = useState(0);
  const radius = 110;
  const stroke = 12;
  const circumference = 2 * Math.PI * radius;

  useEffect(() => {
    let start = 0;
    const end = Math.round(score);
    const duration = 1200;
    const stepTime = 16;
    const stepValue = end / (duration / stepTime);

    const counter = setInterval(() => {
      start += stepValue;
      if (start >= end) {
        start = end;
        clearInterval(counter);
      }
      setDisplayScore(Math.round(start));
    }, stepTime);

    return () => clearInterval(counter);
  }, [score]);

  const progress = (displayScore / 100) * circumference;

  return (
    <div className="gauge-wrapper" style={{ "--gauge-color": color, "--gauge-glow": glow }}>
      <svg width="260" height="260" viewBox="0 0 260 260" className="gauge-svg">
        <defs>
          <filter id="gauge-glow-filter" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        {/* Track */}
        <circle
          cx="130"
          cy="130"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={stroke}
        />
        {/* Progress */}
        <circle
          cx="130"
          cy="130"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          transform="rotate(-90 130 130)"
          filter="url(#gauge-glow-filter)"
          style={{ transition: "stroke-dashoffset 0.05s linear" }}
        />
      </svg>
      <div className="gauge-content">
        <div className="gauge-number">{displayScore}</div>
        <div className="gauge-outof">/ 100</div>
      </div>
    </div>
  );
}


// ============ Mini progress bar for breakdown cards ============
function MiniBar({ value, color }) {
  return (
    <div className="mini-bar-track">
      <div
        className="mini-bar-fill"
        style={{ width: `${Math.min(100, Math.max(0, value))}%`, background: color }}
      />
    </div>
  );
}


// ============ Skills summary strip ============
function SkillsSummary({ matched, total, color }) {
  if (!total) return null;
  const pct = (matched / total) * 100;
  return (
    <div className="skills-summary">
      <div className="skills-summary-text">
        <span className="skills-summary-num">{matched}</span>
        <span className="skills-summary-sep">of</span>
        <span className="skills-summary-num">{total}</span>
        <span className="skills-summary-label">skills from the job description matched</span>
      </div>
      <div className="skills-summary-bar">
        <div
          className="skills-summary-fill"
          style={{ width: `${pct}%`, background: color, boxShadow: `0 0 12px ${color}` }}
        />
      </div>
    </div>
  );
}


// ============ Main dashboard ============
function ScoreDashboard({ result, onReset }) {
  const tier = getTier(result.total_score);
  const tierKey = Object.keys(TIER).find((k) => TIER[k] === tier);
  const tierDesc = TIER_DESC[tierKey];

  const radarData = [
    { subject: "Keyword", value: result.breakdown.keyword },
    { subject: "ATS",       value: result.breakdown.ats },
    { subject: "Impact",    value: result.breakdown.impact },
    { subject: "Skills",    value: result.breakdown.skills },
    { subject: "Structure", value: result.breakdown.structure },
  ];

  // Strengths
  const strengths = [];
  if (result.breakdown.ats >= 90) strengths.push("Excellent ATS formatting — all required sections present.");
  if (result.breakdown.impact >= 80) strengths.push("Strong quantified achievements with metrics and action verbs.");
  if (result.breakdown.structure >= 90) strengths.push("Clean, well-organized resume structure.");
  if (result.breakdown.keyword >= 80) strengths.push("High semantic alignment with the job description.");
  if (result.breakdown.skills >= 80) strengths.push("Broad skills coverage matching the role's requirements.");

  // Suggestions — split visible / collapsed
  const suggestions = result.suggestions || [];
  const [showAllSuggestions, setShowAllSuggestions] = useState(false);
  const VISIBLE_SUGGESTIONS = 3;
  const visible = showAllSuggestions ? suggestions : suggestions.slice(0, VISIBLE_SUGGESTIONS);
  const hidden = suggestions.length - VISIBLE_SUGGESTIONS;

  const matched = result.matched_skills || [];
  const missing = result.missing_skills || [];
  const skillsSummary = result.skills_summary || { matched: 0, total: 0 };

  return (
    <div className="dashboard">

      {/* Top bar with re-analyze */}
      <div className="dashboard-topbar">
        <div className="dashboard-topbar-label">
          <span className="dashboard-topbar-dot" style={{ background: tier.color, boxShadow: `0 0 8px ${tier.color}` }} />
          analysis complete
        </div>
        <button className="reanalyze-btn" onClick={onReset}>
          ↺ Analyze another
        </button>
      </div>

      {/* Hero score section */}
      <div className="score-hero">
        <ScoreGauge score={result.total_score} color={tier.color} glow={tier.glow} />
        <div className="score-hero-text">
          <div className="score-tier-label" style={{ color: tier.color }}>
            {tier.label.toUpperCase()}
          </div>
          <div className="score-tier-desc">{tierDesc}</div>
        </div>
      </div>

      {/* Skills summary strip */}
      <SkillsSummary
        matched={skillsSummary.matched}
        total={skillsSummary.total}
        color={tier.color}
      />

      {/* Breakdown grid */}
      <div className="breakdown-section">
        <div className="section-label">
          <span className="section-label-mono">01</span>
          Breakdown
        </div>
        <div className="breakdown-grid">
          {Object.entries(result.breakdown).map(([key, value]) => {
            const subTier = getTier(value);
            return (
              <div key={key} className="breakdown-card">
                <div className="breakdown-card-label">{BREAKDOWN_LABELS[key] || key}</div>
                <div className="breakdown-card-value" style={{ color: subTier.color }}>
                  {value}
                  <span className="breakdown-card-unit">/100</span>
                </div>
                <MiniBar value={value} color={subTier.color} />
              </div>
            );
          })}
        </div>
      </div>

      {/* Radar */}
      <div className="radar-section">
        <div className="section-label">
          <span className="section-label-mono">02</span>
          Score radar
        </div>
        <div className="radar-wrapper">
          <ResponsiveContainer width="100%" height={360}>
            <RadarChart data={radarData} outerRadius="75%" margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
              <PolarGrid stroke="rgba(255,255,255,0.1)" />
              <PolarAngleAxis
                dataKey="subject"
                tick={{ fill: "#a1a1aa", fontSize: 12, fontFamily: "Inter" }}
              />
              <Radar
                dataKey="value"
                stroke={tier.color}
                fill={tier.color}
                fillOpacity={0.25}
                strokeWidth={2}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Two-column: strengths + matched / missing + suggestions */}
      <div className="insights-grid">

        {/* Left column */}
        <div className="insights-col">
          {strengths.length > 0 && (
            <div className="insights-block">
              <div className="section-label">
                <span className="section-label-mono">03</span>
                Strengths
              </div>
              <ul className="insights-list">
                {strengths.map((s, i) => (
                  <li key={i} className="insights-list-item insights-list-item--positive">
                    <span className="check-icon">✓</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {matched.length > 0 && (
            <div className="insights-block">
              <div className="section-label">
                <span className="section-label-mono">04</span>
                Skills you have
              </div>
              <div className="chip-group">
                {matched.map((s, i) => (
                  <span key={i} className="chip chip--matched">{s}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right column */}
        <div className="insights-col">
          {missing.length > 0 && (
            <div className="insights-block">
              <div className="section-label">
                <span className="section-label-mono">05</span>
                Skills to add
              </div>
              <div className="chip-group">
                {missing.map((s, i) => (
                  <span key={i} className="chip chip--missing">{s}</span>
                ))}
              </div>
            </div>
          )}

          {suggestions.length > 0 && (
            <div className="insights-block">
              <div className="section-label">
                <span className="section-label-mono">06</span>
                Suggestions
              </div>
              <ul className="insights-list">
                {visible.map((s, i) => (
                  <li key={i} className="insights-list-item">
                    <span className="arrow-icon">→</span>
                    {s}
                  </li>
                ))}
              </ul>
              {hidden > 0 && (
                <button
                  className="expand-btn"
                  onClick={() => setShowAllSuggestions((v) => !v)}
                >
                  {showAllSuggestions ? "Show less" : `Show ${hidden} more`}
                </button>
              )}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}

export default ScoreDashboard;