import { useSelector } from "react-redux";

function ValidationResult() {
  const validation = useSelector(
    (state) => state.complaint.validation,
  );

  if (!validation) {
    return null;
  }

  return (
    <div
      className={`validation-card ${
        validation.valid ? "valid" : "invalid"
      }`}
    >
      <span className="validation-icon">
        {validation.valid ? "✓" : "!"}
      </span>

      <div>
        <strong>
          {validation.valid
            ? "Complaint validated successfully"
            : "Validation issues detected"}
        </strong>

        {!validation.valid &&
          validation.errors?.map((error, index) => (
            <p key={index}>{error}</p>
          ))}
      </div>
    </div>
  );
}

export default ValidationResult;