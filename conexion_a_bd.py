import pymysql


def obtener_conexion():
    return pymysql.connect(#host='localhost',
                           # host='mysql_host',
                           # user='root',
                           # password='luis2002',
                           # database='truebeauty',
                           # user='admin',
                           # password='admin_123',
                           # database='truebeauty',
                              host='esteticatruebeauty.mysql.pythonanywhere-services.com',
                              user='esteticatruebeau',
                              password='Mysql_password',
                              database='esteticatruebeau$truebeauty',
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor)
