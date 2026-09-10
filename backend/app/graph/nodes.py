from app.services.document_extractor import extract_document
from app.services.complaint_parser import parse_complaint
from app.services.validator import validate_complaint
from app.services.risk_assessor import assess_risk

from app.graph.state import ComplaintState


def extract_text_node(state: ComplaintState) -> ComplaintState:
    try:
        file_path = state["file_path"]

        extracted_text = extract_document(file_path)

        return {
            "extracted_text": extracted_text,
            "error": None,
        }

    except Exception as exc:
        return {
            "error": f"Document extraction failed: {str(exc)}",
        }

def extract_text_input_node(state: ComplaintState) -> ComplaintState:
    try:
        complaint_text = state.get("complaint_text")

        if not complaint_text or not complaint_text.strip():
            return {"error": "No complaint text available."}

        return {
            "extracted_text": complaint_text.strip(),
            "error": None,
        }

    except Exception as exc:
        return {
            "error": f"Text input processing failed: {str(exc)}"
        }
    
def parse_complaint_node(state: ComplaintState) -> ComplaintState:
    try:
        extracted_text = state.get("extracted_text")

        if not extracted_text:
            return {
                "error": "No extracted text available for parsing.",
            }

        complaint = parse_complaint(extracted_text)

        return {
            "complaint": complaint,
            "error": None,
        }

    except Exception as exc:
        return {
            "error": f"Complaint parsing failed: {str(exc)}",
        }


def validate_complaint_node(state: ComplaintState) -> ComplaintState:
    try:
        complaint = state.get("complaint")

        if complaint is None:
            return {
                "error": "No complaint available for validation.",
            }

        validation_result = validate_complaint(complaint)

        return {
            "validation_result": validation_result,
            "error": None,
        }

    except Exception as exc:
        return {
            "error": f"Complaint validation failed: {str(exc)}",
        }


def assess_risk_node(state: ComplaintState) -> ComplaintState:
    try:
        complaint = state.get("complaint")

        if complaint is None:
            return {
                "error": "No complaint available for risk assessment.",
            }

        risk_assessment = assess_risk(complaint)

        return {
            "risk_assessment": risk_assessment,
            "error": None,
        }

    except Exception as exc:
        return {
            "error": f"Risk assessment failed: {str(exc)}",
        }


def handle_error_node(state: ComplaintState) -> ComplaintState:
    print("\nWorkflow error:")
    print(state.get("error"))

    return {
        "error": state.get("error", "Unknown workflow error"),
    }

def finish_draft_node(state: ComplaintState) -> ComplaintState:
    return {
        "error": None
    }