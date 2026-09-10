from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import ComplaintForm, RiskAssessment
from app.api.routes import router


app = FastAPI(
    title="AI Complaint Assistant",
    description="AI-powered pharmaceutical complaint intake and QMS system",
    version="0.1.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")   
def root():
    return {
        "message": "Welcome to the AI Complaint Intake Assistant API. "
                   "Visit /docs for API documentation.",
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-complaint-qms",
    }


@app.post("/test/complaint")
def test_complaint(complaint: ComplaintForm):
    return complaint


@app.post("/test/risk")
def test_risk(risk: RiskAssessment):
    return risk