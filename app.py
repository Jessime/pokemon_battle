
from flask import Flask, render_template, request, flash, send_from_directory
from flaskext.mysql import MySQL
############### App ##################3
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sonoma'
app.config['MYSQL_DATABASE_DB'] = 'pokemon_schema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor=conn.cursor()


############################################################# HOME ###########################################################################
@app.route('/')
def main():
    return render_template('home.html')

############################################################  Authentication ##########################################################################
@app.route("/Authenticate", methods = ['POST', 'GET'])
def Authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
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



if __name__ == '__main__':
    app.run(debug=True, port=5000)