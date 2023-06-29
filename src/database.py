import sqlite3 as sql


class DB:
    def create(self):
        """Create database"""
        self.conn = sql.connect('data.db')
        self.cursor = self.conn.cursor()
        self.query = "CREATE TABLE data (ci text,name text)"
        self.cursor.execute(self.query)
        self.conn.commit()
        self.conn.close()

    def insert(self, data_list):
        """Insert data in the database"""
        self.conn = sql.connect('data.db')
        self.cursor = self.conn.cursor()
        self.query = f"INSERT INTO data VALUES (?, ?)"
        self.cursor.executemany(self.query, data_list)
        self.conn.commit()
        self.conn.close()

    def delete(self, ci):
        self.conn = sql.connect('data.db')
        self.cursor = self.conn.cursor()
        self.query = f"DELETE FROM data WHERE ci='{ci}'"
        self.cursor.execute(self.query)
        self.conn.commit()
        self.conn.close()

    def search(self, ci):
        """Search data in the database"""
        self.conn = sql.connect('data.db')
        self.cursor = self.conn.cursor()
        self.query = f"SELECT * FROM data WHERE ci = '{ci}'"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()

        return self.result