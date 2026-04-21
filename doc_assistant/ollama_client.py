import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="gemma4:e4b"):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt, system_prompt="You are a helpful assistant."):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {prompt}",
            "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, messages):
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            return f"Error: {str(e)}"
