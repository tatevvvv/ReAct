from abc import ABC, abstractmethod
from typing import List

class LLMModel(ABC):
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
    @abstractmethod
    def generate(self, prompt: str, stop: List) -> str:
        pass

class ReActPlugin(ABC):
    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def action_names(self) -> List[str]:
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def prompt_header(self) -> str:
        pass
