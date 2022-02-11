import sqlite3

conn = sqlite3.connect("rent.db")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS USER(
username TEXT PRIMARY KEY,
password TEXT NOT NULL,
fullname TEXT NOT NULL,
email TEXT NOT NULL,
sessionid TEXT NOT NULL,
phoneno INTEGER NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS HOUSE(
houseid INTEGER PRIMARY KEY,
street TEXT NOT NULL,
noOfBedrooms INTEGER NOT NULL,
MonthlyFee INTEGER NOT NULL,
renterun TEXT NOT NULL,
cname TEXT NOT NULL,
FOREIGN KEY (renterun) REFERENCES USER(username),
FOREIGN KEY (cname) REFERENCES CITY(cname))""")

c.execute("""CREATE TABLE IF NOT EXISTS CITY(
cid INTEGER PRIMARY KEY,
cname TEXT NOT NULL)""")

cities = [(1, 'Lefkosa'), (2, 'Girne'), (3, 'Gazi Magusa'), (4, 'Iskele'), (5, 'Guzelyurt'), (6, 'Lefke')]

c.executemany("INSERT OR IGNORE INTO CITY (cid, cname) VALUES (?,?)", cities)


conn.commit()

conn.close()