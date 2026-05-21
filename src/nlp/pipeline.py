import json
import pandas as pd
from pathlib import Path
from typing import Dict, Union
from .extractor import ParameterExtractor
from .converter import CategoryToRangeConverter
from .bridge import BridgeBuilder

class NLPPipeline:
    def __init__(
        self,
        model_path: Union[str, Path],
        df_path: Union[str, Path],
        config_path: Union[str, Path],
        bridge_dir: Union[str, Path]
    ):
        self.model_path = Path(model_path)
        self.df_path = Path(df_path)

        # Загрузка конфигов
        with open(config_path, encoding="utf-8") as f:
            self.property_mapping = json.load(f)
            # если обёрнут в ключ, извлекаем
            if isinstance(self.property_mapping, dict) and len(self.property_mapping) == 1:
                self.property_mapping = list(self.property_mapping.values())[0]

        self.all_features = list(self.property_mapping.keys())
        self.df = pd.read_csv(df_path).dropna(subset=["smiles"])

        # Компоненты
        self.extractor = ParameterExtractor(self.model_path)
        self.converter = CategoryToRangeConverter(self.df, self.all_features)
        self.bridge = BridgeBuilder(self.converter, self.all_features, Path(bridge_dir))

    def process_request(self, text: str) -> Dict:
        extracted = self.extractor.extract(text)
        if not extracted:
            return {"success": False, "error": "No parameters found"}

        recommendations = {}
        for param, info in extracted.items():
            rec = self.converter.to_range(param, info["category"])
            recommendations[param] = {
                "category": info["category"],
                "extracted_value": info["value"],
                "recommendation": rec,
            }

        gen_input = self.bridge.build(recommendations)
        bridge_path = self.bridge.save(gen_input)

        return {
            "success": True,
            "original_request": text,
            "extracted_parameters": extracted,
            "recommendations": recommendations,
            "bridge_file": str(bridge_path),
        }