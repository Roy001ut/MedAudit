from anthropic import Anthropic
from app.config import settings
import json
from typing import Dict, Any

client = Anthropic()

class BillService:
    @staticmethod
    def analyze_bill(bill_text: str, diagnosis: str = None) -> Dict[str, Any]:
        text_preview = bill_text[:2000]
        prompt = f"""Analyze hospital bill. {diagnosis or ""} Return JSON with: charges (array), red_flags (array), fraud_risk_score (0-100 int)"""

        try:
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": f"{prompt}\n\nBill:\n{text_preview}"}]
            )

            text = message.content[0].text
            start = text.find('{')
            end = text.rfind('}') + 1

            if start >= 0 and end > start:
                return json.loads(text[start:end])
            return {"raw_response": text}
        except Exception as e:
            return {"error": str(e)}
