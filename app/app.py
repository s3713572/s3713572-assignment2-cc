import os
from flask import Flask
from flask_mysqldb import MySQL
from dotenv import dotenv_values
from config.db import db_conifg

app = Flask(__name__)

app.config['MYSQL_HOST'] = db_conifg['MYSQL_HOST']
app.config['MYSQL_USER'] = db_conifg['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = db_conifg['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = db_conifg['MYSQL_DB']

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')