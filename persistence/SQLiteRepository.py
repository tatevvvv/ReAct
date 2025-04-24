import sqlite3
from typing import Dict, Any

from persistence.abstractions import Repository


class SQLLiteRepository(Repository):
    def __init__(self, db_path: str = "sessions.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            chat_name TEXT,
            summary   TEXT
        )""")
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            session_id TEXT,
            turn_index INTEGER,
            role       TEXT,
            content    TEXT,
            PRIMARY KEY(session_id, turn_index)
        )""")
        self.conn.commit()

    def load_session(self, session_id: str) -> Dict[str, Any]:
        cur = self.conn.execute(
            "SELECT chat_name, summary FROM sessions WHERE session_id = ?", (session_id,)
        )
        row = cur.fetchone()
        data: Dict[str, Any] = {"messages": [], "summary": ""}
        if row:
            data["chat_name"], data["summary"] = row
        cur2 = self.conn.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY turn_index", (session_id,)
        )
        for r in cur2.fetchall():
            data["messages"].append({"role": r[0], "content": r[1]})
        return data

    def save_session(self, session_id: str, data: Dict[str, Any]) -> None:
        self.conn.execute(
            "REPLACE INTO sessions(session_id, chat_name, summary) VALUES (?,?,?)",
            (session_id, data.get("chat_name", ""), data.get("summary", ""))
        )
        self.conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        for idx, msg in enumerate(data.get("messages", [])):
            self.conn.execute(
                "INSERT INTO messages(session_id, turn_index, role, content) VALUES (?,?,?,?)",
                (session_id, idx, msg["role"], msg["content"])
            )
        self.conn.commit()