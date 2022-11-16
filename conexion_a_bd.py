import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',
                           # host='mysql_host',
                           user='root',
                           password='luis2002',
                           database='truebeauty',
                           # user='admin',
                           # password='admin_123',
                           # database='truebeauty',
                           #    host='petvet.mysql.pythonanywhere-services.com',
                           #    user='petvet',
                           #    password='b15c419d98df06db4a88f8cee',
                           #    database='petvet$veterinaria',
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor)
