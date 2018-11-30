import sqlite3

conn = sqlite3.connect('MP01_SQL.db')
c = conn.cursor()
c.execute("DELETE FROM sessions")
c.execute("DELETE FROM descriptors")
conn.commit()
conn.close()
