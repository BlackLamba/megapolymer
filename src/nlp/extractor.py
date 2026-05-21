import spacy
from pathlib import Path
from typing import Dict

class ParameterExtractor:
    def __init__(self, model_path: Path):
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        self.nlp = spacy.load(model_path)

    def extract(self, text: str) -> Dict[str, Dict]:
        doc = self.nlp(text)
        params = {}
        for ent in doc.ents:
            if "_" in ent.label_:
                param, category = ent.label_.rsplit("_", 1)
                params[param] = {
                    "category": category.lower(),
                    "value": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
        return params