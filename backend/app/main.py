from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CalAI MVP API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv", ".json", ".xlsx", ".ehb"}


class LoginRequest(BaseModel):
    username: str
    password: str


class AskRequest(BaseModel):
    question: str = Field(min_length=3)


@dataclass
class ParsedEHB:
    functions: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    calibrations: list[str] = field(default_factory=list)


@dataclass
class DocumentRecord:
    doc_id: str
    filename: str
    text: str
    entities: ParsedEHB


@dataclass
class AppState:
    users: dict[str, dict[str, str]] = field(
        default_factory=lambda: {"engineer": {"password": "calai", "role": "engineer"}}
    )
    tokens: dict[str, str] = field(default_factory=dict)
    documents: dict[str, DocumentRecord] = field(default_factory=dict)


state = AppState()


def parse_ehb_text(text: str) -> ParsedEHB:
    pattern_sets = {
        "functions": r"\b(?:FN|Function)[:\s_\-]*([A-Za-z0-9_]+)",
        "signals": r"\b(?:SIG|Signal)[:\s_\-]*([A-Za-z0-9_]+)",
        "diagnostics": r"\b(?:DTC|Diag)[:\s_\-]*([A-Za-z0-9_]+)",
        "calibrations": r"\b(?:CAL|Cal)[:\s_\-]*([A-Za-z0-9_]+)",
    }

    parsed = ParsedEHB()
    for key, pattern in pattern_sets.items():
        values = sorted({match.upper() for match in re.findall(pattern, text, re.IGNORECASE)})
        setattr(parsed, key, values)
    return parsed


def build_answer(question: str) -> tuple[str, list[dict[str, Any]], float]:
    if not state.documents:
        return (
            "No indexed documents yet. Upload engineering content to start Q&A.",
            [],
            0.2,
        )

    lowered = question.lower()
    matches: list[DocumentRecord] = []
    for doc in state.documents.values():
        if any(token in doc.text.lower() for token in lowered.split() if len(token) > 3):
            matches.append(doc)

    if not matches:
        matches = list(state.documents.values())[:2]

    sources = [{"doc_id": doc.doc_id, "filename": doc.filename} for doc in matches[:3]]
    summary = ", ".join(src["filename"] for src in sources)
    return (
        f"Likely relevant information was found in: {summary}. Review cited sources for engineering confirmation.",
        sources,
        0.71 if matches else 0.35,
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "calai-backend"}


@app.post("/api/auth/login")
def login(payload: LoginRequest) -> dict[str, str]:
    user = state.users.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = f"token-{uuid4()}"
    state.tokens[token] = payload.username
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}


@app.get("/api/license/status")
def license_status() -> dict[str, Any]:
    return {
        "mode": "offline",
        "valid": True,
        "tier": "Professional",
        "offline_grace_days": 90,
        "feature_flags": [
            "document_upload",
            "engineering_chat",
            "signal_graph",
            "ehb_parser",
        ],
    }


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    doc_id = str(uuid4())
    entities = parse_ehb_text(text)
    state.documents[doc_id] = DocumentRecord(doc_id=doc_id, filename=file.filename or doc_id, text=text, entities=entities)

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "bytes": len(content),
        "parsed_entities": entities.__dict__,
    }


@app.get("/api/documents")
def list_documents() -> dict[str, Any]:
    return {
        "documents": [
            {"doc_id": doc.doc_id, "filename": doc.filename}
            for doc in state.documents.values()
        ]
    }


@app.post("/api/ehb/parse")
async def parse_ehb(file: UploadFile = File(...)) -> dict[str, Any]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix != ".ehb":
        raise HTTPException(status_code=400, detail="Only .ehb files are accepted for EHB parsing")

    text = (await file.read()).decode("utf-8", errors="ignore")
    parsed = parse_ehb_text(text)
    return {"filename": file.filename, "entities": parsed.__dict__}


@app.post("/api/chat/ask")
def ask_engineering_question(payload: AskRequest) -> dict[str, Any]:
    answer, sources, confidence = build_answer(payload.question)
    return {
        "question": payload.question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }


@app.get("/api/signals/{signal_name}/dependencies")
def signal_dependencies(signal_name: str) -> dict[str, Any]:
    signal_key = signal_name.upper()

    used_by = sorted(
        {
            diagnostic
            for doc in state.documents.values()
            for diagnostic in doc.entities.diagnostics
            if signal_key in doc.text.upper()
        }
    )
    related_calibrations = sorted(
        {
            calibration
            for doc in state.documents.values()
            for calibration in doc.entities.calibrations
            if signal_key in doc.text.upper()
        }
    )

    if not used_by:
        used_by = ["LP_FUEL_CONTROLLER", "P0087_DIAGNOSTICS"]
    if not related_calibrations:
        related_calibrations = ["FRP_TARGET_MIN", "LPSYS_PSET_GAIN"]

    return {
        "signal": signal_key,
        "uses": ["FUEL_RAIL_PRESSURE_ACTUAL", "PUMP_DUTY", "FUEL_TEMPERATURE"],
        "used_by": used_by,
        "related_calibrations": related_calibrations,
    }


@app.get("/api/diagnostics/{dtc}")
def diagnostics_view(dtc: str) -> dict[str, Any]:
    code = dtc.upper()
    return {
        "dtc": code,
        "enable_conditions": ["Engine running", "Fuel system enabled"],
        "entry_conditions": ["Rail pressure below threshold for calibrated duration"],
        "exit_conditions": ["Rail pressure recovers above threshold"],
        "inhibit_conditions": ["Cranking", "Sensor invalid"],
        "calibrations": ["FRP_TARGET_MIN", "LP_PRESSURE_FAIL_DELAY"],
        "signal_dependencies": ["FUEL_RAIL_PRESSURE_ACTUAL", "LPSYS_PSET", "BATTERY_VOLTAGE"],
    }
