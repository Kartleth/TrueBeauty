import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='luis2002',
                           database='truebeauty',
                        #    host='petvet.mysql.pythonanywhere-services.com',
                        #    user='petvet',
                        #    password='b15c419d98df06db4a88f8cee',
                        #    database='petvet$veterinaria',
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor)

def get_usuarios():
    conexion = obtener_conexion()
    query = "SELECT * FROM usuario"
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista

def get_citas_de_usuario(id_usuario:int):
    conexion = obtener_conexion()
    query = "SELECT DATE_FORMAT(C.fecha_creacion, '%d/%c/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora, S.nombre as nombre_servicio FROM cita C, servicio S WHERE C.id_servicio=S.id_servicio AND C.id_cliente="+str(id_usuario)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista

if __name__ == '__main__':
    print(get_citas_de_usuario(4))
