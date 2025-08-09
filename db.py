import sqlite3
from datetime import datetime

class MessageDB:
    def __init__(self, db_name="messages.db"):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self, table_name):
        """Создает таблицу с указанным именем"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                );
            """)
            conn.commit()

    def insert_message(self, table_name, user_id, username, message, timestamp=None):
        """Вставляет сообщение в таблицу"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {table_name} (user_id, username, message, timestamp)
                VALUES (?, ?, ?, ?);
            """, (user_id, username, message, timestamp))
            conn.commit()

    def select_messages_by_time(self, table_name, start_time):
        """Возвращает список сообщений, отправленных после указанного времени"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM {table_name}
                WHERE timestamp >= ?;
            """, (start_time,))
            return cursor.fetchall()

    def delete_messages_before_time(self, table_name, cutoff_time):
        """Удаляет сообщения, отправленные до указанного времени"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                DELETE FROM {table_name}
                WHERE timestamp < ?;
            """, (cutoff_time,))
            conn.commit()

if __name__ == '__main__':
        
    db = MessageDB()
    table_name = 'chat2'

    # db.create_table(table_name)

    # db.insert_message(table_name, 1, 'Артем', 'ляллялялялялялялля')
    # db.insert_message(table_name, 1, 'Артем', 'asl;dadkasl;dka')
    # db.insert_message(table_name, 1, 'Артем', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    # messages = db.select_messages_by_time(table_name, "2025-08-01T00:00:00")
    # for m in messages:
    #     print(m)

    db.delete_messages_before_time(table_name, "2025-08-09T00:00:00")
    db.select_messages_by_time(table_name, "2025-08-08T00:00:00")