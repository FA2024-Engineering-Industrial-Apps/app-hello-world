from .llm import LLM
import requests
from requests.auth import HTTPBasicAuth

class SiemensLLM(LLM):
    def __init__(self, model : str, api_key : str) -> None:
        super().__init__()
        self._url = f"https://api.siemens.com/llm/v1/completions"
        self._model = model
        self._auth = HTTPBasicAuth('apikey', api_key)
        
    def process_prompt(self, prompt: str) -> str:
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        
        ollama_response = requests.post(self._url, auth=self._auth, json=payload, stream=False)
        if ollama_response.status_code != 200:
            raise Exception()
        
        return ollama_response.json()['response']