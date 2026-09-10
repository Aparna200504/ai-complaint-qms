# AI Complaint Intake Assistant

An AI-powered pharmaceutical complaint intake and QMS workflow that converts unstructured complaint information into a structured complaint form, validates the data, performs AI-assisted risk assessment, supports conversational editing, and commits finalized complaints to a local QMS Ledger.

## Overview

Pharmaceutical complaints can arrive through emails, documents, text, and other unstructured formats. This application provides a human-in-the-loop workflow for converting that information into a structured complaint record.

The system combines:

- Document extraction
- LLM-based complaint parsing
- Deterministic validation
- AI risk assessment
- Conversational complaint editing
- Human review
- QMS Ledger persistence

### Workflow

```text
Complaint File / Text
	|
	v
Document Extraction
	|
	v
Complaint Parser
	|
	v
ComplaintForm
	|
	v
Deterministic Validation
	|
	+---- Invalid ----> Draft + Validation Issues
	|
	v
AI Risk Assessment
	|
	v
Human Review
	|
	v
Conversational Editing
	|
	v
Re-validation + Risk Reassessment
	|
	v
Commit to QMS Ledger
	|
	v
SQLite Database
```

## Features

### Complaint Intake

Supports:

- PDF
- DOCX
- TXT
- EML
- Manually entered complaint text

Image-based/scanned PDFs are not OCR processed in the current version.

### AI Complaint Parsing

The complaint parser extracts structured information into a `ComplaintForm`.

The form includes:

- Complaint Source
- Customer Name
- Product Name
- Product Strength / Grade
- Batch / Lot Number
- Affected Quantity
- Manufacturing Date
- Expiry Date
- Originating Site Block
- Impacted Non-Product Materials (NPM)
- Complaint Category
- Complaint Description
- Complaint Date
- Initial Severity
- Priority

Missing information is represented as `null` rather than being invented.

### Deterministic Validation

Validation is performed using Python rules rather than an LLM.

The current validation checks:

- Required fields
- Date format
- Numeric quantity information

Invalid complaints can remain as drafts for human correction.

### AI Risk Assessment

A separate reasoning model evaluates validated complaints and provides:

- Suggested Severity
- Suggested Next Action
- Initial Risk Assessment

Risk categories:

- Critical
- Major
- Minor

The risk assessment is AI-generated and intended for human review before committing the complaint.

### Conversational Editing

The RHS AI Copilot allows users to modify complaint information using natural language.

Examples:

```
Change the affected quantity to 20 bottles.

Set the customer name to Apollo Pharmacy.

Set the impacted non-product materials to PVC.
```

After an edit:

```
User Instruction
      |
      v
AI Complaint Editor
      |
      v
Updated ComplaintForm
      |
      v
Validation
      |
      v
Risk Reassessment
```

The LHS review form remains read-only. Human changes are performed through the conversational interface.

### QMS Ledger

After human review, a validated complaint and its final risk assessment can be committed to the QMS Ledger.

The development version uses SQLite.

Each committed record stores:

- Complaint information
- Risk assessment
- Severity
- Suggested next action
- Commit status
- Creation timestamp

## Tech Stack

### Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Groq
- Pydantic
- SQLite
- PyPDF2
- pdfplumber
- python-docx
- Python email parser

### Frontend

- React
- Vite
- Redux Toolkit
- JavaScript
- CSS

### AI Models

The current Groq configuration uses:

- `openai/gpt-oss-20b` for complaint extraction and conversational editing
- `openai/gpt-oss-120b` for risk assessment

Model configuration is stored through environment variables rather than hard-coded API credentials.

## Project Structure

```
ai-complaint-qms/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── agents/
│   │   │
│   │   ├── graph/
│   │   │   ├── conditions.py
│   │   │   ├── nodes.py
│   │   │   ├── state.py
│   │   │   └── workflow.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   └── services/
│   │       ├── complaint_editor.py
│   │       ├── complaint_parser.py
│   │       ├── database.py
│   │       ├── document_extractor.py
│   │       ├── groq_service.py
│   │       ├── risk_assessor.py
│   │       └── validator.py
│   │
│   └── data/
│       └── qms_ledger.db
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   ├── services/
│   │   └── ...
│   └── package.json
│
├── sample_data/
├── tests/
├── .gitignore
├── README.md
└── agents.md
```

`agents.md` is intentionally excluded from version control as an internal assignment specification.

## Setup

### Prerequisites

- Python 3.12+
- Node.js 22+
- npm
- Git
- Groq API key

### Backend Setup

From the project root:

```
python -m venv .venv
```

Activate the environment on Windows:

```
.venv\Scripts\activate
```

Install backend dependencies:

```
pip install fastapi uvicorn python-multipart pydantic python-dotenv langgraph langchain langchain-groq groq PyPDF2 pdfplumber python-docx reportlab
```

Create:

```
backend/.env
```

Add:

```
GROQ_API_KEY=your_groq_api_key
GROQ_EXTRACTION_MODEL=openai/gpt-oss-20b
GROQ_REASONING_MODEL=openai/gpt-oss-120b
```

Do not commit `.env`.

### Start Backend

```
cd backend
python -m uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open another terminal:

```
cd frontend
npm install
npm run dev
```

The frontend runs through the Vite development server, normally at:

```
http://localhost:5173
```

## API Endpoints

| Method | Endpoint                 | Purpose                                  |
| ------ | ------------------------ | ---------------------------------------- |
| POST   | `/api/extract-complaint` | Extract text from uploaded document      |
| POST   | `/api/parse-complaint`   | Parse complaint text into ComplaintForm  |
| POST   | `/api/validate`          | Deterministically validate ComplaintForm |
| POST   | `/api/assess-risk`       | Generate AI risk assessment              |
| POST   | `/api/process-complaint` | Run complete file processing workflow    |
| POST   | `/api/process-text`      | Run complete text processing workflow    |
| POST   | `/api/chat`              | Conversationally edit ComplaintForm      |
| POST   | `/api/save-complaint`    | Commit complaint to QMS Ledger           |
| GET    | `/api/complaints`        | Retrieve committed complaints            |


## Testing

Backend graph tests cover:

- File/text workflow
- Valid complaint processing
- Invalid complaint routing
- Validation behavior

Run tests from the backend environment:

```
python -m pytest
```

## Human-in-the-Loop Design

The system does not automatically commit AI output.

The intended workflow is:

1. AI extracts complaint information.
2. Deterministic validation checks the form.
3. AI generates a risk assessment.
4. Human reviews the structured complaint.
5. Human can request conversational corrections.
6. The complaint is revalidated.
7. Risk is reassessed after valid edits.
8. Human commits the final record to the QMS Ledger.

This keeps the final QMS commitment under human review.

## Current Limitations

- OCR is not implemented for scanned/image-based PDFs.
- SQLite is used for development.
- Authentication and authorization are not implemented.
- Originating Site Block options require organization-specific master data.
- Validation rules are currently limited to the implemented deterministic checks.
- Duplicate complaint detection is not currently implemented.
- Production deployment configuration is not included.

## Future Enhancements

Potential future improvements:

- OCR support for scanned PDFs
- Duplicate complaint detection
- PostgreSQL/MySQL production database
- Authentication and role-based access control
- Full audit trail for complaint edits
- Configurable site/block master data
- Expanded deterministic validation
- CI/CD pipeline
- Production containerization
- Observability and LLM tracing
- Complaint analytics and trend dashboards
