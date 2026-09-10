import { useDispatch, useSelector } from "react-redux";

import {
  setProcessing,
  setCommitted,
  setComplaintError,
  resetComplaint,
} from "./features/complaint/complaintSlice";
import { saveComplaint } from "./services/complaintApi";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import ComplaintDetails from "./components/ComplaintDetails";
import ValidationResult from "./components/ValidationResult";
import RiskAssessment from "./components/RiskAssessment";

import "./App.css";

function App() {
  const dispatch = useDispatch();
  const {
    complaint,
    riskAssessment,
    validation,
    committed,
    commitId,
    error,
  } = useSelector((state) => state.complaint);

  const handleCommit = async () => {
    if (!complaint) {
      dispatch(setComplaintError("No complaint available to commit."));
      return;
    }

    if (!validation?.valid) {
      dispatch(
        setComplaintError(
          "Please resolve validation issues before committing the complaint.",
        ),
      );
      return;
    }

    if (!riskAssessment) {
      dispatch(
        setComplaintError(
          "Risk assessment is required before committing the complaint.",
        ),
      );
      return;
    }

    dispatch(setProcessing());

    try {
      const result = await saveComplaint(complaint, riskAssessment);
      dispatch(setCommitted(result));
    } catch (commitError) {
      dispatch(setComplaintError(commitError.message));
    }
  };

  const handleNewComplaint = () => {
    dispatch(resetComplaint());
  };

  return (
    <div className="app">

      <main className="main-content">
        <div className="left-panel">

          <Header />

          <ComplaintDetails />

          <ValidationResult />

          <RiskAssessment />

          {error && (
            <div className="error-card">
              {error}
            </div>
          )}

          {complaint && riskAssessment && (
            committed ? (
              <div className="commit-actions">
                <div className="commit-success">
                  ✓ Complaint committed successfully
                  {commitId && ` — QMS Record #${commitId}`}
                </div>

                <button
                  type="button"
                  className="new-complaint-button"
                  onClick={handleNewComplaint}
                >
                  + New Complaint
                </button>
              </div>
            ) : (
              <button
                type="button"
                className="commit-button"
                onClick={handleCommit}
                disabled={!complaint || !validation?.valid || !riskAssessment}
              >
                Commit to QMS Ledger
              </button>
            )
          )}

        </div>

        <aside className="right-panel">
          <FileUpload />
        </aside>

      </main>

    </div>
  );
}

export default App;