from flask import *
import sqlite3


app = Flask(__name__)
app.secret_key = "secret key"

def connectDatabase(query):
    """
    Connects to a SQLite database and executes the given query.
    Parameters:
    - query (str): SQL query to be executed.
    Returns:
    - If the query is a SELECT query, returns the fetched data.
    - If the query is not a SELECT query, returns 1.
    Note:
    - SQLite database name should be 'database.db'
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()

    opType = query.split(" ")[0]

    if opType == "SELECT":
        data = c.fetchall()
        conn.close()
        return data
    else:
        conn.close()
        return 1


@app.route("/")
@app.route("/index")
def index():
    """
    If the user is authenticated (username in session), it renders the homepage
    with the username and the categories.
    If the user is not authenticated, it renders the homepage with only the categories.
    """
    query = "SELECT * FROM Category"
    categories = connectDatabase(query)

    if "username" in session:
        return render_template("homepage.html", username=session["username"], categories=categories)
    else:
        return render_template("homepage.html", categories=categories)

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        telno = request.form['telno']
        error = None
        try:
            str1 = f"INSERT INTO User(username, password, fullname, email, telno) VALUES('{username}', '{password}', '{fullname}', '{email}', '{telno}');"
            row = connectDatabase(str1)
            return render_template('registration.html',msg="Succesfull")
        except Exception as e:
            if "UNIQUE constraint failed: User.username" == str(e):
                return render_template('registration.html',msg="ERROR",msg1="Username must be unique!!!")
            else:
                return render_template('registration.html',msg="ERROR",msg1=str(e))

    return render_template('registration.html')

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = f"SELECT * FROM User WHERE username='{username}' and password='{password}'"
        try:
            result = connectDatabase(query)
            if result:
                session["username"] = result[0][0]
                return render_template('login.html', msg="success")
            else:
                return render_template('login.html', msg="error")
        except:
            return render_template('login.html', msg="error")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/')


@app.route('/myprofile', methods=['GET', 'POST'])
def myprofile():
    user = session.get('username')
    str1 = f"SELECT * FROM User WHERE username = '{user}';"
    query = connectDatabase(str1)
    username = query[0][0]
    password = query[0][1]
    fullname = query[0][2]
    email = query[0][3]
    telno = query[0][4]
    
    if request.method=="POST":
        username1 = request.form["username"]
        password1 = request.form['password']
        fullname1 = request.form['fullname']
        email1 = request.form['email']
        telno1 = request.form['telno']

        try:
            str2 = f"UPDATE User SET username='{username1}', password='{password1}', fullname='{fullname1}', email='{email1}', telno='{telno1}' WHERE username='{user}';"
            row = connectDatabase(str2)
            if row == 1:
                session["username"] = username1
                return render_template('myprofile.html',msg="SUCCESFUL", username=username1, password=password1, fullname=fullname1, email=email1, telno=telno1)
            else:
                return render_template('myprofile.html',msg="ERROR", username=username, password=password, fullname=fullname, email=email, telno=telno)
        except Exception as e:
            if "UNIQUE constraint failed: User.username" == str(e):
                return render_template('myprofile.html',msg="ERROR",msg1="Username must be unique!!!", username=username, password=password, fullname=fullname, email=email, telno=telno)
            else:
                return render_template('myprofile.html',msg="ERROR",msg1=str(e), username=username, password=password, fullname=fullname, email=email, telno=telno)

    return render_template('myprofile.html', username=username, password=password, fullname=fullname, email=email, telno=telno)

@app.route('/myAd', methods=['GET', 'POST'])
def myAd():
    if "username" in session:

        query = "SELECT * FROM Category"
        categories = connectDatabase(query)

        username = session.get('username')
        query1 = f"SELECT a.title, a.description, c.cname, a.isactive, a.aid FROM Category as c, Advertisement as a WHERE a.cid = c.cid and username='{username}'"
        
        if request.method=="POST":
            title = request.form["title"]
            description = request.form['description']
            category = int(request.form['category'])
            
            try:
                
                query2 = f"INSERT INTO Advertisement(title, description, username, cid) VALUES('{title}', '{description}', '{username}', {category});"
                result = connectDatabase(query2)
                ads = connectDatabase(query1)
                return render_template('myAd.html', msg="success", ads = ads, categories=categories)
            
            except:
                ads = connectDatabase(query1)
                return render_template('myAd.html', msg="error", ads = ads, categories=categories)
            
        ads = connectDatabase(query1)
        return render_template('myAd.html', ads = ads, categories=categories)
    
    return redirect(url_for('index'))

@app.route('/activation', methods=['GET', 'POST'])
def activation():
    if "username" in session:
        
        query = "SELECT * FROM Category"
        categories = connectDatabase(query)

        username = session.get('username')
        type = request.args.get('type')
        aid = request.args.get('aid')
        query1 = f"SELECT a.title, a.description, c.cname, a.isactive, a.aid FROM Category as c, Advertisement as a WHERE a.cid = c.cid and username='{username}'"
        try:
            query = f"UPDATE Advertisement SET isactive='{type}' WHERE aid='{aid}';"
            result = connectDatabase(query)
            if result == 1:
                ads = connectDatabase(query1)
                return render_template('myAd.html',update="SUCCESFUL", ads = ads, categories=categories)
            else:
                ads = connectDatabase(query1)
                return render_template('myAd.html',update="ERROR", ads = ads, categories=categories)
        except Exception as e:
            ads = connectDatabase(query1)
            return render_template('myAd.html',update="ERROR", ads = ads, categories=categories)
        
        ads = connectDatabase(query1)
        return render_template('myAd.html',update="ERROR", ads = ads, categories=categories)
    
    return redirect(url_for('index'))


@app.route('/actives', methods=['GET', 'POST'])
def getActiveAd():
    if request.method=="POST":
        
        keyword = request.form['keyword']
        category = int(request.form['category'])

        query = "SELECT * FROM Category"
        categories = connectDatabase(query)

        query = f"SELECT a.title, a.description, c.cname, u.fullname, u.email, u.telno FROM User as u, Category as c, Advertisement as a WHERE a.cid=c.cid AND a.username=u.username AND a.isactive = 1 AND (a.title LIKE '%{keyword}%' OR a.description LIKE '%{keyword}%' OR u.fullname LIKE '%{keyword}%')" 
        if category == 0:
            query += ";"
        else:
            query = query + f" AND c.cid={category};"
        try:
            row = connectDatabase(query)
            data = {}
            if len(row) != 0:
                for i in row:
                    if i[2] in data:
                        data[i[2]].append(i)
                    else:
                        data[i[2]] = [i]
            
            if "username" in session and len(row) == 0:
                return render_template("homepage.html", username=session["username"],msg="error", categories=categories)
            elif "username" in session and len(row) != 0:
                return render_template("homepage.html", username=session["username"],msg=data, categories=categories)
            elif len(row) != 0:
                return render_template("homepage.html",msg=data, categories=categories)
            else:
                return render_template("homepage.html",msg="error", categories=categories)
        except:
            if "username" in session:
                return render_template("homepage.html", username=session["username"],msg="error", categories=categories)
            else:
                return render_template("homepage.html",msg="error", categories=categories)
    
    return redirect(url_for('index')) 

@app.route('/seeMore', methods=['GET'])
def seeMore():
    title = request.args.get('title')
    description = request.args.get('description')
    category = request.args.get('category')
    fullname = request.args.get('fullname')
    email = request.args.get('email')
    tel = request.args.get('tel')

    return render_template("seeMore.html",title=title,description=description,category=category,fullname=fullname,email=email,tel=tel)


if __name__ == '__main__':
    app.run()
