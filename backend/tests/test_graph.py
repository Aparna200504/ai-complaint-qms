from pathlib import Path

from app.graph.workflow import complaint_graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_complaint_graph():
    file_path = PROJECT_ROOT / "sample_data" / "sample_complaint.txt"

    result = complaint_graph.invoke(
        {
            "file_path": str(file_path)
        }
    )

    # Extraction should succeed
    assert result.get("extracted_text")

    # Complaint parsing should succeed
    complaint = result.get("complaint")
    assert complaint is not None

    # Validation should succeed
    validation = result.get("validation_result")
    assert validation is not None
    assert validation["valid"] is True
    assert validation["errors"] == []

    # Risk assessment should succeed
    risk = result.get("risk_assessment")
    assert risk is not None
    assert risk.severity in {"Critical", "Major", "Minor"}
    assert risk.suggested_next_action
    assert risk.initial_risk_assessment

    # Workflow should finish without an error
    assert result.get("error") is None