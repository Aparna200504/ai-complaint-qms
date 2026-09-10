from pathlib import Path

from app.services.risk_assessor import assess_risk
from app.services.document_extractor import extract_document
from app.services.complaint_parser import parse_complaint
from app.services.validator import validate_complaint


PROJECT_ROOT = Path(__file__).resolve().parents[2]
file_path = PROJECT_ROOT / "sample_data" / "sample_complaint.txt"

# 1. Extract
text = extract_document(file_path)
print("Step 1: Document extraction successful.")

# 2. Parse
complaint = parse_complaint(text)
print("Step 2: Complaint parsing successful.")

# 3. Validate
validation = validate_complaint(complaint)
print("Step 3: Validation result:")
print(validation)

if not validation["valid"]:
    raise ValueError(
        f"Complaint is invalid. Cannot perform risk assessment: "
        f"{validation['errors']}"
    )

# 4. Assess risk
risk = assess_risk(complaint)

print("\nStep 4: Risk assessment successful.")
print("\nRiskAssessment:")
print(risk.model_dump_json(indent=2))