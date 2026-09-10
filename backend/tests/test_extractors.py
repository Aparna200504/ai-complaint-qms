from pathlib import Path
from docx import Document
from email.message import EmailMessage
from reportlab.pdfgen import canvas

from app.services.document_extractor import extract_document


SAMPLE_TEXT = """Subject: Complaint regarding Paracetamol 650 mg tablets

Complaint Source: Email
Customer Name: ABC Healthcare
Product Name: Paracetamol Tablets
Product Strength/Grade: 650 mg
Batch/Lot Number: P650-2408
Manufacturing Date: 08/15/2024
Expiry Date: 08/14/2026
Quantity Affected: 25 boxes
Complaint Type: Product Quality
Complaint Date: 09/08/2026

Detailed Complaint Description:
ABC Healthcare reported that several Paracetamol 650 mg tablets from
batch P650-2408 were found discolored and had visible surface spots.
Approximately 25 boxes are affected.

Initial Severity: Major
Priority: High
"""


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_DIR = PROJECT_ROOT / "sample_data"

txt_path = TEST_DIR / "test_complaint.txt"
pdf_path = TEST_DIR / "test_complaint.pdf"
docx_path = TEST_DIR / "test_complaint.docx"
eml_path = TEST_DIR / "test_complaint.eml"


# TXT
txt_path.write_text(SAMPLE_TEXT, encoding="utf-8")


# DOCX
document = Document()
for line in SAMPLE_TEXT.splitlines():
    document.add_paragraph(line)

document.save(docx_path)


# PDF
pdf = canvas.Canvas(str(pdf_path))
y = 800

for line in SAMPLE_TEXT.splitlines():
    pdf.drawString(50, y, line)
    y -= 15

    if y < 50:
        pdf.showPage()
        y = 800

pdf.save()


# EML
email = EmailMessage()
email["Subject"] = "Complaint regarding Paracetamol 650 mg tablets"
email["From"] = "customer@example.com"
email["To"] = "qms@example.com"
email.set_content(SAMPLE_TEXT)

eml_path.write_bytes(email.as_bytes())


# Test all formats
for file_path in [txt_path, pdf_path, docx_path, eml_path]:
    print("\n" + "=" * 60)
    print(f"Testing: {file_path.name}")
    print("=" * 60)

    extracted = extract_document(str(file_path))

    print(extracted[:500])
    print("\nExtraction successful!")


print("\nAll extractor tests completed.")