import pandas as pd
from typing import Dict, Optional

class CategoryToRangeConverter:
    def __init__(self, df: pd.DataFrame, features: list):
        self.thresholds = self._compute_thresholds(df, features)

    def _compute_thresholds(self, df, features):
        th = {}
        for col in features:
            if col not in df.columns:
                continue
            s = df[col].dropna()
            if len(s) < 10:
                continue
            th[col] = {
                "low": float(s.quantile(0.33)),
                "high": float(s.quantile(0.67)),
                "min": float(s.min()),
                "max": float(s.max()),
            }
        return th

    def to_range(self, param: str, category: str) -> Optional[Dict]:
        if param not in self.thresholds:
            return None
        t = self.thresholds[param]
        if category == "low":
            lo, hi = t["min"], t["low"]
        elif category == "high":
            lo, hi = t["high"], t["max"]
        else:
            lo, hi = t["low"], t["high"]
        target = (lo + hi) / 2
        return {"min": lo, "max": hi, "target_value": target}