from pathlib import Path

from app.services.document_extractor import extract_document
from app.services.complaint_parser import parse_complaint


PROJECT_ROOT = Path(__file__).resolve().parents[2]


file_path = PROJECT_ROOT / "sample_data" / "sample_complaint.txt"

text = extract_document(file_path)

print("Extracted text successfully.")
print("\nSending complaint to Groq...\n")

complaint = parse_complaint(text)

print("ComplaintForm created successfully!\n")
print(complaint.model_dump_json(indent=2))