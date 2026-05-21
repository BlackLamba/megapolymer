# src/validation/pipeline.py
from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from typing import Optional, List

from .property_predictor import PropertyPredictor
from .requirements import RequirementsLoader
from .scorer import PolymerScorer

class ValidationPipeline:
    """Валидация сгенерированных полимеров и создание отчётов."""

    def __init__(
        self,
        lgbm_model_path: Path,
        thresholds_path: Path,
        real_db_path: Optional[Path] = None,
        output_dir: Path = Path("bridges")
    ):
        self.predictor = PropertyPredictor(lgbm_model_path)
        self.req_loader = RequirementsLoader(thresholds_path)
        self.scorer = PolymerScorer(self.predictor, real_db_path)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, polymers_csv_path: Path, bridge_path: Path) -> Path:
        """
        Загружает полимеры и мост, вычисляет оценки, сохраняет отчёты.
        Возвращает путь к папке с результатами.
        """
        # 1. Загрузить требования
        requirements = self.req_loader.load_from_bridge(bridge_path)
        if not requirements:
            raise ValueError("No requirements found in bridge file")

        # 2. Загрузить полимеры
        df = pd.read_csv(polymers_csv_path)
        # Универсальный поиск колонки со SMILES
        smiles_col = next((c for c in ["smiles", "Polymer_SMILES", "SELFIES"] if c in df.columns), None)
        if smiles_col is None:
            raise KeyError("CSV must contain a SMILES column (smiles, Polymer_SMILES or SELFIES)")
        df.rename(columns={smiles_col: "smiles"}, inplace=True)
        # Оставляем только нужные параметры и smiles
        param_cols = []
        for req in requirements:
            param = req["param"]
            if param in df.columns:
                param_cols.append(param)
            elif f"{param}_target" in df.columns:
                df.rename(columns={f"{param}_target": param}, inplace=True)
                param_cols.append(param)
        df = df[["smiles"] + param_cols]

        # 3. Оценка
        evaluated = self.scorer.evaluate_all(df, requirements)

        # 4. Сохранение отчётов
        top10 = evaluated.head(10)
        evaluated.to_csv(self.output_dir / "validation_full_results.csv", index=False)
        top10.to_csv(self.output_dir / "validation_top.csv", index=False)

        # Текстовый отчёт
        with open(self.output_dir / "summary.txt", "w", encoding="utf-8") as f:
            f.write(f"Оценено {len(evaluated)} полимеров\n")
            f.write(f"Топ-10:\n")
            for i, (_, row) in enumerate(top10.iterrows(), 1):
                f.write(f"{i}. {row['smiles']} – Score: {row['score']:.4f} ({row['notes']})\n")

        return self.output_dir