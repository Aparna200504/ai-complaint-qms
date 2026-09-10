import re
from datetime import datetime

from app.models.schemas import ComplaintForm


REQUIRED_FIELDS = [
    "complaint_source",
    "customer_name",
    "product_name",
    "batch_lot_number",
    "complaint_type",
    "complaint_date",
    "detailed_complaint_description",
]


def validate_date(value: str, field_name: str, errors: list[str]) -> None:
    """Validate that a date follows MM/DD/YYYY format."""
    try:
        datetime.strptime(value, "%m/%d/%Y")
    except ValueError:
        errors.append(
            f"{field_name} must use MM/DD/YYYY format."
        )


def validate_quantity(value: str, errors: list[str]) -> None:
    """Validate that quantity contains a numeric value."""
    if not re.search(r"\d", value):
        errors.append(
            "quantity_affected must contain a numeric quantity."
        )


def validate_complaint(complaint: ComplaintForm) -> dict:
    """
    Perform deterministic validation of a ComplaintForm.

    Returns:
        {
            "valid": bool,
            "errors": list[str]
        }
    """

    errors = []

    # 1. Required fields
    for field_name in REQUIRED_FIELDS:
        value = getattr(complaint, field_name)

        if value is None or not str(value).strip():
            errors.append(
                f"{field_name} is required."
            )

    # 2. Date validation
    date_fields = [
        "manufacturing_date",
        "expiry_date",
        "complaint_date",
    ]

    for field_name in date_fields:
        value = getattr(complaint, field_name)

        if value:
            validate_date(value, field_name, errors)

    # 3. Quantity validation
    if complaint.quantity_affected:
        validate_quantity(
            complaint.quantity_affected,
            errors,
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }