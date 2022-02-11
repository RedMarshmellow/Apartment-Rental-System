#!C:\Program Files\Python310\python.exe
import http.cookies as Cookie
import sqlite3
import os

def printHeader(title):
	print ("Content-type: text/html")
	print ("")
	print ("<html><head><title>{}</title></head><body>".format(title))

def printFooter():
	print ("</body></html>")

printHeader("Logout process")

if "HTTP_COOKIE" in os.environ:
	cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
	if "session" in cookie.keys():
		conn = sqlite3.connect("rent.db")
		c = conn.cursor()
		c.execute("SELECT * FROM USER WHERE sessionid= ?", (cookie["session"].value,))
		row = c.fetchone()
		if row != None:
			c.execute("UPDATE USER SET sessionid = -1 WHERE username = ?", (row[0],))
			conn.commit()
			print ("<script>")
			print ("document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTF; path=/;';")
			print("window.location = 'index.py'")
			print ("</script>")
		else:
			print ("<p>No matching user!</p>")
		conn.close()
	else:
		print ("<p>You're not supposed to be here yet!, please log in from the home page first</p>")
else:
	print ("<p>You're not supposed to be here yet!, please log in from the home page first</p>")
print("<a href='index.py'>Click here to logout</a>")
printFooter()