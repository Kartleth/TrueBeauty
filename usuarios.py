from bd import obtener_conexion


def insertar_usuario(nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario):
    conexion = obtener_conexion()
    nombre = nombre.title()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuario (nombre,apellido_paterno,apellido_materno,correo,contrasenia,telefono,tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario))
    conexion.commit()
    conexion.close()


def actualizar_usuario(user_id: str, column: str, cambio: str):
    conexion = obtener_conexion()
    query = "UPDATE usuario SET " + column + " = %s WHERE id_usuario = %s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (cambio, user_id))
    conexion.commit()
    conexion.close()


def eliminar_usuario(user_id: str):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuario WHERE user_id=%s",
                       (user_id))
    conexion.commit()
    conexion.close()


def get_usuario(column: str, valor: str):
    conexion = obtener_conexion()
    query = "SELECT * FROM usuario WHERE " + column + "=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        usuario = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return usuario


def usuario_existe(column: str, valor: str):
    conexion = obtener_conexion()
    query = "SELECT * FROM usuario WHERE " + column + "=%s"
    with conexion.cursor() as cursor:
        cursor.execute(query, (valor))
        if cursor.fetchone() is None:
            return False
    conexion.commit()
    conexion.close()
    return True
