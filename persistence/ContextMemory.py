from typing import Dict, Any
from persistence.abstractions import Repository, ShortTermMemory


class ContextMemory:
    def __init__(self, session_id, prompt,  repository: Repository):
        self.repository = repository
        self.session_id = session_id
        self.context: Dict[str, str] = {"prompt": "", "conversation":"", "summaries":""}

    def load_session(self) -> Dict[str, Any]:
        session_data = self.repository.get_session_data(self.session_id)
        if session_data:
            self.context = session_data

    def add_prompt(self, prompt):
        self.context["prompt"] = prompt

    def upsert_conversation(self, question: str, answer: str) -> None:
        self.context['conversation'].append({"role": "user", "content": question})
        self.context['conversation'].append({"role": "assistant", "content": answer})

    def upsert_summary(self, summary) -> None:
        self.context['summary'].append(summary)

    def flush(self) -> None:
        data = {"conversation": self.stm.conversation, "summary": self.stm.summary}
        self.repository.upsert_session_data(self.session_id, data)


