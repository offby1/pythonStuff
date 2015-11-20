import sqlite3

with sqlite3.connect('duden2.db') as conn:
	c = conn.cursor()
	c.execute("PRAGMA foreign_keys = ON")
	c.execute("CREATE TABLE IF NOT EXISTS Woertern(Woertern TEXT, WordID INT PRIMARY KEY)")
	c.execute("CREATE TABLE IF NOT EXISTS Bedeutung(Bedeutung TEXT, WordID INT, FOREIGN KEY (WordID) REFERENCES Woertern (WordID))")
	c.execute("CREATE TABLE IF NOT EXISTS Synonyme(Synonym TEXT, WordID Int, FOREIGN KEY (WordID) REFERENCES Woertern (WordID))")
