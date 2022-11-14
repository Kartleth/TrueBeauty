import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',
                           #host='mysql_host',
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

""" 
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
"""

def get_citas_de_usuario(columna: str, id_usuario: int):
    conexion = obtener_conexion()
    query = "SELECT C.id_cita, DATE_FORMAT(C.fecha, '%d/%c/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora, S.nombre as nombre_servicio FROM cita C, servicio S WHERE C.id_servicio=S.id_servicio AND C." + columna + "=" + str(
        id_usuario)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def cita_pertenece_a_usuario(columna: str, id_usuario: int, id_cita: int):
    conexion = obtener_conexion()
    query = "SELECT * FROM cita WHERE " + columna + "=" + str(id_usuario) + " AND id_cita=" + str(id_cita)
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def get_info_cita(id_cita: int):
    conexion = obtener_conexion()
    query = "SELECT C.id_cita,DATE_FORMAT(C.fecha, '%d/%c/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora, SU.nombre as nombre_sucursal, SU.direccion as direccion_sucursal, SE.nombre as nombre_servicio, SE.precio as precio_servicio, SE.descripcion as descripcion_servicio FROM cita C, sucursal SU, servicio SE WHERE C.id_servicio=SE.id_servicio AND C.id_sucursal=SU.id_sucursal AND C.id_cita=" + str(
        id_cita)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]


def get_lista_servicios():
    conexion = obtener_conexion()
    query = "SELECT CONCAT(id_servicio,'') as id_servicio, nombre, descripcion, CONCAT(precio,'') as precio, tiempo FROM servicio"
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def get_lista_sucursales():
    conexion = obtener_conexion()
    query = "SELECT * FROM sucursal"
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista

def get_lista_estilistas_de_sucursal(id_sucursal):
    conexion = obtener_conexion()
    query = "SELECT id_usuario,turno FROM empleado WHERE id_sucursal="+id_sucursal
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


if __name__ == '__main__':
    print(get_lista_servicios())
    print(get_lista_sucursales())