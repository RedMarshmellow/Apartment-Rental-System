#!C:\Program Files\Python310\python.exe
import os
import sqlite3
import urllib.parse
import http.cookies as Cookie


def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))


def printFooter():
    print("</body></html>")


printHeader("DeleteID")
query = os.environ["QUERY_STRING"]
if "HTTP_COOKIE" in os.environ:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    if "session" in cookie.keys():
        if len(query) == 0:
            pass

        else:
            pairs = urllib.parse.parse_qs(query)
            conn = sqlite3.connect("rent.db")
            c = conn.cursor()
            c.execute("SELECT * FROM USER WHERE sessionid = ?", (cookie["session"].value,))
            row1 = c.fetchone()
            if row1 is not None:
                c.execute("SELECT * FROM HOUSE WHERE renterun = ? AND houseid = ?",(row1[0], pairs['q'][0]))
                row2 = c.fetchone()
                if row2 is not None:
                    c.execute("DELETE FROM HOUSE WHERE houseid = ?", (pairs['q'][0],))
                    conn.commit()
                else:
                    print("<script>")
                    print("location.href = 'https://www.youtube.com/watch?v=O2otihe65SI';")
                    print("</script>")
            else:
                print("<script>")
                print("location.href = 'https://www.youtube.com/watch?v=O2otihe65SI';")
                print("</script>")
            conn.close()
    else:
        print("<script>")
        print("location.href = 'https://www.youtube.com/watch?v=O2otihe65SI';")
        print("</script>")
else:
    print("<script>")
    print("location.href = 'https://www.youtube.com/watch?v=O2otihe65SI';")
    print("</script>")
print("<script>")
print("window.location = 'main.py'")
print("</script>")
printFooter()
