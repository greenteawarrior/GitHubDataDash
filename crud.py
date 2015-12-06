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
            pr_updated_at TEXT,
            avatar_url TEXT
            )"""
        )
        self.conn.commit()

    def upsert_comment(self, link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at, avatar_url):
        c = self.conn.cursor()
        c.execute("""INSERT OR IGNORE INTO comments
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at, avatar_url))
        c.execute("""UPDATE comments SET
            link=?,
            person=?,
            time=?,
            body=?,
            repo_owner=?,
            repo_name=?,
            pr_number=?,
            pr_updated_at=?,
            avatar_url=?
            WHERE link=? """,
            (link, person, time, body, repo_owner, repo_name, pr_number, pr_updated_at, avatar_url, link))
        self.conn.commit()

    def get_comments_for_repo(self, repo_owner, repo_name):
        c = self.conn.cursor()
        return c.execute("""SELECT * FROM comments
            WHERE repo_owner=? AND repo_name=?""",
            (repo_owner, repo_name))

    # TODO: Should test the ninja functions before pushing to GitHub

    def create_ninjas_table(self):
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE ninjas
            (
            github_handle TEXT,
            first TEXT,
            last TEXT,
            course TEXT,
            semester TEXT
            )"""
        )
        self.conn.commit()

    def insert_ninja(self, github_handle, first, last, course, semester):
        c = self.conn.cursor()
        c.execute("""INSERT OR IGNORE INTO comments
            (github_handle, first, last, course, semester)
            VALUES (?, ?, ?, ?, ?)""",
            (github_handle, first, last, course, semester))
        self.conn.commit()

