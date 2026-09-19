from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid
app=FastAPI(title="FDE Training AI Backend")
class ChatRequest(BaseModel):
    message:str
    conversationId:Optional[str]=None
class ChatResponse(BaseModel):
    requestId:str
    answer:str
    model:str
@app.get("/api/ai/health")
async def health(): return {"status":"healthy","service":"ai-backend","model":"simulated-ai-model"}
@app.post("/api/ai/chat")
async def chat(request:ChatRequest): return ChatResponse(requestId=str(uuid.uuid4()),answer=f"AI analysis received for message: {request.message}",model="simulated-ai-model")
@app.get("/api/incidents")
async def incidents(): return {"incidents":[{"id":"INC-1001","title":"Customer 360 pipeline failure","description":"Silver transformation failed because customer_segment was missing.","status":"Investigating"},{"id":"INC-1002","title":"Retail ingestion delay","description":"Source file arrival was delayed beyond the ingestion SLA.","status":"Open"}]}
