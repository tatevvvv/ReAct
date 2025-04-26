from reactagent.core.ReActReasoner import ReActReasoner
from reactagent.persistence.ContextMemory import ContextMemory
from reactagent.persistence.abstractions import Repository

class ReActMainAgent:
    def __init__(self, session_id, llm, plugins, ltm: Repository):
        self.session_id = session_id
        self.memory = ContextMemory(self.session_id, ltm)

        reasoner = ReActReasoner(llm=llm, plugins=plugins, memory=self.memory)
        self.reasoner = reasoner

    def ask(self, question: str, transparency=True) -> str:
        answer, info = self.reasoner.run(question, transparency=transparency)
        return answer, info

    def flush(self):
        self.memory.flush()