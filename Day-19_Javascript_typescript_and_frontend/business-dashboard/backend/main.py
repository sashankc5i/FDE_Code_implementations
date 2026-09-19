from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Business Dashboard API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/kpis")
async def get_kpis():
    return {
        "period": "September 2026",
        "revenue": 1240000,
        "customers": 12480,
        "orders": 4821,
        "conversionRate": 8.4
    }


@app.get("/api/customers")
async def get_customers():
    return {
        "customers": [
            {
                "id": "CUS-1001",
                "name": "Acme Corp",
                "segment": "Enterprise",
                "revenue": 120000
            },
            {
                "id": "CUS-1002",
                "name": "Globex",
                "segment": "SMB",
                "revenue": 85000
            },
            {
                "id": "CUS-1003",
                "name": "Initech",
                "segment": "Enterprise",
                "revenue": 150000
            }
        ]
    }


@app.get("/api/orders")
async def get_orders():
    return {
        "orders": [
            {
                "id": "ORD-1001",
                "customer": "Acme Corp",
                "revenue": 12000,
                "status": "Completed"
            },
            {
                "id": "ORD-1002",
                "customer": "Globex",
                "revenue": 8500,
                "status": "Pending"
            },
            {
                "id": "ORD-1003",
                "customer": "Initech",
                "revenue": 15000,
                "status": "Completed"
            }
        ]
    }


@app.get("/api/segments")
async def get_segments():
    return {
        "segments": [
            {
                "name": "Enterprise",
                "customers": 4200,
                "revenue": 720000
            },
            {
                "name": "SMB",
                "customers": 8280,
                "revenue": 520000
            }
        ]
    }
from pydantic import BaseModel
from typing import Optional
import uuid


class ChatRequest(BaseModel):
    message: str
    conversationId: Optional[str] = None


class ChatResponse(BaseModel):
    requestId: str
    answer: str
    model: str


class AnalyzeRequest(BaseModel):
    text: str
    analysisType: str


class AnalyzeResponse(BaseModel):
    requestId: str
    analysisType: str
    result: str
    confidence: float


@app.get("/api/ai/health")
async def ai_health():
    return {
        "status": "healthy",
        "service": "ai-backend",
        "model": "simulated-ai-model"
    }


@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):

    return ChatResponse(
        requestId=str(uuid.uuid4()),
        answer=(
            f"AI analysis received for message: "
            f"{request.message}"
        ),
        model="simulated-ai-model"
    )


@app.post("/api/ai/analyze")
async def ai_analyze(request: AnalyzeRequest):

    return AnalyzeResponse(
        requestId=str(uuid.uuid4()),
        analysisType=request.analysisType,
        result=(
            f"Analysis completed for: "
            f"{request.text}"
        ),
        confidence=0.92
    )