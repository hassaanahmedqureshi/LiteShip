import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path='data/liteship.db'):
        self.db_path = db_path
        Path('data').mkdir(exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Master list
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS master_list (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        courier TEXT NOT NULL
                    )
                ''')

        # Freight rates
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS freight_rates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        master_list_id INTEGER NOT NULL,
                        weight_min REAL NOT NULL,
                        weight_max REAL NOT NULL,
                        price REAL NOT NULL,
                        FOREIGN KEY (master_list_id) REFERENCES master_list(id)
                    )
                ''')

        # Accessories
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS accessories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        master_list_id INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        calc_type TEXT NOT NULL,
                        value REAL NOT NULL,
                        FOREIGN KEY (master_list_id) REFERENCES master_list(id)
                    )
                ''')

        # Clients
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        code TEXT UNIQUE NOT NULL
                    )
                ''')

        # Sales list
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sales_list (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER NOT NULL,
                        master_list_id INTEGER NOT NULL,
                        FOREIGN KEY (client_id) REFERENCES clients(id),
                        FOREIGN KEY (master_list_id) REFERENCES master_list(id)
                    )
                ''')

        # Markup rules
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS markup_rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sales_list_id INTEGER NOT NULL,
                        applies_to TEXT NOT NULL,
                        calc_type TEXT NOT NULL,
                        value REAL NOT NULL,
                        FOREIGN KEY (sales_list_id) REFERENCES sales_list(id)
                    )
                ''')

        conn.commit()
        conn.close()
        print("✅ Database initialized!")

if __name__ == '__main__':
    db = DatabaseManager()