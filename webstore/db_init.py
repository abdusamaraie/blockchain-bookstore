import sqlite3 as sql

def addUser(name,email,password):
    con = sql.connect("mydb.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Users (name,email,password) VALUES (?,?,?)", (name,email,password))
    con.commit()
    cur.close()
    con.close()

def getUser(email):
    con = sql.connect("mydb.db")
    cur = con.cursor()
    try:
        cur.execute('SELECT userId from Users WHERE email = ? ', (email,))
        user = cur.fetchall()
        if len(user) < 0:
            return False
        else:
            return user[0][0]
    except Exception as e:
        return str(e)
    finally:
        cur.close()
        con.close()

def retrieveUsers():
    con = sql.connect("mydb.db")
    cur = con.cursor()
    cur.execute("SELECT name, email, password FROM Users")
    users = cur.fetchall()
    cur.close()
    con.close()
    return users


def userValidate(e,p):
    con = sql.connect("mydb.db")
    cur = con.cursor()

    try:
        login = cur.execute('SELECT * from Users WHERE email = ? AND password = ?', (e,p))
        if (len(login.fetchall()) > 0):
            return True
        else:
            return False
    except Exception as e:
        return str(e)
    finally:
        cur.close()
        con.close()


def add_item(userId,name,disc,picURL):
    con = sql.connect("mydb.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Items (userId,name,disc,pictureURL) VALUES (?,?,?,?)", (userId,name,disc,picURL))
    con.commit()
    con.close()

def get_items(userId):
    con = sql.connect("mydb.db")
    cur = con.cursor()
    cur.execute('SELECT itemId,name,disc,pictureURL from Items WHERE userId = ? ', (userId,))
    items = cur.fetchall()
    cur.close()
    con.close()
    return items
