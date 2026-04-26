import pymysql

def get_connection():
    return pymysql.connect(
        host="shuttle.proxy.rlwy.net",
        port=28605,
        user="root",
        password="NUGzJSssSarOXeLaNvcLhnYNKZEiNBCa",
        database="railway",
        cursorclass=pymysql.cursors.DictCursor
    )
