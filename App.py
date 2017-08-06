import numpy as np
import pandas as pd

from webbrowser import open_new_tab
from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__)

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
        t1, t2 = choose_teams()
        print(t1.index)
        return render_template('battle.html', t1=t1, t2=t2)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print('Sign up')
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

if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    open_new_tab(url)
    app.run(debug=True)
