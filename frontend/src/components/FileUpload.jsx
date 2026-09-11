import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  setProcessing,
  setComplaintResult,
  setEditedComplaint,
  setComplaintError,
} from "../features/complaint/complaintSlice";

import {
  processComplaint,
  processText,
  editComplaint,
} from "../services/complaintApi";

function FileUpload() {
  const dispatch = useDispatch();
  const fileInputRef = useRef(null);

  const [message, setMessage] = useState("");

  const {
    loading,
    complaint,
    riskAssessment,
  } = useSelector((state) => state.complaint);

  const handleFile = async (file) => {
    if (!file) {
      return;
    }

    dispatch(setProcessing());

    try {
      const result = await processComplaint(file);
      dispatch(setComplaintResult(result));
    } catch (error) {
      dispatch(setComplaintError(error.message));
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      handleFile(file);
    }

    event.target.value = "";
  };

  const handleSend = async () => {
    const userMessage = message.trim();

    if (!userMessage) {
      return;
    }

    dispatch(setProcessing());

    try {
      let result;

      const hasComplaintData =
        complaint &&
        Object.values(complaint).some(
          (value) =>
            value !== null &&
            value !== undefined &&
            String(value).trim() !== ""
        );

      if (hasComplaintData) {
        // Existing complaint → treat message as an edit
        result = await editComplaint(
          userMessage,
          complaint
        );

        dispatch(setEditedComplaint(result));
      } else {
        // No complaint yet → treat message as a new complaint
        result = await processText(userMessage);

        dispatch(setComplaintResult(result));
      }

      setMessage("");
    } catch (error) {
      dispatch(setComplaintError(error.message));
    }
  };

  return (
    <div className="copilot-panel">

      {/* COPILOT HEADER */}
      <div className="copilot-header">
        <div>
          <div className="copilot-title">
            <span className="flask-icon">⚗</span>

            <strong>AIVOA Copilot</strong>
          </div>

          <p>
            Drop complaint files or paste text below.
          </p>
        </div>

        <span className="online-dot"></span>
      </div>

      {/* CONVERSATION */}
      <div className="copilot-body">

        <div className="copilot-message assistant-message">
          <span className="message-icon">ϟ</span>

          <div>
            Ready to process new complaints. You can paste
            the raw complaint from the customer or upload a
            complaint document. I will extract the data and
            run the initial risk assessment.
          </div>
        </div>

        {complaint && (
          <div className="copilot-message user-message">
            <span className="message-icon">◯</span>

            <div>
              Complaint processed successfully.
              <br />
              <strong>
                {complaint.product_name || "Product"}
              </strong>
              {" — "}
              {complaint.complaint_type || "Complaint"}
            </div>
          </div>
        )}

        {riskAssessment && (
          <div className="copilot-message assistant-message">
            <span className="message-icon">✓</span>

            <div>
              Initial risk assessment completed.
              <br />
              Suggested severity:
              {" "}
              <strong>{riskAssessment.severity}</strong>
            </div>
          </div>
        )}

        {loading && (
          <div className="processing-message">
            Processing complaint...
          </div>
        )}
      </div>

      {/* INPUT AREA */}
      <div className="copilot-input-area">

        <div className="input-row">

          <button
            type="button"
            className="attachment-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            title="Upload complaint"
          >
            📎
          </button>

          <textarea
            value={message}
            onChange={(event) =>
              setMessage(event.target.value)
            }
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey
              ) {
                event.preventDefault();
                handleSend();
              }
            }}
            placeholder="Type a message or paste a complaint..."
            disabled={loading}
          />

          <button
            type="button"
            className="send-button"
            onClick={handleSend}
            disabled={loading || !message.trim()}
          >
            ✓
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt,.eml"
            onChange={handleFileChange}
            hidden
          />

        </div>

        <div className="upload-hint">
          Supported files: PDF · DOCX · TXT · EML
        </div>

      </div>

      <div className="copilot-footer">
        POWERED BY LANGGRAPH
      </div>

    </div>
  );
}

export default FileUpload;