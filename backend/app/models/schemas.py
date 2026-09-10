from typing import Optional

from pydantic import BaseModel, Field


class ComplaintForm(BaseModel):
    # Category 1: Origin & Customer Details
    complaint_source: Optional[str] = Field(
        None,
        description="Source of the complaint, e.g. Pharmacy, Email, Phone, Portal",
    )
    customer_name: Optional[str] = Field(
        None,
        description="Name of the customer or complainant",
    )

    # Category 2: Product & Batch Identification
    product_name: Optional[str] = Field(
        None,
        description="Name of the pharmaceutical product",
    )
    product_strength_grade: Optional[str] = Field(
        None,
        description="Strength or grade of the product",
    )
    batch_lot_number: Optional[str] = Field(
        None,
        description="Batch or Lot number",
    )
    quantity_affected: Optional[str] = Field(
        None,
        description="Quantity affected with unit",
    )
    manufacturing_date: Optional[str] = Field(
        None,
        description="Manufacturing date as provided in the complaint",
    )
    expiry_date: Optional[str] = Field(
        None,
        description="Expiry date as provided in the complaint",
    )

    # Category 3: Facility & Material Impact
    originating_site_block: Optional[str] = Field(
        None,
        description="Originating site block",
    )
    impacted_non_product_materials: Optional[str] = Field(
        None,
        description="Impacted non-product materials (NPM)",
    )

    # Category 4: Defect Analysis
    complaint_type: Optional[str] = Field(
        None,
        description="Complaint category or type",
    )
    detailed_complaint_description: Optional[str] = Field(
        None,
        description="Detailed description of the complaint",
    )

    # Existing intake / triage fields
    complaint_date: Optional[str] = Field(
        None,
        description="Date complaint was received",
    )
    initial_severity: Optional[str] = Field(
        None,
        description="Initial severity: Critical, Major, or Minor",
    )
    priority: Optional[str] = Field(
        None,
        description="Priority of investigation: High, Medium, or Low",
    )


class RiskAssessment(BaseModel):
    severity: str = Field(
        ...,
        description="Suggested severity: Critical, Major, or Minor",
    )
    suggested_next_action: str = Field(
        ...,
        description="Suggested next step",
    )
    initial_risk_assessment: str = Field(
        ...,
        description="Brief rationale explaining the potential risk",
    )
    
class TextComplaintRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str
    current_form: ComplaintForm


class ChatResponse(BaseModel):
    updated_form: ComplaintForm
    validation: dict
    risk_assessment: Optional[RiskAssessment] = None


class SaveComplaintRequest(BaseModel):
    complaint: ComplaintForm
    risk_assessment: RiskAssessment