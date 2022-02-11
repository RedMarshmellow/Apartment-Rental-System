#!C:\Program Files\Python310\python.exe
import sqlite3
import cgi


def printHeader(title):
    print("Content-type: text/html\n\n")
    print("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,700">
    <link rel="stylesheet" href="CSS/index.css">
    """)
    print("<html><head><title>{}</title></head><body>".format(title))


def printFooter():
    print("</body></html>")


printHeader("Login")

form = cgi.FieldStorage()

print(""" <div>
        <form action="register.py" method="post" name="regform">
            <h3>Register</h3>
            <div class="input-group">
            <label for="uname">Username</label>
            <input type="text" name="uname" id="uname" required>
            </div>
            <div class="input-group">
            <label for="pwd">Password</label>
            <input type="password" name="pwd" id="pwd" required>
            </div>
            <div class="input-group">
            <label for="fname">Full Name</label>
            <input type="text" name="fname" id="fname" required>
            </div>
            <div class="input-group">
            <label for="email">Email</label>
            <input type="text" name="email" id="email" required>
            </div>
            <div class="input-group">
            <label for="tel">Telephone</label>
            <input type="number" name="tel" id="tel" required>
            </div>
            <button type="submit">Register</button>
        </form>
        <form action="login.py" method="post" name="loginform">
            <h3>Login</h3>
            <div class="input-group">
            <label for="uname">Username</label>
            <input type="text" name="uname" id="uname" required>
            </div>
            <div class="input-group">
            <label for="pwd">Password</label>
            <input type="password" name="pwd" id="pwd" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>""")
print("""
<div>
<form action="index.py" method="post">
<label for="criteria">Sort By:</label>
<select name="criteria" id="criteria">
  <option value="0">Recency</option>
  <option value="1">Monthly Fee</option>
  <option value="2">Number of Bedrooms</option>
</select>
""")
if "criteria" in form.keys():
    cselect = str(form["criteria"].value)
else:
    cselect = '0'
criteria = {'0': 'houseid', '1': 'MonthlyFee', '2': 'noOfBedrooms'}
print("""
<label for="order">Order:</label>
<select name="order" id="order"">
  <option value="0">Descending</option>
  <option value="1">Ascending</option>
</select>
<button type="submit">Sort</button>
</form>
""")
if "order" in form.keys():
    oselect = str(form["order"].value)
else:
    oselect = '0'
order = {'0': 'DESC', '1': 'ASC'}
conn = sqlite3.connect("rent.db")
c = conn.cursor()

c.execute("""
SELECT H.street, H.cname, H.noOfBedrooms, H.MonthlyFee, U.email, U.phoneno FROM HOUSE as H
 JOIN USER as U 
 WHERE H.renterun = U.username 
 ORDER BY {} 
 {} LIMIT 10""".format(criteria[cselect], order[oselect]))

rows = c.fetchall()
if not rows:
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
                    <th rowspan="2">Contact Email</th>
                    <th rowspan="2">Contact Phone</th>
                </tr>
            </thead>
            <tbody>
        """)
    for row in rows:
        print("""
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(row[0], row[1], row[2], row[3], row[4], row[5]))
    print("""
    </tbody>
    </table>
    </div>
    """)

printFooter()
