import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.models.schemas import ComplaintForm, RiskAssessment

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "qms_ledger.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_source TEXT,
                customer_name TEXT,
                product_name TEXT,
                batch_lot_number TEXT,
                complaint_type TEXT,
                complaint_date TEXT,
                severity TEXT,
                suggested_next_action TEXT,
                complaint_json TEXT NOT NULL,
                risk_assessment_json TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Committed',
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def save_complaint(
    complaint: ComplaintForm,
    risk_assessment: RiskAssessment,
):
    initialize_database()

    complaint_data = complaint.model_dump()
    risk_data = risk_assessment.model_dump()

    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO complaints (
                complaint_source,
                customer_name,
                product_name,
                batch_lot_number,
                complaint_type,
                complaint_date,
                severity,
                suggested_next_action,
                complaint_json,
                risk_assessment_json,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                complaint.complaint_source,
                complaint.customer_name,
                complaint.product_name,
                complaint.batch_lot_number,
                complaint.complaint_type,
                complaint.complaint_date,
                risk_assessment.severity,
                risk_assessment.suggested_next_action,
                json.dumps(complaint_data),
                json.dumps(risk_data),
                "Committed",
                created_at,
            ),
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "status": "Committed",
            "created_at": created_at,
        }

    finally:
        connection.close()


def get_saved_complaints():
    initialize_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                complaint_source,
                customer_name,
                product_name,
                batch_lot_number,
                complaint_type,
                complaint_date,
                severity,
                suggested_next_action,
                status,
                created_at
            FROM complaints
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()
