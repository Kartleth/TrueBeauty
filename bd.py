from conexion_a_bd import obtener_conexion

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
    query = "SELECT C.id_cita, DATE_FORMAT(C.fecha, '%d/%c/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora, C.monto FROM cita C WHERE  C." + columna + "=" + str(
        id_usuario) + " ORDER BY C.fecha"
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
    query = "SELECT C.id_cita,DATE_FORMAT(C.fecha, '%d/%m/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora,DATE_FORMAT(C.hora_fin, '%H:%i') as hora_fin, SU.nombre as nombre_sucursal, SU.direccion as direccion_sucursal,SU.id_sucursal, C.monto,C.iva,C.total, U.nombre as nombre_cliente, U.apellido_paterno as apellido1_cliente, U.apellido_materno as apellido2_cliente, U.correo AS correo FROM cita C, sucursal SU, servicio SE, usuario U WHERE  C.id_sucursal=SU.id_sucursal AND C.id_cliente=U.id_usuario AND C.id_cita=" + str(
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


def estilista_tiene_cita(hora, id_estilista, fecha, hora_fin, id_cita_a_modificar):
    conexion = obtener_conexion()
    if id_cita_a_modificar is None:
        query = "SELECT CS.id_estilista from cita_servicio CS, cita C WHERE C.id_cita=CS.id_cita AND C.fecha='" + fecha + "' AND CS.hora_inicio<='" + hora + "' AND CS.hora_fin>'" + hora + "' AND CS.id_estilista=" + str(
        id_estilista)
    else:
        query = "SELECT CS.id_estilista from cita_servicio CS, cita C WHERE C.id_cita=CS.id_cita AND C.fecha='" + fecha + "' AND CS.hora_inicio<='" + hora + "' AND CS.hora_fin>'" + hora + "' AND CS.id_estilista=" + str(
            id_estilista)+" AND NOT C.id_cita="+id_cita_a_modificar
    # query = "SELECT CS.id_estilista from cita_servicio CS, cita C WHERE C.id_cita=CS.id_cita AND C.fecha='" + fecha + "' AND (C.hora BETWEEN '" + hora + "' AND '" + str(hora_fin) + "') AND CS.id_estilista=" + str(
    #     id_estilista)
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

def get_servs_por_lista_id(lista_id_servicio):
    conexion = obtener_conexion()
    query = "SELECT * FROM servicio WHERE"
    for id_servicio in lista_id_servicio:
        query += ' id_servicio=' + str(id_servicio) + " OR"
    query = query[:-2]
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def get_info_sucursal(id_sucursal):
    conexion = obtener_conexion()
    query = "SELECT * FROM sucursal WHERE id_sucursal=" + id_sucursal

    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]


def get_lista_citas():
    conexion = obtener_conexion()
    query = "SELECT C.id_cita,U.nombre,U.apellido_paterno,U.apellido_materno, DATE_FORMAT(C.fecha, '%d/%c/%Y') as fecha, DATE_FORMAT(C.hora, '%H:%i') as hora, C.monto,S.nombre as nombre_sucursal FROM cita C, usuario U, sucursal S WHERE C.id_cliente=U.id_usuario AND C.id_sucursal=S.id_sucursal ORDER BY C.fecha DESC"

    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def calcular_monto(lista_id_servicio):
    conexion = obtener_conexion()
    query = "SELECT SUM(precio) as precio FROM servicio WHERE"
    for id_servicio in lista_id_servicio:
        query += ' id_servicio=' + str(id_servicio) + " OR"
    query = query[:-2]
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]


def insert_into_cita(fecha, hora, hora_fin, id_cliente, id_sucursal, monto, iva, total):
    conexion = obtener_conexion()
    lista = []
    id_cliente = str(id_cliente)
    id_sucursal = str(id_sucursal)
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO cita (fecha, hora, hora_fin, id_cliente, id_sucursal, monto, iva, total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (fecha, hora, hora_fin, id_cliente, id_sucursal, monto, iva, total))
        cursor.execute(
            "SELECT id_cita FROM cita WHERE fecha='" + fecha + "' AND hora='" + hora + "' AND id_cliente=" + id_cliente + " AND id_sucursal=" + id_sucursal)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['id_cita']


def get_nombre_servicios_de_cita(id_cita):
    conexion = obtener_conexion()
    query = "SELECT S.nombre FROM cita_servicio CS, servicio S WHERE CS.id_servicio=S.id_servicio AND CS.id_cita=" + str(
        id_cita)

    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def get_posibles_estilistas(id_sucursal, id_servicio):
    conexion = obtener_conexion()
    print(id_servicio, id_sucursal)
    query = "SELECT DISTINCT U.id_usuario AS id_estilista FROM usuario U, empleado E, estilista_servicio ES WHERE U.tipo_usuario='estilista' AND E.id_usuario=U.id_usuario AND E.id_sucursal=" + str(
        id_sucursal) + " AND ES.id_estilista=E.id_usuario AND ES.id_servicio=" + str(id_servicio)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()

    lista_id_estilistas = []
    for dicc in lista:
        lista_id_estilistas.append(dicc['id_estilista'])
    return lista_id_estilistas


def get_tiempo_servicio(id_servicio):
    conexion = obtener_conexion()
    query = "SELECT tiempo FROM servicio WHERE id_servicio=" + id_servicio
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['tiempo']


def insert_into_cita_servicio(id_cita, id_servicio, id_estilista, hora_inicio, hora_fin):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO cita_servicio  VALUES (%s,%s,%s,%s,%s)",
            (id_cita, id_servicio, str(id_estilista), hora_inicio, hora_fin))

    conexion.commit()
    conexion.close()


def get_lista_citas_fechas(fecha1, fecha2) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT a.id, a.fecha, u.name as cliente, m.nombre_mascota, m.tipo_mascota, a.descripcion, a.subtotal, a.iva, a.total FROM atenciones a, users u, mascotas m WHERE (DATE(fecha) BETWEEN %s and %s) and u.id=a.user_id and m.id=a.mascota_id",
            (fecha1, fecha2))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_servicio(id_servicio):
    conexion = obtener_conexion()
    query = "SELECT CONCAT(id_servicio,'') as id_servicio, nombre, descripcion, CONCAT(precio,'') as precio, tiempo FROM servicio WHERE id_servicio=" + id_servicio
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def get_lista_info_servicios(id_cita):
    conexion = obtener_conexion()
    query = "SELECT cs.id_servicio, S.nombre AS nombre_servicio, S.descripcion ,S.precio ,U.nombre AS nombre_estilista, U.apellido_paterno as apellido1_estilista  FROM cita_servicio CS, usuario U, servicio S WHERE CS.id_estilista=U.id_usuario AND CS.id_servicio=S.id_servicio AND CS.id_cita=" + id_cita
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def update_servicio(id_servicio, nombre, precio, descripcion, tiempo):
    conexion = obtener_conexion()
    query = "UPDATE servicio SET nombre='" + nombre + "' , precio=" + precio + " , descripcion='" + descripcion + "' , tiempo=" + tiempo + " WHERE id_servicio=" + id_servicio
    with conexion.cursor() as cursor:
        cursor.execute(query)
    conexion.commit()
    conexion.close()


def insert_into_servicio(nombre, precio, descripcion, tiempo):
    conexion = obtener_conexion()
    query = "INSERT INTO servicio (nombre, precio, descripcion, tiempo) VALUES ('" + nombre + "', " + precio + ", '" + descripcion + "', " + tiempo + ")"
    print(query)
    with conexion.cursor() as cursor:
        cursor.execute(query)
    conexion.commit()
    conexion.close()


def hay_servicio_con_ese_nombre(nombre):
    conexion = obtener_conexion()
    query = "SELECT id_servicio FROM servicio WHERE nombre='" + nombre + "'"
    print(query)
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def get_lista_clientes():
    conexion = obtener_conexion()
    query = "SELECT * FROM usuario WHERE tipo_usuario='cliente'"
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista


def id_es_de_cliente(id_usuario):
    conexion = obtener_conexion()
    query = "SELECT id_usuario FROM usuario WHERE id_usuario=" + id_usuario + " AND tipo_usuario='cliente'"
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def get_info_cliente(id_cliente):
    conexion = obtener_conexion()
    query = "SELECT * FROM usuario WHERE id_usuario=" + id_cliente
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]


def get_lista_id_servicios_de_cita(id_cita):
    conexion = obtener_conexion()
    query = "SELECT id_servicio FROM cita_servicio WHERE id_cita=" + id_cita
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    lista_de_id = []
    for dicc in lista:
        lista_de_id.append(str(dicc['id_servicio']))
    return lista_de_id


def get_asientos_de_sucursal(id_sucursal):
    conexion = obtener_conexion()
    query = "SELECT asientos FROM sucursal WHERE id_sucursal=" + id_sucursal
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['asientos']


def get_asientos_ocupados_de_sucursal(id_sucursal, fecha, hora, id_cita_a_modificar):
    conexion = obtener_conexion()
    if id_cita_a_modificar is None:
        query = "SELECT count(id_cita) as num_asientos_ocupados FROM cita C WHERE  C.id_sucursal="+id_sucursal+" AND C.fecha='"+fecha+"' AND C.hora<='"+hora+"' AND C.hora_fin>'"+hora+"'"
    else:
        query = "SELECT count(id_cita) as num_asientos_ocupados FROM cita C WHERE  C.id_sucursal="+id_sucursal+" AND C.fecha='"+fecha+"' AND C.hora<='"+hora+"' AND C.hora_fin>'"+hora+"' AND NOT C.id_cita="+id_cita_a_modificar

    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['num_asientos_ocupados']


def cliente_ya_tiene_cita(id_cliente, fecha, hora, id_sucursal, id_cita_a_modificar):
    conexion = obtener_conexion()
    id_cliente = str(id_cliente)
    id_sucursal = str(id_sucursal)
    if id_cita_a_modificar is None:
        query = "SELECT id_cita FROM cita WHERE id_cliente=" + id_cliente + " AND id_sucursal=" + id_sucursal + " AND fecha='" + fecha + "' AND hora<='" + hora + "' AND hora_fin>'" + hora + "'"
    else:

        query = "SELECT id_cita FROM cita WHERE id_cliente=" + id_cliente + " AND id_sucursal=" + id_sucursal + " AND fecha='" + fecha + "' AND hora<='" + hora + "' AND hora_fin>'" + hora + "' AND NOT id_cita="+id_cita_a_modificar
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def estilista_esta_ocupado(id_estilista, hora, fecha):
    conexion = obtener_conexion()
    query = "SELECT * FROM cita C, cita_servicio CS WHERE C.id_cita=CS.id_cita AND C.fecha='" + fecha + "' AND CS.hora_inicio<='" + hora + "' AND CS.hora_fin>'" + hora + "' AND CS.id_estilista=" + str(id_estilista)
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True


def get_info_usuario(id_usuario):
    conexion = obtener_conexion()
    query = "SELECT id_usuario, nombre, apellido_paterno, apellido_materno, correo, telefono, tipo_usuario FROM usuario WHERE id_usuario="+str(id_usuario)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]


def update_usuario(id_usuario,nombre,apellido1,apellido2,correo,telefono,tipo_usuario):
    conexion = obtener_conexion()
    query = "UPDATE usuario SET nombre = %s, apellido_paterno= %s, apellido_materno = %s, correo= %s, telefono= %s, tipo_usuario= %s WHERE id_usuario = %s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (nombre,apellido1,apellido2,correo,telefono,tipo_usuario,id_usuario))
    conexion.commit()
    conexion.close()


def get_correo_de_usuario(id_usuario):
    conexion = obtener_conexion()
    query = "SELECT correo FROM usuario WHERE id_usuario="+str(id_usuario)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['correo']
def get_lista_citas_fechas(fecha1, fecha2) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT a.id_cita, a.fecha, u.nombre as cliente, a.monto, a.iva, a.total FROM cita a, usuario u WHERE (DATE(fecha) BETWEEN %s and %s) and u.id_usuario=a.id_cliente",
            (fecha1, fecha2))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista


def get_lista_usuarios_fechas(fecha1, fecha2) -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_usuario, correo, nombre,telefono, tipo_usuario FROM usuario WHERE (fecha_creacion BETWEEN %s and %s) and tipo_usuario = 'cliente'", (fecha1, fecha2))
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_lista_serv_de_citas() -> list:
    conexion = obtener_conexion()
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cita_servicio a, servicio s WHERE a.id_servicio=s.id_servicio")
        lista = cursor.fetchall()

    conexion.commit()
    conexion.close()
    return lista

def get_suma_citas(fecha1, fecha2):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT SUM(total), SUM(iva), SUM(monto) FROM cita WHERE (DATE(fecha) BETWEEN %s and %s)",
                       (fecha1, fecha2))
        atencion = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return atencion

def get_datos_grafica_diaria(fecha) -> dict:
    dict = {}
    for hora in range(7,20):
        tiempos=[str(hora)+":00",str(hora)+":30"]
        for tiempo in tiempos:
            datos = get_valores_tabla_diaria(tiempo,fecha)
            hora = str(hora)+":00"
            if datos['suma'] is None:
                dict[tiempo]= 0
            else:
                dict[tiempo]=float(datos['suma'])
    return dict

def get_valores_tabla_diaria(hora,fecha): #1-5
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sum(total) as suma FROM cita WHERE DATE(fecha)=%s AND hora=%s", (fecha,hora))
        valores = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return valores
def get_cliente_que_agendo_cita(id_cita):
    conexion = obtener_conexion()
    query = "SELECT id_cliente FROM cita WHERE id_cita=" + str(id_cita)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['id_cliente']


def get_sucursal_de_cita(id_cita):
    conexion = obtener_conexion()
    query = "SELECT id_sucursal FROM cita WHERE id_cita=" + str(id_cita)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['id_sucursal']


def delete_cita(id_cita):
    conexion = obtener_conexion()
    query = "DELETE FROM cita WHERE id_cita="+id_cita
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)

    conexion.commit()
    conexion.close()



def get_fecha_hora_de_cita(id_cita):
    conexion = obtener_conexion()
    query = "SELECT DATE_FORMAT(fecha, '%d/%m/%Y') as fecha, DATE_FORMAT(hora, '%H:%i') as hora FROM cita WHERE id_cita=" + str(id_cita)
    lista = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        lista = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return lista[0]['fecha'], lista[0]['hora']


def cita_existe(id_cita):
    conexion = obtener_conexion()
    query = "SELECT id_cita FROM cita WHERE id_cita="+str(id_cita)
    with conexion.cursor() as cursor:
        cursor.execute(query)
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True

if __name__ == '__main__':
    print('hola')
