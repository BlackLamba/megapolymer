from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Добавляем корень проекта в PYTHONPATH (при необходимости)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.nlp.pipeline import NLPPipeline
from src.validation.pipeline import ValidationPipeline

# ---------------------------------------------------------------------
# Конфигурация
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Polyforge-AI

NLP_CONFIG = {
    "model_path":       BASE_DIR / "models" / "nlp_model_fast",
    "df_path":          BASE_DIR / "data" / "raw" / "polyOne_aa.csv",
    "config_path":      BASE_DIR / "data" / "configs" / "property_mapping.json",
    "bridge_dir":       BASE_DIR / "data" / "configs" / "bridges",
}

VALIDATION_CONFIG = {
    "lgbm_model_path":  BASE_DIR / "models" / "fingerprint_property_model.pkl",
    "thresholds_path":  BASE_DIR / "models" / "nlp_model_bert" / "artifacts.pkl",
    "real_db_path":     BASE_DIR / "data" / "raw" / "polymers_with_names_predicted_selfies.csv",
    "output_dir":       BASE_DIR / "data" / "configs" / "bridges",
}

# ---------------------------------------------------------------------
# Инициализация пайплайнов
# ---------------------------------------------------------------------
nlp_pipeline = NLPPipeline(**NLP_CONFIG)
validation_pipeline = ValidationPipeline(**VALIDATION_CONFIG)

# ---------------------------------------------------------------------
# Pydantic-схемы
# ---------------------------------------------------------------------
class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    success: bool
    original_request: Optional[str] = None
    extracted_parameters: Optional[dict] = None
    recommendations: Optional[dict] = None
    bridge_file: Optional[str] = None
    error: Optional[str] = None

class ValidateRequest(BaseModel):
    polymers_csv: str    # путь к gen_to_val_bridge.csv
    bridge_json: str     # путь к nlp_to_gen_bridge.json

class ValidateResponse(BaseModel):
    top10: list          # первые 10 полимеров с оценками
    result_dir: str      # папка, куда сохранены отчёты

# ---------------------------------------------------------------------
# FastAPI-приложение
# ---------------------------------------------------------------------
app = FastAPI(title="Polyforge AI API", version="1.0")

@app.post("/extract", response_model=QueryResponse)
async def extract_properties(request: QueryRequest):
    """Извлекает параметры полимера из запроса пользователя."""
    result = nlp_pipeline.process_request(request.text)
    if not result["success"]:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

@app.post("/validate", response_model=ValidateResponse)
async def validate_polymers(request: ValidateRequest):
    """
    Оценивает сгенерированные полимеры.
    Ожидает пути к CSV с полимерами и JSON моста NLP->Gen.
    """
    try:
        polymers_path = Path(request.polymers_csv)
        bridge_path   = Path(request.bridge_json)
        if not polymers_path.exists():
            raise HTTPException(status_code=400, detail="Polymers CSV not found")
        if not bridge_path.exists():
            raise HTTPException(status_code=400, detail="Bridge JSON not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file paths")

    result_dir = validation_pipeline.evaluate(polymers_path, bridge_path)

    # Читаем топ-10 из сохранённого файла
    import pandas as pd
    top10_df = pd.read_csv(result_dir / "validation_top.csv")
    top10 = top10_df.to_dict(orient="records")

    return ValidateResponse(
        top10=top10,
        result_dir=str(result_dir)
    )