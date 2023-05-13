import sqlite3


class Database:
    def __init__(self, db_file: str) -> None:
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS `channels`
        (id integer PRIMARY KEY, ad text)
        """)
        self.conn.commit()

    def get_ids(self):
        with self.conn:
            self.cur.execute("SELECT id FROM channels")
            userbase = []
            while True:
                row = self.cur.fetchone()
                if row is None:
                    break
                userbase.append(row)
            return userbase

    def ad(self, channel_id):
        with self.conn:
            return self.cur.execute("SELECT ad FROM `channels` WHERE id = ?", (channel_id,)).fetchone()[0]

    def add(self, user_id, text):
        with self.conn:
            return self.cur.execute(
                "INSERT INTO channels values (:id, :ad);",
                {'id': user_id, 'ad': text})

    def upd(self, id, ad: str):
        with self.conn:
            return self.cur.execute("UPDATE channels SET ad = ? WHERE id = ?", (ad, id,))

    def delete(self, channel_id):
        with self.conn:
            return self.cur.execute("DELETE FROM `channels` WHERE id = ?", (channel_id,))

    def delete_ad(self, channel_id):
        with self.conn:
            return self.cur.execute("UPDATE channels SET ad = ? WHERE id = ?", (None, channel_id,))
