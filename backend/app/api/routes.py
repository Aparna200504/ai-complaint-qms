from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, UploadFile, HTTPException


from app.models.schemas import (
    ComplaintForm,
    RiskAssessment,
    ChatRequest,
    ChatResponse,
    TextComplaintRequest,
    SaveComplaintRequest,
)

from app.services.document_extractor import extract_document
from app.services.complaint_parser import parse_complaint
from app.services.complaint_editor import edit_complaint
from app.services.validator import validate_complaint
from app.services.risk_assessor import assess_risk
from app.services.database import save_complaint, get_saved_complaints


from app.graph.workflow import complaint_graph

router = APIRouter(prefix="/api", tags=["Complaint"])

@router.post("/validate")
async def validate_complaint_endpoint(complaint: ComplaintForm):
    """
    Validate a ComplaintForm using deterministic Python rules.
    """

    result = validate_complaint(complaint)

    return {
        "complaint": complaint.model_dump(),
        "validation": result,
    }

@router.post("/assess-risk", response_model=RiskAssessment)
async def assess_risk_endpoint(complaint: ComplaintForm):
    try:
        return assess_risk(complaint)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(exc)}",
        )

@router.post("/process-complaint")
async def process_complaint(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx", ".txt", ".eml"}

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Supported formats: {', '.join(sorted(allowed_extensions))}"
            ),
        )

    temporary_path = None

    try:
        file_contents = await file.read()

        with NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temporary_file:
            temporary_file.write(file_contents)
            temporary_path = temporary_file.name

        result = complaint_graph.invoke(
            {
                "file_path": temporary_path
            }
        )

        if result.get("error"):
            raise HTTPException(
                status_code=500,
                detail=result["error"],
            )

        complaint = result.get("complaint")
        validation_result = result.get("validation_result")
        risk_assessment = result.get("risk_assessment")

        return {
            "filename": file.filename,
            "file_type": extension,
            "extracted_text": result.get("extracted_text"),
            "complaint": (
                complaint.model_dump()
                if complaint
                else None
            ),
            "validation": validation_result,
            "risk_assessment": (
                risk_assessment.model_dump()
                if risk_assessment
                else None
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Complaint processing failed: {str(exc)}",
        )

    finally:
        if temporary_path:
            Path(temporary_path).unlink(missing_ok=True)


@router.post("/process-text")
def process_text_complaint(request: TextComplaintRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Complaint text cannot be empty.",
        )

    try:
        result = complaint_graph.invoke(
            {
                "complaint_text": request.text.strip()
            }
        )

        if result.get("error"):
            raise HTTPException(
                status_code=500,
                detail=result["error"],
            )

        complaint = result.get("complaint")
        validation_result = result.get("validation_result")
        risk_assessment = result.get("risk_assessment")

        return {
            "filename": None,
            "file_type": "text",
            "extracted_text": result.get("extracted_text"),
            "complaint": (
                complaint.model_dump()
                if complaint
                else None
            ),
            "validation": validation_result,
            "risk_assessment": (
                risk_assessment.model_dump()
                if risk_assessment
                else None
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Complaint text processing failed: {str(exc)}",
        )


@router.post("/chat", response_model=ChatResponse)
def chat_with_complaint_editor(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        updated_form = edit_complaint(
            current_form=request.current_form,
            user_message=request.message,
        )

        validation = validate_complaint(updated_form)

        risk_assessment = None

        if validation.get("valid") is True:
            risk_assessment = assess_risk(updated_form)

        return {
            "updated_form": updated_form.model_dump(),
            "validation": validation,
            "risk_assessment": (
                risk_assessment.model_dump()
                if risk_assessment
                else None
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Complaint editing failed: {str(exc)}",
        )


@router.post("/save-complaint")
def save_complaint_endpoint(request: SaveComplaintRequest):
    """
    Commit a human-reviewed complaint and its final
    AI risk assessment to the QMS Ledger.
    """

    try:
        validation = validate_complaint(request.complaint)

        if not validation.get("valid"):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Complaint cannot be committed.",
                    "validation_errors": validation.get("errors", []),
                },
            )

        saved_record = save_complaint(
            complaint=request.complaint,
            risk_assessment=request.risk_assessment,
        )

        return {
            "success": True,
            "message": "Complaint committed to QMS Ledger successfully.",
            "record": saved_record,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save complaint: {str(exc)}",
        )


@router.get("/complaints")
def get_complaints():
    """
    Return complaints committed to the QMS Ledger.
    """

    try:
        complaints = get_saved_complaints()

        return {
            "count": len(complaints),
            "complaints": complaints,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve complaints: {str(exc)}",
        )


@router.post("/extract-complaint")
async def extract_complaint(file: UploadFile = File(...)):
    """
    Upload a complaint document and extract its raw text.
    Supported formats: PDF, DOCX, TXT, EML.
    """

    allowed_extensions = {".pdf", ".docx", ".txt", ".eml"}

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Supported formats: {', '.join(sorted(allowed_extensions))}"
            ),
        )

    try:
        file_contents = await file.read()

        with NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temporary_file:
            temporary_file.write(file_contents)
            temporary_path = temporary_file.name

        try:
            extracted_text = extract_document(temporary_path)
        finally:
            Path(temporary_path).unlink(missing_ok=True)

        return {
            "filename": file.filename,
            "file_type": extension,
            "extracted_text": extracted_text,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document extraction failed: {str(exc)}",
        )

@router.post("/parse-complaint")
async def parse_complaint_endpoint(text: str):
    """
    Convert raw complaint text into a validated ComplaintForm.
    """

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Complaint text cannot be empty.",
        )

    try:
        complaint = parse_complaint(text)

        return complaint.model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Complaint parsing failed: {str(exc)}",
        )
