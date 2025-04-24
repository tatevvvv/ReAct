from typing import Dict, Any
from pymongo import MongoClient

from persistence.abstractions import Repository

class MongoDbRepository(Repository):
    def __init__(self, configuration):
        self.client = MongoClient(configuration['mongodb']['uri'])
        self.col = self.client[configuration['mongodb']['db']][configuration['mongodb']['collection']]

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        doc = self.col.find_one({"session_id": session_id}) or None
        return {
            "summary": doc.get("summary", ""),
            "conversation": doc.get("conversation", "")
        }

    def upsert_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        self.col.update_one(
            {"session_id": session_id},
            {"$set": {
                "summary": data.get("summary", ""),
                "conversation": data.get("conversation", "")
            }},
            upsert=True
        )