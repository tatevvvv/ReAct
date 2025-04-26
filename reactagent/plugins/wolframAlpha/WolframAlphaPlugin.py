from typing import List
from reactagent.intelligence.abstractions import ReActPlugin


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