import sqlite3

c = sqlite3.connect("database.db")
cursor = c.cursor()

cursor.execute("CREATE TABLE User("
                "username TEXT PRIMARY KEY,"
                "password TEXT NOT NULL,"
                "fullname TEXT NOT NULL,"
                "email TEXT NOT NULL,"
                "telno TEXT NOT NULL)")


cursor.execute("CREATE TABLE Advertisement("
                "aid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "title TEXT NOT NULL,"
                "description TEXT NOT NULL,"
                "isactive BOOLEAN DEFAULT 1,"
                "username TEXT NOT NULL,"
                "cid INTEGER NOT NULL,"
                "FOREIGN KEY (cid) REFERENCES Category (cid)," # foreign keys added because of the 1 to many relationship 
                "FOREIGN KEY (username) REFERENCES User (username))")


cursor.execute("CREATE TABLE Category("
                "cid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "cname TEXT NOT NULL)")



cursor.execute("INSERT INTO Category (cname) VALUES(?)", ("Clothes",))
cursor.execute("INSERT INTO Category (cname) VALUES(?)", ("Technology",))
cursor.execute("INSERT INTO Category (cname) VALUES(?)", ("Cars",))
cursor.execute("INSERT INTO Category (cname) VALUES(?)", ("Food",))
cursor.execute("INSERT INTO Category (cname) VALUES(?)", ("Drink",))

cursor.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?)", ("mexikali", "123", "Ömer Faruk Sezen", "omer.sezen@gmail.com", "05446912161"))
cursor.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?)", ("umut", "123", "Umut Yilmaz", "umut.yilmaz@gmail.com", "05399518000"))
c.commit()