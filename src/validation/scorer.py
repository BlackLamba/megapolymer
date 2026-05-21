# src/validation/scorer.py
from __future__ import annotations

import math
import pandas as pd
from typing import Dict, List, Optional
from rdkit import Chem
from .property_predictor import PropertyPredictor

class PolymerScorer:
    """Оценивает степень соответствия полимеров требованиям."""

    def __init__(self, predictor: PropertyPredictor, real_db_path: Optional[Path] = None):
        self.predictor = predictor
        # Реальная база данных для штрафа – можно загрузить CSV или словарь
        self.real_props_df = None
        if real_db_path:
            self.real_props_df = pd.read_csv(real_db_path)
            self.real_props_df["Polymer_SMILES"] = self.real_props_df["Polymer_SMILES"].str.strip()

    def compute_score(self, row: pd.Series, requirements: List[Dict],
                      sigma_rel: float = 0.2) -> Dict:
        smiles = row.get("smiles", "")
        if not self._valid_smiles(smiles):
            return {"overall_score": 0.0, "details": {}, "notes": "Invalid SMILES"}

        # 1. Базовое соответствие требованиям
        scores = {}
        for req in requirements:
            param = req["param"]
            value = row.get(param)
            scores[param] = self._eval_parameter(value, req)

        # Среднее геометрическое (пользовательские все имеют вес 1)
        log_sum = 0.0
        total_weight = 0.0
        for req in requirements:
            s = max(scores[req["param"]], 1e-6)
            log_sum += math.log(s)
            total_weight += 1.0
        base_score = math.exp(log_sum / total_weight) if total_weight > 0 else 0.0

        # 2. Штраф от реальной БД
        db_penalty = self._calc_db_penalty(smiles, row, requirements)

        # 3. Реализм через LightGBM
        realism_score = self._calc_realism(smiles, row, requirements, sigma_rel)

        overall = base_score * db_penalty * realism_score
        notes = []
        if db_penalty < 1.0:
            notes.append(f"DB mismatch penalty: {db_penalty:.2f}")
        if realism_score < 0.999:
            notes.append(f"Realism: {realism_score:.4f}")
        return {
            "overall_score": overall,
            "details": scores,
            "db_penalty": db_penalty,
            "realism_score": realism_score,
            "notes": "; ".join(notes) if notes else "OK",
        }

    def evaluate_all(self, polymers_df: pd.DataFrame,
                     requirements: List[Dict]) -> pd.DataFrame:
        results = []
        for _, row in polymers_df.iterrows():
            res = self.compute_score(row, requirements)
            results.append({**row.to_dict(),
                            "score": res["overall_score"],
                            "realism_score": res["realism_score"],
                            "notes": res["notes"]})
        return pd.DataFrame(results).sort_values("score", ascending=False)

    # -----------------------------------------------------------------
    # Вспомогательные методы
    # -----------------------------------------------------------------
    @staticmethod
    def _valid_smiles(smiles: str) -> bool:
        return bool(smiles) and Chem.MolFromSmiles(smiles) is not None

    @staticmethod
    def _eval_parameter(value: Optional[float], req: Dict) -> float:
        if value is None or math.isnan(value):
            return 0.1 if req["is_user"] else 0.5
        L, U, sigma = req["L"], req["U"], req["sigma"]
        if L <= value <= U:
            return 1.0
        dist = L - value if value < L else value - U
        return math.exp(-0.5 * (dist / sigma) ** 2)

    def _calc_db_penalty(self, smiles: str, row: pd.Series,
                         requirements: List[Dict]) -> float:
        if self.real_props_df is None:
            return 1.0
        match = self.real_props_df[self.real_props_df["Polymer_SMILES"] == smiles]
        if match.empty:
            return 1.0
        real_row = match.iloc[0]
        deviations = 0
        for req in requirements:
            param = req["param"]
            if param not in real_row or param not in row:
                continue
            stated, actual = row[param], real_row[param]
            if pd.isna(stated) or pd.isna(actual):
                continue
            rel_diff = abs(stated - actual) / abs(actual) if actual != 0 else abs(stated - actual)
            if rel_diff > 0.20:
                deviations += 1
        return max(0.5, 1.0 - 0.05 * deviations)

    def _calc_realism(self, smiles: str, row: pd.Series,
                      requirements: List[Dict], sigma_rel: float) -> float:
        pred_props = self.predictor.predict(smiles)
        if not pred_props:
            return 1.0
        factors = []
        for req in requirements:
            param = req["param"]
            if param not in pred_props or param not in row:
                continue
            stated, predicted = row[param], pred_props[param]
            if pd.isna(stated) or predicted == 0:
                continue
            rel_err = abs(stated - predicted) / abs(predicted)
            factor = math.exp(-0.5 * (rel_err / sigma_rel) ** 2)
            factors.append(max(factor, 1e-12))
        if not factors:
            return 1.0
        log_prod = sum(math.log(f) for f in factors)
        return math.exp(log_prod / len(factors))