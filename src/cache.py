import sqlite3


class Cache:

    DB_NAME = "cache.db"

    @staticmethod
    def initialize():

        connection = sqlite3.connect(Cache.DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache(
                question TEXT PRIMARY KEY,
                answer TEXT
            )
        """)

        connection.commit()
        connection.close()

    @staticmethod
    def get(question):

        connection = sqlite3.connect(Cache.DB_NAME)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT answer FROM cache WHERE question=?",
            (question,)
        )

        result = cursor.fetchone()

        connection.close()

        if result:
            return result[0]

        return None

    @staticmethod
    def save(question, answer):

        connection = sqlite3.connect(Cache.DB_NAME)

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO cache(question, answer)
            VALUES (?, ?)
            """,
            (question, answer)
        )

        connection.commit()
        connection.close()