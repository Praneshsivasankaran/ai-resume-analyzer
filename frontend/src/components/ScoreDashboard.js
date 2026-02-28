import React, { useEffect, useState } from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer
} from "recharts";

function ScoreDashboard({ result }) {

  const data = [
    { subject: "Keyword", value: result.breakdown.keyword },
    { subject: "ATS", value: result.breakdown.ats },
    { subject: "Impact", value: result.breakdown.impact },
    { subject: "Skills", value: result.breakdown.skills },
    { subject: "Structure", value: result.breakdown.structure },
    { subject: "Grammar", value: result.breakdown.grammar }
  ];

  const getTier = (score) => {
    if (score >= 85) return { label: "Excellent", color: "#16A34A" };
    if (score >= 70) return { label: "Strong", color: "#2563EB" };
    if (score >= 50) return { label: "Moderate", color: "#F59E0B" };
    return { label: "Needs Improvement", color: "#EF4444" };
  };

  const tier = getTier(result.total_score);

  const getTierDescription = (score) => {
    if (score >= 85)
      return "Your resume shows excellent alignment with this job description. Minor refinements may further strengthen it.";
    if (score >= 70)
      return "Your resume is strongly aligned with this role, with a few areas that could be improved.";
    if (score >= 50)
      return "Your resume has moderate alignment. Address missing skills and keywords to improve competitiveness.";
    return "Your resume requires significant improvement to match this job description effectively.";
  };

  const tierDescription = getTierDescription(result.total_score);

  const getScoreColor = (score) => {
    if (score >= 80) return "#22C55E";
    if (score >= 60) return "#F59E0B";
    return "#EF4444";
  };

  const scoreColor = getScoreColor(result.total_score);

  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = Math.round(result.total_score);
    const duration = 800;
    const incrementTime = 20;
    const step = Math.ceil(end / (duration / incrementTime));

    const counter = setInterval(() => {
      start += step;
      if (start >= end) {
        start = end;
        clearInterval(counter);
      }
      setDisplayScore(start);
    }, incrementTime);

    return () => clearInterval(counter);
  }, [result.total_score]);

  const strengths = [];

  if (result.breakdown.ats >= 90)
    strengths.push("Excellent ATS formatting and structure.");

  if (result.breakdown.impact >= 80)
    strengths.push("Strong quantified achievements detected.");

  if (result.breakdown.grammar >= 80)
    strengths.push("High grammar quality.");

  if (result.breakdown.structure >= 90)
    strengths.push("Well-organized resume structure.");

  return (
    <div style={{ marginTop: "50px", animation: "slideIn 0.6s ease-out" }}>

      {/* SCORE CARD */}
      <div
        style={{
          background: scoreColor,
          color: "white",
          padding: "60px",
          borderRadius: "24px",
          textAlign: "center",
          marginBottom: "35px",
          boxShadow: `0 20px 40px ${scoreColor}80`
        }}
      >
        <h2 style={{ fontWeight: "400", fontSize: "20px", letterSpacing: "1px" }}>
          RESUME SCORE
        </h2>

        <h1 style={{ fontSize: "82px", margin: "20px 0", fontWeight: "700" }}>
          {displayScore}
        </h1>

        <div
          style={{
            display: "inline-block",
            padding: "10px 22px",
            borderRadius: "25px",
            background: "white",
            color: tier.color,
            fontWeight: "600",
            fontSize: "15px"
          }}
        >
          {tier.label}
        </div>
      </div>

      {/* TIER DESCRIPTION */}
      <div
        style={{
          background: "#EEF2FF",
          padding: "25px 40px",
          borderRadius: "16px",
          marginBottom: "45px",
          textAlign: "center",
          boxShadow: "0 8px 20px rgba(0,0,0,0.05)"
        }}
      >
        <p
          style={{
            margin: 0,
            fontSize: "17px",
            fontWeight: "500",
            color: "#1E293B",
            lineHeight: "1.6"
          }}
        >
          {tierDescription}
        </p>
      </div>

      {/* BREAKDOWN CARDS */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
          gap: "25px",
          marginBottom: "50px"
        }}
      >
        {Object.entries(result.breakdown).map(([key, value]) => (
          <div
            key={key}
            style={{
              background: "white",
              padding: "25px",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 10px 20px rgba(0,0,0,0.05)"
            }}
          >
            <h4
              style={{
                marginBottom: "10px",
                textTransform: "capitalize",
                fontSize: "14px",
                color: "#64748B"
              }}
            >
              {key}
            </h4>
            <h2 style={{ color: "#4F46E5", fontSize: "28px" }}>{value}</h2>
          </div>
        ))}
      </div>

      {/* RADAR + SIDE PANEL */}
      <div style={{ display: "flex", gap: "40px", flexWrap: "wrap" }}>

        <div style={{ flex: 1, minWidth: "320px", height: 420 }}>
          <ResponsiveContainer>
            <RadarChart data={data}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar
                dataKey="value"
                stroke={scoreColor}
                fill={scoreColor}
                fillOpacity={0.5}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: 1, minWidth: "320px" }}>

          {strengths.length > 0 && (
            <>
              <h3 style={{ fontSize: "20px", marginBottom: "15px" }}>
                Strengths
              </h3>
              <ul style={{ marginBottom: "25px" }}>
                {strengths.map((item, index) => (
                  <li key={index} style={{ marginBottom: "10px", color: "#16A34A", fontSize: "15px" }}>
                    {item}
                  </li>
                ))}
              </ul>
            </>
          )}

          <h3 style={{ fontSize: "20px", marginBottom: "15px" }}>
            Missing Skills
          </h3>

          <div style={{ marginBottom: "25px" }}>
            {result.missing_skills.map((skill, index) => (
              <span
                key={index}
                style={{
                  display: "inline-block",
                  background: "#E0E7FF",
                  color: "#3730A3",
                  padding: "8px 14px",
                  borderRadius: "20px",
                  margin: "6px",
                  fontSize: "14px"
                }}
              >
                {skill}
              </span>
            ))}
          </div>

          <h3 style={{ fontSize: "20px", marginBottom: "15px" }}>
            Suggestions
          </h3>

          <ul>
            {result.suggestions.map((s, index) => (
              <li key={index} style={{ marginBottom: "12px", fontSize: "15px" }}>
                {s}
              </li>
            ))}
          </ul>

        </div>
      </div>
    </div>
  );
}

export default ScoreDashboard;