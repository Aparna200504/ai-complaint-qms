from app.graph.workflow import complaint_graph


def test_text_complaint_graph():
    complaint_text = """
    Complaint Source: Pharmacy
    Customer Name: Apollo Pharmacy
    Product Name: Amoxicillin Capsules
    Product Strength: 500 mg
    Batch/Lot Number: AMX24602
    Affected Quantity: 12 capsules
    Manufacturing Date: 03/01/2026
    Expiry Date: 02/01/2028
    Complaint Type: Product Defect - Discoloration
    Complaint Date: 09/10/2026

    Customer reported that several capsules from batch AMX24602
    showed discoloration. Approximately 12 capsules are affected.
    """

    result = complaint_graph.invoke(
        {
            "complaint_text": complaint_text
        }
    )

    assert result.get("extracted_text")

    complaint = result.get("complaint")
    assert complaint is not None

    validation = result.get("validation_result")
    assert validation is not None

    assert validation["valid"] is True
    assert validation["errors"] == []

    risk = result.get("risk_assessment")
    assert risk is not None

    assert risk.severity in {
        "Critical",
        "Major",
        "Minor",
    }

    assert risk.suggested_next_action
    assert risk.initial_risk_assessment

    assert result.get("error") is None