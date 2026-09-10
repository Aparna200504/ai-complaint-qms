from pathlib import Path

from app.graph.workflow import complaint_graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_invalid_complaint_stops_before_risk_assessment():
    file_path = PROJECT_ROOT / "sample_data" / "invalid_complaint.txt"

    result = complaint_graph.invoke(
        {"file_path": str(file_path)}
    )

    validation = result.get("validation_result")

    assert validation is not None
    assert validation["valid"] is False
    assert validation["errors"]

    assert result.get("risk_assessment") is None
    assert result.get("error") is None