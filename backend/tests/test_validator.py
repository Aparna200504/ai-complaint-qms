from app.models.schemas import ComplaintForm
from app.services.validator import validate_complaint


valid_complaint = ComplaintForm(
    complaint_source="Email",
    customer_name="ABC Healthcare",
    product_name="Paracetamol Tablets",
    product_strength_grade="650 mg",
    batch_lot_number="P650-2408",
    manufacturing_date="08/15/2024",
    expiry_date="08/14/2026",
    quantity_affected="25 boxes",
    complaint_type="Product Quality",
    complaint_date="09/08/2026",
    detailed_complaint_description=(
        "Several tablets were found discolored "
        "and had visible surface spots."
    ),
    initial_severity="Major",
    priority="High",
)


result = validate_complaint(valid_complaint)

print("Validation result:")
print(result)

assert result["valid"] is True
assert result["errors"] == []

print("\nValid complaint test: PASSED")

invalid_complaint = ComplaintForm(
    complaint_source=None,
    customer_name="ABC Healthcare",
    product_name="Paracetamol Tablets",
    batch_lot_number="P650-2408",
    complaint_type="Product Quality",
    complaint_date="2026-99-99",
    detailed_complaint_description="Test complaint",
    quantity_affected="twenty five boxes",
)


invalid_result = validate_complaint(invalid_complaint)

print("\nInvalid complaint validation:")
print(invalid_result)

assert invalid_result["valid"] is False
assert len(invalid_result["errors"]) > 0

print("\nInvalid complaint test: PASSED")