import numpy as np
import pandas as pd

from webbrowser import open_new_tab
from flask import Flask, render_template, redirect, request, jsonify
from flask import Flask, render_template, request, flash, send_from_directory
from flaskext.mysql import MySQL

app = Flask(__name__)

####################################### Sherif ###################################
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sonoma'
app.config['MYSQL_DATABASE_DB'] = 'pokemon_schema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor=conn.cursor()
####################################################################################

class Data:

    stats = pd.read_csv('Pokemon.csv').groupby('#').first()
    username = None
    password = None

def choose_teams():
    t1 = np.random.choice(range(1, 722), size=5, replace=False)
    t2 = np.random.choice(range(1, 722), size=5, replace=False)
    t1 = Data.stats.loc[t1]
    t2 = Data.stats.loc[t2]
    return t1, t2

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('Login')
        username = request.form['username']
        password = request.form['password']
        print username, password
        cursor.execute("SELECT * from pokemon_table where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            error = 'Invalid username or password. Please try again!'
            return render_template('login.html', error=error)
        else:
            #flash('You were successfully logged in')
            t1, t2 = choose_teams()
            return render_template('battle.html', t1=t1, t2=t2)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print('Sign up')
        username = request.form['username']
        password = request.form['password']

        print username, password
        cursor.execute("SELECT * from pokemon_table where username='" + username + "'")
        data = cursor.fetchone()
        if data is not None:
            error = ' username has already been taken!'
            return render_template('signup.html', error=error)
        else:
            signUp(username, password)
            t1, t2 = choose_teams()
            return render_template('battle.html', t1=t1, t2=t2)
    return render_template('signup.html')

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'POST':
        print('Sign up')
    t1, t2 = choose_teams()
    return render_template('battle.html', t1=t1, t2=t2)

@app.route('/')
def index():
    return render_template('index.html')



#### ####################### Sherif #######################
@app.route("/Authenticate", methods = ['POST', 'GET'])
def Authenticate():
    username = request.form['username']
    password = request.form['password']
    username="bonerChamps"
    password="joe"
    str="SELECT * from pokemon_table where username='" + username + "' and password='" + password + "'"
    cursor.execute("SELECT * from pokemon_table where username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    print type(data),
    if data is None:
        error = 'Invalid username or password. Please try again!'

        return render_template('home.html', error=error)
    else:
        error = 'You were successfully logged in'
        return render_template('login.html', error=error)


def signUp(username, password):
    query = "INSERT INTO pokemon_table (username, password,wins,losses) VALUES ('{}','{}',0,0)".format(username, password)
    cursor.execute(query)
    conn.commit()


def updateTable(res, username):
    if res:
        cursor.execute("UPDATE pokemon_table SET wins=wins+1 WHERE username='{}' ".format(username))
        conn.commit()
    else:
        cursor.execute("UPDATE pokemon_table SET losses=losses+1 WHERE username='{}'".format(username))
        conn.commit()
##############################################################

if __name__ == "__main__":
    url = 'http://127.0.0.1:5001'
    #open_new_tab(url)
    app.run(debug=True)
