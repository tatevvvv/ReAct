import json
from typing import Dict
from .core.ReActMainAgent import ReActMainAgent
from .helper import Helper

class Agent:
    def __init__(self, session_id, settings_path: str):
        settings_path
        with open(settings_path) as f:
            self.cfg: Dict = json.load(f)
        llm, plugins, ltm = Helper.resolve_dependencies(self.cfg)
        self.agent = ReActMainAgent(session_id, llm, plugins, ltm)


    def start(self, user_input, transparency=True):
        answer, info = self.agent.ask(user_input, transparency=transparency)
        return info

    def flush(self):
        self.agent.flush()