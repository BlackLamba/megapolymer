import json
import random
from pathlib import Path
from typing import Dict
from converter import CategoryToRangeConverter

class BridgeBuilder:
    def __init__(self, converter: CategoryToRangeConverter, all_features: list, output_dir: Path):
        self.converter = converter
        self.all_features = all_features
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, extracted_params: Dict[str, Dict]) -> Dict:
        """Формирует словарь параметров с target_value для генератора."""
        gen_input = {}
        # Пользовательские параметры
        for param, info in extracted_params.items():
            rec = self.converter.to_range(param, info["category"])
            if rec:
                gen_input[param] = {"target_value": rec["target_value"]}
        # Автозаполнение пропущенных средними значениями
        for param in self.all_features:
            if param in gen_input:
                continue
            t = self.converter.thresholds.get(param)
            if t:
                gen_input[param] = {"target_value": round(random.uniform(t["low"], t["high"]), 4)}
            else:
                gen_input[param] = {"target_value": 0.5}  # fallback
        return gen_input

    def save(self, gen_input: Dict) -> Path:
        path = self.output_dir / "nlp_to_gen_bridge.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"requirements": gen_input}, f, ensure_ascii=False, indent=2)
        return path