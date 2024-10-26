# este archivo debería llamarse config.py e ingresar los datos respectivos

from flask_mysqldb import MySQL

def init_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = ''
    mysql = MySQL(app)
    return mysql



class Config:
    SECRET_KEY = ""
    OPENAI_API_KEY = "sk-proj--"