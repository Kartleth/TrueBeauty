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


def get_lista_estilista_por_sucursal_servicio(id_sucursal, id_servicio):
    conexion = obtener_conexion()
    # query = "SELECT E.id_usuario FROM empleado E, estilista_servicio ES WHERE E.id_usuario=ES.id_estilista AND ES.id_servicio=" + id_servicio + " AND E.id_sucursal=" + id_sucursal + " AND E.id_usuario=(SELECT estilista_minimo.id_estilista FROM (SELECT servicios_por_estilista.id_estilista, min(servicios_por_estilista.num_servicios) AS num_servicios FROM (SELECT id_estilista, count(id_estilista) as num_servicios FROM estilista_servicio) as servicios_por_estilista LIMIT 1 ) as estilista_minimo)"
    query = "SELECT E.id_usuario FROM empleado E, estilista_servicio ES WHERE E.id_usuario=ES.id_estilista AND E.id_sucursal=" + id_sucursal + " AND ES.id_servicio=" + id_servicio
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista

def estilista_tiene_cita(hora,id_estilista,fecha):
    conexion = obtener_conexion()
    query = "SELECT id_cita FROM cita WHERE hora='"+str(hora)+"' AND id_estilista="+str(id_estilista)+" AND fecha='"+fecha+"'"
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

# def hora_esta_disponible(hora,id_estilista,id_servicio):
#     conexion = obtener_conexion()
#     query = ""
#     with conexion.cursor() as cursor:
#         cursor.execute(query)
#         if cursor.fetchone() is None:
#             return True
#     conexion.commit()
#     conexion.close()
#     return False

if __name__ == '__main__':
    print(get_lista_servicios())
    print(get_lista_sucursales())
