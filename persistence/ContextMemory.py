from typing import Dict, Any
from persistence.abstractions import Repository, ShortTermMemory


class ContextMemory:
    def __init__(self, session_id, repository: Repository):
        self.repository = repository
        self.session_id = session_id
        self.context: Dict[str, str] = {"prompt": "", "conversation":"", "summaries":""}
        self.load_session()
    def load_session(self) -> Dict[str, Any]:
        session_data = self.repository.get_session_data(self.session_id)
        if session_data is not None:
            self.context = session_data

    def add_prompt(self, prompt):
        self.context["prompt"] = prompt

    def upsert_conversation(self, question: str, answer: str) -> None:
        self.context['conversation']+= f"role: user, content: {question}"
        self.context['conversation']+= "\n"
        self.context['conversation']+= f"role: assistant, content: {answer}"

    def upsert_summary(self, summary) -> None:
        self.context['summaries'] += summary
        self.context['summaries'] += "\n"

    def flush(self) -> None:
        data = {"prompt": {self.context['prompt']}, "conversation": self.context['conversation'], "summaries": self.context['summaries']}
        self.repository.upsert_session_data(self.session_id, data)

