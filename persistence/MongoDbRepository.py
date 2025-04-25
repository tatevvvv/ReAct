from typing import Dict, Any
from pymongo import MongoClient

from persistence.abstractions import Repository

class MongoDbRepository(Repository):
    def __init__(self, configuration):
        self.client = MongoClient(configuration['mongodb']['uri'])
        self.col = self.client[configuration['mongodb']['db']][configuration['mongodb']['collection']]

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        doc = self.col.find_one({"_id": session_id})
        if doc is not None:
            return {
                "summaries": doc.get("summaries", ""),
                "conversation": doc.get("conversation", "")
            }
        return doc

    def upsert_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        self.col.update_one(
            {"_id": session_id},
            {"$set": {
                "summaries": data.get("summaries", ""),
                "conversation": data.get("conversation", "")
            }},
            upsert=True
        )