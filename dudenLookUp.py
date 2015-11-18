import requests
import sqlite3
import sys
import bs4

if len(sys.argv) > 1:
	word = ' '.join(sys.argv[1:])
else:
	word = raw_input("""
Welches Wort wollen Sie nachschlagen?

(Beachten Sie bitte, dass nomen einen
grossen Anfangsbuchstaben brauchen,
waehrend alle anderen Woertern eienen
kleinen brauchen)

Wort: """)
try:
	#download the page
	res = requests.get('http://www.duden.de/rechtschreibung/' + word)
	res.raise_for_status()

	#create a Beautiful Soup instance to inspect the file
	noStarchSoup = bs4.BeautifulSoup(res.text, "lxml")

	#create the tuple that we will pass to SQLite
	word_data = (word,)
	for i in range(0,3):
		#find the first three blocks of relevant html code 
		#from the Duden website and add them to the tuple
		word_data += (unicode(noStarchSoup.select('#block-duden-tiles-' + str(i))),)

	#add the html and the word to the sqlite database
	with sqlite3.connect("/home/michael/nicePython/duden.db") as conn:
		c = conn.cursor()
		c.execute("INSERT INTO Woertern VALUES(?, ?, ?, ?)", word_data)
	print "Words Duden HTML Data successfully added to the Database!" 



except requests.exceptions.HTTPError as err:
	print "Ooops! We couldn't find the word!"
	print err.args