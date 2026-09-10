import json

from app.config import GROQ_REASONING_MODEL
from app.models.schemas import ComplaintForm, RiskAssessment
from app.services.groq_service import client

SYSTEM_PROMPT = """
You are an AI pharmaceutical Quality Management System (QMS) risk assessment
assistant.

Your task is to evaluate the provided ComplaintForm and produce a structured
RiskAssessment for human review.

IMPORTANT:
- Base the assessment only on information contained in the ComplaintForm.
- Do not invent facts.
- Do not claim certainty when the complaint information is incomplete.
- Patient safety and product quality take priority over cosmetic considerations.
- Return ONLY valid JSON matching the requested RiskAssessment schema.

SEVERITY GUIDELINES:

Critical:
- Potential patient safety risk
- Contamination or sterility concerns
- Wrong product or potentially dangerous product mix-up
- Other issues that could directly compromise patient safety

Major:
- Potential efficacy concern
- Significant packaging defect
- Significant product quality issue that may affect product performance

Minor:
- Cosmetic defect
- Minor labeling issue
- Documentation issue
- Low-risk issue without an apparent patient safety or product quality impact

NEXT ACTION GUIDELINES:

Use the action that best matches the complaint:

- Immediate Recall & Root Cause Analysis
  For serious patient safety, contamination, sterility, or wrong-product
  concerns.

- Route to QA Investigation & Issue Replacement
  For significant product quality, efficacy, or packaging concerns.

- Request Return Sample for Testing
  When physical product evaluation is needed to determine the issue.

- Log for Trend Analysis Only
  For minor, low-risk, cosmetic, labeling, or documentation issues.

Return:
1. severity
2. suggested_next_action
3. initial_risk_assessment

The initial_risk_assessment must briefly explain why the suggested severity
and action are appropriate.
"""

def assess_risk(complaint: ComplaintForm) -> RiskAssessment:
    complaint_data = complaint.model_dump()

    user_prompt = f"""
Assess the following pharmaceutical complaint:

Product: {complaint_data.get("product_name")}
Product Strength/Grade: {complaint_data.get("product_strength_grade")}
Batch/Lot: {complaint_data.get("batch_lot_number")}
Quantity Affected: {complaint_data.get("quantity_affected")}
Complaint Type: {complaint_data.get("complaint_type")}
Description: {complaint_data.get("detailed_complaint_description")}
Initial Severity: {complaint_data.get("initial_severity")}
Priority: {complaint_data.get("priority")}

Return the risk assessment as JSON.
"""

    response = client.chat.completions.create(
        model=GROQ_REASONING_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    raw_content = response.choices[0].message.content

    if not raw_content:
        raise ValueError("Groq returned an empty risk assessment.")

    try:
        parsed_data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Groq returned invalid JSON for risk assessment: {exc}"
        ) from exc

    try:
        risk_assessment = RiskAssessment.model_validate(parsed_data)
    except Exception as exc:
        raise ValueError(
            f"RiskAssessment validation failed: {exc}"
        ) from exc

    return risk_assessment