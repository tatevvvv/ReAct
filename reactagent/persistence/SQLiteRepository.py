import sqlite3
from typing import Dict, Any
from reactagent.persistence.abstractions import Repository


class SQLiteRepository(Repository):
    def __init__(self, configuration: Dict[str, Any]):
        db_path = configuration['sqllite']['path']
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self) -> None:
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            _id          TEXT PRIMARY KEY,
            summaries    TEXT,
            conversation TEXT
        )
        """)
        self.conn.commit()

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        cur = self.conn.execute(
            "SELECT summaries, conversation FROM sessions WHERE _id = ?",
            (session_id,)
        )
        row = cur.fetchone()
        if row:
            return {
                "summaries":    row[0] or "",
                "conversation": row[1] or ""
            }
        return {}

    def upsert_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        summaries    = data.get("summaries", "")
        conversation = data.get("conversation", "")
        self.conn.execute("""
            INSERT INTO sessions(_id, summaries, conversation)
            VALUES (?, ?, ?)
            ON CONFLICT(_id) DO UPDATE SET
              summaries    = excluded.summaries,
              conversation = excluded.conversation
        """, (session_id, summaries, conversation))
        self.conn.commit()
