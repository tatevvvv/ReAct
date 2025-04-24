from typing import List
from intelligence.abstractions import LLMModel
from google import genai
from google.genai import types

class GeminiModel(LLMModel):
    def __init__(self, name, api_key):
        super().__init__(name, api_key)
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, stop:List) -> str:
        cfg = types.GenerateContentConfig(
            stop_sequences=stop,
            max_output_tokens=100,
            temperature=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            top_p=1
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
            config=cfg,
        )
        return response.text
