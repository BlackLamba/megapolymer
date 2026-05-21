from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.nlp.pipeline import NLPPipeline
from pathlib import Path

app = FastAPI()

# Инициализация пайплайна (пути настройте под ваш сервер)
pipeline = NLPPipeline(
    model_path="models/nlp_model_fast",
    df_path="data/raw/polyOne_aa.csv",
    config_path="data/configs/property_mapping.json",
    bridge_dir="data/configs/bridges"
)

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    success: bool
    original_request: str = None
    extracted_parameters: dict = None
    recommendations: dict = None
    bridge_file: str = None
    error: str = None

@app.post("/extract", response_model=QueryResponse)
async def extract_properties(request: QueryRequest):
    result = pipeline.process_request(request.text)
    if not result["success"]:
        raise HTTPException(status_code=422, detail=result["error"])
    return result