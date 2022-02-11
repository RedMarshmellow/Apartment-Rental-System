#!C:\Program Files\Python310\python.exe
import http.cookies as Cookie
import random
import sqlite3
import cgi
import string

def printHeader(title):
	print ("Content-type: text/html")
	print ("")
	print ("<html><head><title>{}</title></head><body>".format(title))

def printFooter():
	print ("</body></html>")

printHeader("Login")


form = cgi.FieldStorage()
if "uname" in form.keys() and "pwd" in form.keys():
	conn = sqlite3.connect("rent.db")
	c = conn.cursor()
	c.execute("SELECT * FROM USER WHERE username = ? AND password = ?", (form["uname"].value, form["pwd"].value))
	row = c.fetchone()
	if row is not None:
		cookie = Cookie.SimpleCookie()
		cookie["session"] = str(random.randint(1,1000000)) + ''.join(random.choices(string.ascii_letters, k=3))
		cookie["session"]["domain"] = "localhost"
		cookie["session"]["path"] = "/"
		c.execute("UPDATE USER SET sessionid = ? WHERE username = ?", (cookie["session"].value, form["uname"].value))
		conn.commit()
		print ("<script>")
		print ("document.cookie = '{}';".format(cookie.output().replace("Set-Cookie: ", ""))) #Seting cookie with JS
		print ("window.location = 'main.py';")
		print ("</script>")
	else:
		print ("<p>Incorrect username and/or password</p>")
		print("<a href='index.py'><button>Return to Login Page</button></a>")
	conn.close()
else:
	print("<p>Please enter your username and password</p>")


printFooter()