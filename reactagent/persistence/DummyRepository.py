from typing import Dict, Any

from reactagent.persistence.abstractions import Repository

class DummyRepository(Repository):
    def __init__(self):
        pass

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        return None

    def upsert_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        pass