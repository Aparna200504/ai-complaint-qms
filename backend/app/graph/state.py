from typing import Optional, TypedDict

from app.models.schemas import ComplaintForm, RiskAssessment


class ComplaintState(TypedDict, total=False):
    file_path: Optional[str]
    complaint_text: Optional[str]
    extracted_text: Optional[str]
    complaint: Optional[ComplaintForm]
    validation_result: Optional[dict]
    risk_assessment: Optional[RiskAssessment]
    error: Optional[str]