from flask import Flask

from flaskext.mysql import MySQL


app = Flask(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sonoma'
app.config['MYSQL_DATABASE_DB'] = 'pokemondb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor=conn.cursor()
