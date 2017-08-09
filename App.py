import os

import numpy as np
import pandas as pd

from webbrowser import open_new_tab
from flask import Flask, render_template, redirect, request, jsonify
from flask import Flask, render_template, request, flash, send_from_directory
from flaskext.mysql import MySQL

from battle import Simulation

app = Flask(__name__)

############################ Data #######################


class Data:

    stats = pd.read_csv('Pokemon.csv').groupby('#').first()
    username = None
    password = None
    t1 = None
    t2 = None

class DB:

    def __init__(self, connection):
        self.connection = connection

    def check_un(username):
        cursor  = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{Data.username}'")
        result = cursor.fetchone()
        cursor.close()
        return result

    def check_un_pw(username, password):
        cursor  = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{Data.username}' AND password='{Data.password}'")
        result = cursor.fetchone()
        cursor.close()
        return result

    def signUp(username, password):
        cursor = self.connection.cursor()
        query = f"INSERT INTO users (username, password,wins,losses) VALUES ('{username}','{password}',0,0)"
        cursor.execute(query)
        conn.commit()
        cursor.close()

    def updateTable(res, username):
        cursor  = self.connection.cursor()
        if res:
            cursor.execute(f"UPDATE users SET wins=wins+1 WHERE username='{username}'")
        else:
            cursor.execute(f"UPDATE users SET losses=losses+1 WHERE username='{username}'")
        conn.commit()
        cursor.close()

    def get_wins_losses(username):
        cursor  = self.connection.cursor()
        cursor.execute(f"SELECT wins, losses FROM users WHERE username='{Data.username}'")
        result = cursor.fetchone()
        cursor.close()
        return result

app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DB']
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
db = DB(conn)

#########################################################

def choose_teams():
    t1 = np.random.choice(range(1, 722), size=5, replace=False)
    t2 = np.random.choice(range(1, 722), size=5, replace=False)
    t1 = Data.stats.loc[t1]
    t2 = Data.stats.loc[t2]
    return t1, t2

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Data.username = request.form['username']
        Data.password = request.form['password']
        data = db.check_un_pw(Data.username, Data.password)
        if data is None:
            error = 'Invalid username or password. Please try again!'
            return render_template('login.html', error=error)
        else:
            return redirect('battle')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Data.username = request.form['username']
        Data.password = request.form['password']
        data = db.check_un(Data.username)
        if data is not None:
            error = ' username has already been taken!'
            return render_template('signup.html', error=error)
        else:
            db.signUp(Data.username, Data.password)
            Data.t1, Data.t2 = choose_teams()
            return render_template('battle.html', t1=Data.t1, t2=Data.t2)
    return render_template('signup.html')

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'POST':
        guess = 0 if request.form['guess'] == 'team1' else 1
        result = Simulation(Data.t1.index.values, Data.t2.index.values, guess).run()
        print('Guess:', guess)
        print('result:', result)
        db.updateTable(result, Data.username)
    Data.t1, Data.t2 = choose_teams()
    wins, losses =  db.get_wins_losses(Data.username)
    return render_template('battle.html',
                           t1=Data.t1,
                           t2=Data.t2,
                           username=Data.username,
                           wins=wins,
                           losses=losses)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    #url = 'http://127.0.0.1:5001'
    #open_new_tab(url)
    #app.run(debug=True)
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
