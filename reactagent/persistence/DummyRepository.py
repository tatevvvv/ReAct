from typing import Dict, Any

from reactagent.persistence.abstractions import Repository

class DummyRepository(Repository):
    def __init__(self, configuration):
        pass

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        doc  = {"prompt": "", "conversation":"", "summaries":""}
        return doc

    def upsert_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        pass