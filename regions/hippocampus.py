import sqlite3, json, time, uuid

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
        c.execute("INSERT INTO episodes VALUES (?,?,?,?,?,?,?,?)", (
            ep_id, time.time(),
            json.dumps([i.content for i in workspace.spotlight], ensure_ascii=False),
            workspace.goal, action, result, valence, salience,
        ))
        self.conn.commit()
        return ep_id

    def recall(self, cue, limit=5):
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM episodes WHERE focus LIKE ? OR goal LIKE ? ORDER BY ts DESC LIMIT ?",
            (f"%{cue}%", f"%{cue}%", limit),
        )
        return c.fetchall()

    def replay(self, n=10):
        c = self.conn.cursor()
        c.execute("SELECT * FROM episodes ORDER BY ts DESC LIMIT ?", (n,))
        return c.fetchall()