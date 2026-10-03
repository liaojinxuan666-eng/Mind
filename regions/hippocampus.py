import sqlite3
import json
import time
import uuid


class Hippocampus:
    def __init__(self, db_path="mind.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                ts REAL,
                focus TEXT,
                goal TEXT,
                action TEXT,
                result TEXT,
                valence REAL,
                salience REAL
            )
        """)
        self.conn.commit()

    def encode(self, workspace, action, result, valence, salience):
        c = self.conn.cursor()
        ep_id = str(uuid.uuid4())
        c.execute(
            "INSERT INTO episodes VALUES (?,?,?,?,?,?,?,?)",
            (
                ep_id,
                time.time(),
                json.dumps(
                    [i.content for i in workspace.spotlight],
                    ensure_ascii=False,
                ),
                workspace.goal,
                action,
                result,
                valence,
                salience,
            ),
        )
        self.conn.commit()
        return ep_id

    def recall(self, cue, limit=5):
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM episodes "
            "WHERE focus LIKE ? OR goal LIKE ? "
            "ORDER BY ts DESC LIMIT ?",
            (f"%{cue}%", f"%{cue}%", limit),
        )
        return c.fetchall()

    def recall_first(self, cue, threshold=0.85):
        """问过的问题，直接回忆答案。
        命中条件：cue 出现在最近情景的 focus 里。
        返回结果字符串，否则 None。
        """
        hits = self.recall(cue, limit=1)
        if not hits:
            return None
        focus_str = hits[0][2] or ""
        if cue and cue in focus_str:
            return hits[0][5]   # result
        return None

    def replay(self, n=10):
        c = self.conn.cursor()
        c.execute("SELECT * FROM episodes ORDER BY ts DESC LIMIT ?", (n,))
        return c.fetchall()