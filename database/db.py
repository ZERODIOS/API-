import pymysql

def get_connection():
    return pymysql.connect(
        host="caboose.proxy.rlwy.net",
        port=35240,
        user="root",
        password="BUOaiJaLrBhLNWhNSFwAPALuJmzxZQby",
        database="railway",
        cursorclass=pymysql.cursors.DictCursor
    )
