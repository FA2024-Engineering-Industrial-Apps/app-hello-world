import requests
from .llm import LLM
import json

class Ollama(LLM):
    def __init__(self, server_address : str, model : str) -> None:
        super().__init__()
        self._url = f"http://{server_address}/api/generate"
        self._model = model
        
    def process_prompt(self, prompt: str) -> str:
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        
        ollama_response = requests.post(self._url, json=payload, stream=False)
        if ollama_response.status_code != 200:
            raise Exception()
        
        return ollama_response.json()['response']