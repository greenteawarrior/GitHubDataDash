from __future__ import unicode_literals
import sqlite3

class DBWrapper(object):

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_comments_table(self):
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE comments 
            (
            link TEXT PRIMARY KEY,
            person TEXT,
            time TEXT,
            body TEXT,
            repo_owner TEXT,
            repo_name TEXT,
            pr_number INT,
            pr_updated_at TEXT
            )"""
        )
        self.conn.commit()

    def upsert_comment(self, link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at):
        c = self.conn.cursor()
        c.execute("""INSERT OR IGNORE INTO comments
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at))
        c.execute("""UPDATE comments SET
            link=?,
            person=?,
            time=?,
            body=?,
            repo_owner=?,
            repo_name=?,
            pr_number=?,
            pr_updated_at=?
            WHERE link=? """,
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at, link))
        self.conn.commit()