#!C:\Program Files\Python310\python.exe
import http.cookies as Cookie
import sqlite3
import os
import cgi
import html


def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("""
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,700">
        <link rel="stylesheet" href="CSS/main.css"> 
        """)  # designate external style sheet and import font
    print("<html><head><title>{}</title></head><body>".format(title))


def printFooter():
    print("</body></html>")


printHeader("Welcome to the user page!")

if "HTTP_COOKIE" in os.environ:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    if "session" in cookie.keys():
        conn = sqlite3.connect("rent.db")
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE sessionid = ?", (cookie["session"].value,))  # validate cookie vs session ID
        row1 = c.fetchone()
        if row1 is not None:
            print("<h1>Welcome {}!</h1>".format(row1[0]))
            print("""
            <form method='post' action = 'main.py'>
            <h3>Add Apartment</h3>
            <div class="input-group">
            <label for="street">Street</label>
            <input type="text" name="street" id="street" required>
            </div>
			<div class="input-group">
            <label for="city">City</label>
            <input type="text" name="city" id="city" required>
            </div>
			<div class="input-group">
            <label for="noOfBedroom">Number of Bedrooms</label>
            <input type="number" name="noOfBedroom" id="noOfBedroom" required>
            </div>
			<div class="input-group">
            <label for="MonthlyFee">Monthly Fee</label>
            <input type="number" name="MonthlyFee" id="MonthlyFee" required>
            </div>
			<button type="submit">Add</button>
			</form>
			""")
            print("<a href='logout.py'><button>Log Out</button></a>")
            form = cgi.FieldStorage()
            if "city" in form.keys():
                c.execute("SELECT * FROM CITY WHERE cname = ?", (html.escape(form["city"].value),))
                row3 = c.fetchone()
                if "street" in form.keys() and "city" in form.keys() and "noOfBedroom" in form.keys() and "MonthlyFee" in form.keys():
                    if row3 is not None:
                        c.execute("SELECT MAX(houseid) FROM HOUSE")
                        row2 = c.fetchone()
                        hid = row2[0]
                        run = row1[0]
                        if hid is None:
                            hid = 0
                        nhouse = [
                            (int(hid) + 1, html.escape(form["street"].value), html.escape(form["noOfBedroom"].value),
                             html.escape(form["MonthlyFee"].value), run, html.escape(form["city"].value))]
                        c.executemany(
                            "INSERT INTO HOUSE (houseid, street, noOfBedrooms, MonthlyFee, renterun, cname) VALUES ("
                            "?,?,?,?,?,?)", nhouse)
                    else:
                        print("<p>Invalid City</p>")
                else:
                    print("<p>Please input correct data in all given fields</p>")
                conn.commit()
                print("<script>")
                print(
                    "window.location = 'main.py'")  # This redriect exists to prevent the program from adding the same apartment twice in case of a refresh of the page
                print("</script>")
        else:
            print("<p>Login required!")
        c.execute(
            "SELECT houseid, street, cname, noOfBedrooms, MonthlyFee, renterun from HOUSE  where renterun = ?",
            (row1[0],))
        row4 = c.fetchall()
        if not row4:
            print("<p>No Advertisments Found</p>")
        else:
            print("""
                    <table>
                        <thead>
                            <tr>
                                <th rowspan="2">Street</th>
                                <th rowspan="2">City</th>
                                <th rowspan="2">Number of Bedrooms</th>
                                <th rowspan="2">Monthly Fee</th>
                                <th rowspan="2">Delete?</th>
                            </tr>
                        </thead>
                        <tbody>
                    """)
            for row in row4:
                print("""
                       <tr>
                           <td>{}</td>
                           <td>{}</td>
                           <td>{}</td>
                           <td>{}</td>
                           <td><a href='delete.py?q={}'><button>Delete</button></a></td>
                       </tr>
                       """.format(row[1], row[2], row[3], row[4], row[0]))
            print("""
                </tbody>
                </table>
                """)
        conn.close()
    else:
        print("<p>Login required!")
else:
    print("<p>Login required!")

printFooter()
