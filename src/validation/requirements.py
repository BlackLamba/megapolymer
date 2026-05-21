# src/validation/requirements.py
from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional

class RequirementsLoader:
    """Загружает и ужесточает требования из моста NLP→Gen."""

    def __init__(self, thresholds_path: Path):
        # Загружаем пороги (THRESHOLDS) из сохранённого файла
        with open(thresholds_path, 'rb') as f:
            self.thresholds = pickle.load(f)["thresholds"]

    def load_from_bridge(self, bridge_path: Path) -> List[Dict]:
        """Читает bridge JSON и возвращает список ужесточённых требований."""
        with open(bridge_path, encoding='utf-8') as f:
            bridge = json.load(f)

        # Поддерживаем формат: {"requirements": {param: {"target_value": ...}}}
        if "requirements" not in bridge:
            raise ValueError("Bridge file must contain 'requirements' key")
        req_dict = bridge["requirements"]

        reqs = []
        for param, info in req_dict.items():
            target = info["target_value"]
            prepared = self._prepare_requirement(param, target, is_user=True)
            if prepared:
                reqs.append(prepared)
        return reqs

    def _prepare_requirement(self, param: str, target: float,
                             is_user: bool) -> Optional[Dict]:
        t = self.thresholds.get(param)
        if t is None:
            # Если нет порогов, используем узкий коридор вокруг target
            L, U = target * 0.95, target * 1.05
            sigma = (U - L) * 0.2 if U > L else 0.1
        else:
            full_range = t["max"] - t["min"]
            if is_user:
                L = target - 0.02 * full_range
                U = target + 0.02 * full_range
                sigma = 0.02 * full_range
            else:
                L = target - 0.10 * full_range
                U = target + 0.10 * full_range
                sigma = 0.05 * full_range
            L = max(L, t["min"])
            U = min(U, t["max"])
        if L > U:
            return None
        return {
            "param": param,
            "target": target,
            "L": L,
            "U": U,
            "sigma": sigma,
            "is_user": is_user,
        }