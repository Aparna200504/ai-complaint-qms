import { useSelector } from "react-redux";

function RiskAssessment() {
  const riskAssessment = useSelector(
    (state) => state.complaint.riskAssessment,
  );

  if (!riskAssessment) {
    return null;
  }

  return (
    <section className="risk-card">
      <div className="risk-title">
        <span className="risk-shield">♢</span>

        <h2>AI Copilot Risk Assessment</h2>
      </div>

      <div className="risk-grid">
        <div className="form-field">
          <label>Severity (Suggested)</label>

          <input
            value={riskAssessment.severity || ""}
            readOnly
          />
        </div>

        <div className="form-field">
          <label>Suggested Next Action</label>

          <input
            value={riskAssessment.suggested_next_action || ""}
            readOnly
          />
        </div>
      </div>

      <div className="form-field risk-summary">
        <label>Initial Risk Assessment</label>

        <textarea
          value={riskAssessment.initial_risk_assessment || ""}
          readOnly
        />
      </div>
    </section>
  );
}

export default RiskAssessment;