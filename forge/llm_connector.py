import os
import json
import requests

class LLMConnector:
    """Base class for LLM connectors."""
    def generate_request(self, prompt: str) -> dict:
        raise NotImplementedError("Subclasses must implement generate_request")

class MockConnector(LLMConnector):
    """A logic-free connector for testing the architecture."""
    def generate_request(self, prompt: str) -> dict:
        print("[LLM] Using MockConnector...")
        p = prompt.lower()
        primitive = "cube"
        if "sphere" in p: primitive = "sphere"
        elif "cylinder" in p: primitive = "cylinder"
        elif "plane" in p: primitive = "plane"
        
        return {
            "asset": {
                "name": "mock_interpreted_asset",
                "primitive": primitive,
                "scale": [1.0, 1.0, 1.0]
            },
            "options": {
                "shading": "smooth" if "smooth" in p else "flat",
                "tags": ["llm_mock", "skeleton"]
            }
        }

class OpenAIConnector(LLMConnector):
    """Connector for OpenAI Chat Completion API."""
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate_request(self, prompt: str) -> dict:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        print(f"[LLM] Querying OpenAI ({self.model})...")
        
        system_prompt = (
            "You are an assistant for the MStorm Asset Forge. "
            "Translate the user's natural language request into a valid JSON object. "
            "You MUST return ONLY the JSON object. No explanation, no markdown blocks. "
            "The JSON must strictly follow this schema: "
            "{ 'asset': { 'name': str, 'primitive': 'cube'|'sphere'|'cylinder'|'plane', 'scale': [x,y,z] }, "
            "  'options': { 'shading': 'flat'|'smooth', 'author': str, 'tags': [str, ...] } }"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed: {e}")

def get_connector(provider: str, model: str = None) -> LLMConnector:
    """Factory function to get the appropriate connector."""
    if provider == "openai":
        return OpenAIConnector(model=model or "gpt-4o-mini")
    elif provider == "mock":
        return MockConnector()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
