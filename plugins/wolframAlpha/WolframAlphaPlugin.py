import json
from typing import List
import os
from intelligence.abstractions import ReActPlugin


class WolframAlphaPlugin(ReActPlugin):
    @property
    def action_names(self) -> List[str]:
        pass

    def step(self, action):
        pass

    def prompt_header(self) -> str:
        pass

    def __init__(self, env):
        super().__init__("WolframAlpha")
        self.env = env