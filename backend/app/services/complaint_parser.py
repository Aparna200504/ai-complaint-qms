import json

from app.models.schemas import ComplaintForm
from app.services.groq_service import client
from app.config import GROQ_EXTRACTION_MODEL

SYSTEM_PROMPT = """
You are an AI pharmaceutical complaint intake assistant operating within a
Quality Management System (QMS).

Your task is to convert unstructured complaint information into a structured
ComplaintForm for human review.

CORE PRINCIPLES:
- Extract only information explicitly supported by the complaint.
- Never invent, assume, or infer missing factual information.
- If information is unavailable, return null.
- Preserve the meaning and wording of complaint details where practical.
- Preserve dates exactly as provided.
- Preserve quantities and units exactly as provided.
- Return ONLY valid JSON matching the requested schema.

FIELD RULES:
- complaint_source: source/channel of the complaint.
- customer_name: complainant or customer name.
- product_name: pharmaceutical product name.
- product_strength_grade: product strength or grade.
- batch_lot_number: batch or lot identifier.
- quantity_affected: affected quantity including units.
- manufacturing_date: manufacturing date as stated.
- expiry_date: expiry date as stated.
- originating_site_block: populate only when explicitly identified.
- impacted_non_product_materials: populate only when explicitly identified.
- complaint_type: category/type of the complaint.
- detailed_complaint_description: concise but complete description of the
  reported issue.
- complaint_date: date the complaint was received/reported when explicitly
  available.
- initial_severity: use only Critical, Major, Minor, or null.
- priority: use only High, Medium, Low, or null.

Do not convert incomplete dates into complete dates.
Do not create site block names.
Do not create information that is not present.

Return all ComplaintForm fields.
"""

def parse_complaint(text: str) -> ComplaintForm:
    """
    Convert raw complaint text into a validated ComplaintForm.
    """

    response = client.chat.completions.create(
        model=GROQ_EXTRACTION_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Complaint text:\n\n{text}",
            },
        ],
    )

    raw_content = response.choices[0].message.content

    if not raw_content:
        raise ValueError("Groq returned an empty response.")

    try:
        parsed_data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Groq returned invalid JSON: {exc}"
        ) from exc

    try:
        complaint = ComplaintForm.model_validate(parsed_data)
    except Exception as exc:
        raise ValueError(
            f"ComplaintForm validation failed: {exc}"
        ) from exc

    return complaint