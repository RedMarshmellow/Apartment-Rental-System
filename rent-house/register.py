#!C:\Program Files\Python310\python.exe
import sqlite3
import cgi
import html


def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))


def printFooter():
    print("</body></html>")


printHeader("Register")

form = cgi.FieldStorage()
if "uname" in form.keys() and "pwd" in form.keys():
    conn = sqlite3.connect("rent.db")
    c = conn.cursor()
    c.execute("SELECT * FROM USER WHERE username = ?", (form["uname"].value,))
    row = c.fetchone()
    if row is None:
        nuser = [(html.escape(form["uname"].value), html.escape(form["pwd"].value), html.escape(form["fname"].value),
                  html.escape(form["email"].value), -1, html.escape(form["tel"].value))]
        c.executemany("INSERT INTO USER (username, password, fullname, email, sessionid, phoneno) VALUES (?,?,?,?,?,?)",
                      nuser)
        conn.commit()
        print("<p>User Added</p>")
        print("<a href='index.py'><button>Return to Login Page</button></a>")
    else:
        print("""
        <p>User already in database</p>
        <a href="index.py"><button>Return to Landing Page</button>
        """)
    conn.close()
else:
    print("<p>Please enter your username and password</p>")

printFooter()
