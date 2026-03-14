from anthropic import Anthropic
from app.config import settings
import json
from typing import Dict, Any

client = Anthropic()

class DrugService:
    @staticmethod
    def analyze_drug(drug_name: str, dosage: str) -> Dict[str, Any]:
        prompt = f"""Analyze drug: {drug_name} {dosage}. Return JSON with: what_is_it, treats (array), side_effects (array), red_flags (array)"""

        try:
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            text = message.content[0].text
            start = text.find('{')
            end = text.rfind('}') + 1

            if start >= 0 and end > start:
                return json.loads(text[start:end])
            return {"raw_response": text}
        except Exception as e:
            return {"error": str(e)}
