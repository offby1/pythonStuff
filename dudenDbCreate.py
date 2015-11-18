import sqlite3

with sqlite3.connect('duden.db') as conn:
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS Woertern")
	c.execute("CREATE TABLE Woertern(Wort TEXT, Rechtschreibung VARCHAR(255), Bedeutung VARCHAR(255), Synonyme VARCHAR(255))")