import os
import json
import requests

class LLMConnector:
    """Base class for LLM connectors."""
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model

    def generate_request(self, prompt: str, sandbox_mode: bool = False, batch_mode: bool = False) -> dict:
        raise NotImplementedError("Subclasses must implement generate_request")

class MockConnector(LLMConnector):
    """A logic-free connector for testing the architecture."""
    def __init__(self, model="mock-v1"):
        super().__init__("mock", model)

    def generate_request(self, prompt: str, sandbox_mode: bool = False, batch_mode: bool = False) -> any:
        print(f"[LLM] Using MockConnector ({self.model}) (Sandbox: {sandbox_mode}, Batch: {batch_mode})...")
        p = prompt.lower()
        
        if batch_mode:
            # Return a deterministic 3-item batch
            return [
                {
                    "asset": {"name": "mock_batch_1", "primitive": "cube"},
                    "options": {"tags": ["mock_batch"]}
                },
                {
                    "asset": {"name": "mock_batch_2", "primitive": "sphere", "scale": [0.5, 0.5, 0.5]},
                    "options": {"shading": "smooth"}
                },
                {
                    "asset": {"name": "mock_batch_3", "primitive": "cylinder"},
                    "options": {"bevel": 0.1}
                }
            ]

        # Single mode logic
        primitive = "cube"
        if "sphere" in p: primitive = "sphere"
        elif "cylinder" in p: primitive = "cylinder"
        elif "plane" in p: primitive = "plane"
        
        response = {
            "asset": {
                "name": "mock_interpreted_asset",
                "primitive": primitive,
                "scale": [1.0, 1.0, 1.0]
            },
            "options": {
                "shading": "smooth" if "smooth" in p else "flat",
                "tags": ["llm_mock", "sandbox" if sandbox_mode else "skeleton"]
            }
        }

        if sandbox_mode:
            response["options"]["python_code"] = "bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0.5, 0.5, 0.5))"

        return response

class OpenAIConnector(LLMConnector):
    """Connector for OpenAI Chat Completion API."""
    def __init__(self, model=None):
        final_model = model or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
        super().__init__("openai", final_model)
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate_request(self, prompt: str, sandbox_mode: bool = False, batch_mode: bool = False) -> any:
        print(f"[LLM] Querying OpenAI ({self.model})...")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
        item_schema = (
            "{ 'asset': { 'name': str, 'primitive': str, 'scale': [x,y,z] }, "
            "  'options': { 'shading': 'flat'|'smooth', 'author': str, 'tags': [str, ...]"
        )
        if sandbox_mode:
            item_schema += ", 'python_code': str } }"
        else:
            item_schema += " } }"

        if batch_mode:
            schema_instruction = f"Return a JSON LIST of objects, each matching this schema: {item_schema}"
        else:
            schema_instruction = f"Return a single JSON object matching this schema: {item_schema}"

        system_prompt = (
            "You are an assistant for the MStorm Asset Forge. "
            "Translate the user's natural language request into valid JSON. "
            "You MUST return ONLY the JSON. No explanation, no markdown blocks. "
            f"{schema_instruction}"
        )

        if sandbox_mode:
            system_prompt += (
                "\n\nEXPERIMENTAL MODE: You may provide a tightly-scoped Blender Python (bpy) snippet in 'options.python_code' "
                "to create the requested geometry. ONLY use bpy.ops.mesh operators. "
                "DO NOT use imports, filesystem access, or external libraries."
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
            data = json.loads(content)
            # If batch mode, the model might return {"requests": [...]} or just the list
            if batch_mode and isinstance(data, dict) and "requests" in data:
                return data["requests"]
            return data
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed: {e}")

class GeminiConnector(LLMConnector):
    """Connector for Google Gemini API (REST)."""
    def __init__(self, model=None):
        final_model = model or os.environ.get("GEMINI_MODEL") or "gemini-1.5-flash"
        super().__init__("gemini", final_model)
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def generate_request(self, prompt: str, sandbox_mode: bool = False, batch_mode: bool = False) -> any:
        print(f"[LLM] Querying Gemini ({self.model})...")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        item_schema = (
            "{ 'asset': { 'name': str, 'primitive': str, 'scale': [x,y,z] }, "
            "  'options': { 'shading': 'flat'|'smooth', 'author': str, 'tags': [str, ...]"
        )
        if sandbox_mode:
            item_schema += ", 'python_code': str } }"
        else:
            item_schema += " } }"

        if batch_mode:
            schema_instruction = f"Return a JSON LIST of objects, each matching this schema: {item_schema}"
        else:
            schema_instruction = f"Return a single JSON object matching this schema: {item_schema}"

        system_prompt = (
            "You are an assistant for the MStorm Asset Forge. "
            "Translate the user's natural language request into valid JSON. "
            "You MUST return ONLY the JSON. No explanation, no markdown blocks. "
            f"{schema_instruction}"
        )

        if sandbox_mode:
            system_prompt += (
                "\n\nEXPERIMENTAL MODE: You may provide a tightly-scoped Blender Python (bpy) snippet in 'options.python_code' "
                "to create the requested geometry. ONLY use bpy.ops.mesh operators. "
                "DO NOT use imports, filesystem access, or external libraries."
            )

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"parts": [{"text": f"{system_prompt}\n\nUser Prompt: {prompt}"}]}
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
            }
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(content)
            # Normalize list vs dict with list
            if batch_mode and isinstance(parsed, dict) and "requests" in parsed:
                return parsed["requests"]
            return parsed
        except Exception as e:
            raise RuntimeError(f"Gemini API request failed: {e}")

def get_connector(provider: str, model: str = None) -> LLMConnector:
    """Factory function to get the appropriate connector."""
    p = provider.lower()
    if p == "openai":
        return OpenAIConnector(model=model)
    elif p == "gemini":
        return GeminiConnector(model=model)
    elif p == "mock":
        return MockConnector(model=model or "mock-v1")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
