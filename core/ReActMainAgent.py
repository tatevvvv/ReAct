import atexit

from core.ReActReasoner import ReActReasoner
from persistence.ContextMemory import ContextMemory
from persistence.abstractions import Repository

class ReActMainAgent:
    def __init__(self, session_id, llm, plugins, ltm: Repository):
        self.session_id = session_id
        self.memory = ContextMemory(self.session_id, ltm)

        reasoner = ReActReasoner(llm=llm, plugins=plugins, memory=self.memory)
        self.reasoner = reasoner

    def ask(self, question: str, transparency: bool = True) -> str:
        answer, trace = self.reasoner.run(question)
        if transparency:
            print("--- Trace ---")
            for step in trace:
                print(step)
        return answer, trace

    def flush(self):
        self.memory.flush()