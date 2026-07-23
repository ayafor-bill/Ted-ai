"""
    OllamaLLm CLient - Handles communication with the local Ollama instace
"""

import json
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Thin client for calling Ollama's local API"""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "qwen3.5:9b"):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        
    def generate(self, prompt: str, temperature: float = 0.3, timeout: int= 120) -> str:
        """
        Send a prompt to Ollama and return the raw text response.
        temperature is kept low (0.3) to reduce generic/rambling output.
        """
        
        url = f"{self.endpoint}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot reach Ollama at {self.endpoint}. Is 'ollama serve' running"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Ollama request timed out after {timeout}s")
        except Exception as e:
            logger.error(f"Ollama generate error: {str(e)}")
            raise