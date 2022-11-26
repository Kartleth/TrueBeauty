import os
import smtplib, ssl
import datetime
import time
from email.message import EmailMessage
import locale
from bd import *
import locale

locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))


def mandar_correo_codigo(sender, receiver, password, codigo):
    email_subject = 'Código de Cambio de Contraseña'
    sender_email_address = sender
    receiver_email_address = receiver
    email_smtp = "smtp.gmail.com"
    email_password = password

    # Create an email message object
    message = EmailMessage()

    # Configure email headers
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address

    # Set email body text
    message.set_content(f"Su código para cambiar su contraseña es {codigo}")

    context = ssl.create_default_context()
    # Set smtp server and port
    with smtplib.SMTP_SSL(email_smtp, 465, context=context) as smtp:
        # Login to email account
        smtp.login(sender_email_address, email_password)

        # Send email
        smtp.sendmail(sender_email_address, receiver_email_address, message.as_string())

        # Close connection to server


def obtener_servicios(dicc_form: dict) -> list:
    lista_id_servicios = []
    for llave in dicc_form.keys():
        valores = llave.split('_')
        if valores[0] == 'serv':
            lista_id_servicios.append(valores[1])
    return lista_id_servicios


def get_horas_disponibles(id_sucursal, fecha, lista_servicios, id_cliente, id_cita_a_modificar=None):
    posibles_horas_disponibles = []
    for i in range(8, 20):
        posibles_horas_disponibles.append(f"{i}:00")
        posibles_horas_disponibles.append(f"{i}:30")
    horas_disponibles = []
    for hora in posibles_horas_disponibles:
        if hora_esta_disponible(hora, lista_servicios, id_sucursal, fecha, id_cliente, id_cita_a_modificar):
            horas_disponibles.append(hora)
    horas_disponibles = quitar_horas_del_pasado(horas_disponibles,fecha)
    return horas_disponibles

def quitar_horas_del_pasado(horas_disponibles,fecha_cita):
    fecha_actual = datetime.datetime.now()
    fecha_cita = datetime.datetime.strptime(fecha_cita,'%Y-%m-%d')

    if fecha_actual >= fecha_cita:
        copia_horas_disponibles = horas_disponibles.copy()

        for hora in copia_horas_disponibles:
            hora_formateada = datetime.datetime.strptime(hora,"%H:%M").time()
            fecha_hora = datetime.datetime.combine(fecha_cita,hora_formateada)

            if fecha_hora < fecha_actual:
                horas_disponibles.remove(hora)

    return horas_disponibles


def hora_esta_disponible(hora, lista_servicios, id_sucursal, fecha, id_cliente, id_cita_a_modificar):
    # buscar que exista estilista disponible a esa hora en esa sucursal
    hora_de_termino = time.strptime(calcular_hora_fin_de_cita(hora, lista_servicios), "%H:%M")
    hora_de_cierre = time.strptime('20:00', "%H:%M")

    if cliente_ya_tiene_cita(id_cliente, fecha, hora, id_sucursal, id_cita_a_modificar):
        return False
    elif hora_de_termino > hora_de_cierre:
        return False
    else:
        for id_servicio in lista_servicios:
            if not hay_estilista_para_horayservicio(hora, id_servicio, fecha,
                                                    id_sucursal, id_cita_a_modificar) or not hay_espacio_en_estetica(id_sucursal, fecha,
                                                                                                hora, id_cita_a_modificar):
                return False
            else:
                if lista_servicios[-1] == id_servicio:
                    return True
                else:
                    hora = calcular_tiempo_hora_servicio(id_servicio, hora)

    # estilistas = get_estilista_por_sucursal_servicio(id_sucursal, )
    return True


def hay_estilista_para_horayservicio(hora, id_servicio, fecha, id_sucursal, id_cita_a_modificar) -> bool:
    estilistas = get_lista_estilista_por_sucursal_servicio(id_sucursal, id_servicio)

    for estilista in estilistas:
        if not estilista_tiene_cita(hora, estilista['id_usuario'], fecha,
                                    calcular_tiempo_hora_servicio(id_servicio, hora), id_cita_a_modificar):
            return True

    return False


def hay_espacio_en_estetica(id_sucursal, fecha, hora, id_cita_a_modificar):
    asientos_en_sucursal = get_asientos_de_sucursal(id_sucursal)
    asientos_ocupados = get_asientos_ocupados_de_sucursal(id_sucursal, fecha, hora, id_cita_a_modificar)
    if asientos_ocupados >= asientos_en_sucursal:
        return False
    else:
        return True


def crear_dicc_info_cita(id_sucursal, fecha, hora, servicios_seleccionados) -> dict:
    dicc = {}
    lista_de_diccs_servicios = get_servs_por_lista_id(servicios_seleccionados)
    info_sucursal = get_info_sucursal(id_sucursal)

    dicc['lista_servicios'] = lista_de_diccs_servicios
    dicc['info_sucursal'] = info_sucursal
    dicc['fecha'] = fecha
    dicc['hora'] = hora
    dicc['monto'] = float(calcular_monto(servicios_seleccionados)['precio'])
    return dicc


def get_lista_info_citas():
    lista_citas = get_lista_citas()
    lista_de_diccs_citas = []
    dicc_cita = {}
    for cita in lista_citas:
        dicc_cita['id_cita'] = cita['id_cita']
        dicc_cita['nombre_completo'] = cita['nombre'] + " " + cita['apellido_paterno'] + " " + cita['apellido_materno']
        dicc_cita['fecha'] = cita['fecha']
        dicc_cita['hora'] = cita['hora']
        dicc_cita['monto'] = cita['monto']
        dicc_cita['nombre_sucursal'] = cita['nombre_sucursal']
        lista_de_diccs_citas.append(dicc_cita.copy())

    return lista_de_diccs_citas


def get_lista_info_citas_usuario(columna: str, id_usuario: int):
    lista_citas = get_citas_de_usuario(columna, id_usuario)
    lista_de_diccs_citas = []
    dicc_cita = {}
    for cita in lista_citas:
        dicc_cita['id_cita'] = cita['id_cita']
        dicc_cita['fecha'] = cita['fecha']
        dicc_cita['hora'] = cita['hora']

        dicc_cita['lista_servicios'] = get_nombre_servicios_de_cita(cita['id_cita'])
        lista_de_diccs_citas.append(dicc_cita.copy())
    return lista_de_diccs_citas


def guardar_cita(fecha, hora, id_usuario, id_sucursal, monto, lista_servicios):
    subtotal = float(monto)
    iva = subtotal * 0.16
    total = subtotal + iva
    c = 0
    hora2 = hora

    for servicio in lista_servicios:
        # aumento = datetime.timedelta(minutes=int(tiempo_servicio))
        # hora = datetime.datetime.strptime(hora, "%H:%M")
        # hora_fin = aumento + hora
        # hora_fin = hora_fin.strftime("%H:%M")
        # hora = hora.strftime("%H:%M")
        # hora = hora_fin
        hora_fin = calcular_tiempo_hora_servicio(servicio, hora2)
        c += 1
        hora2 = hora_fin
    id_cita = insert_into_cita(fecha, hora, hora_fin, id_usuario, id_sucursal, monto, iva, total)
    guardar_servicios_de_cita(lista_servicios, hora, fecha, id_sucursal, id_cita)


def guardar_servicios_de_cita(lista_servicios, hora, fecha, id_sucursal, id_cita):
    for servicio in lista_servicios:
        id_estilista = get_estilista_apropiado(servicio, hora, fecha, id_sucursal)

        tiempo_servicio = get_tiempo_servicio(servicio)
        aumento = datetime.timedelta(minutes=int(tiempo_servicio))

        hora = datetime.datetime.strptime(hora, "%H:%M")
        hora_fin = aumento + hora
        hora_fin = hora_fin.strftime("%H:%M")
        hora = hora.strftime("%H:%M")
        insert_into_cita_servicio(id_cita, servicio, id_estilista, hora, hora_fin)
        hora = hora_fin


def calcular_tiempo_hora_servicio(id_servicio, hora):
    tiempo_servicio = get_tiempo_servicio(id_servicio)
    aumento = datetime.timedelta(minutes=int(tiempo_servicio))

    hora = datetime.datetime.strptime(hora, "%H:%M")
    hora_fin = aumento + hora
    hora_fin = hora_fin.strftime("%H:%M")
    hora = hora.strftime("%H:%M")
    return hora_fin


def get_dicc_info_cita(id_cita):
    dicc_cita = get_info_cita(id_cita)
    hora_formateada = datetime.datetime.strptime(dicc_cita['hora'], '%H:%M').time()
    fecha_formateada = datetime.datetime.strptime(dicc_cita['fecha'], '%d/%m/%Y')
    dicc_cita['fecha_hora'] = datetime.datetime.combine(fecha_formateada,hora_formateada)
    dicc_cita['lista_servicios'] = get_lista_info_servicios(id_cita)
    dicc_cita['lista_id_servicios'] = get_lista_id_servicios_de_cita(id_cita)
    return dicc_cita


def agregar_fechas_en_formato_datetime(citas):
    for cita in citas:
        hora_formateada = datetime.datetime.strptime(cita['hora'],'%H:%M').time()
        fecha_formateada = datetime.datetime.strptime(cita['fecha'], '%d/%m/%Y')
        cita['fecha_datetime'] = datetime.datetime.combine(fecha_formateada,hora_formateada)
        cita['fecha_escrita'] = cita['fecha_datetime'].strftime('%d de %B de %Y')
    return citas


def calcular_hora_fin_de_cita(hora_de_inicio, lista_servicios):
    hora_de_termino = hora_de_inicio
    for servicio in lista_servicios:
        hora_de_termino = calcular_tiempo_hora_servicio(servicio, hora_de_termino)
    return hora_de_termino


def formatear_fecha_para_input(fecha):
    fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
    fecha = fecha.strftime('%Y-%m-%d')
    return fecha


def get_estilista_apropiado(id_servicio, hora, fecha, id_sucursal):
    posibles_estilistas = get_posibles_estilistas(id_sucursal, id_servicio)
    estilistas_desocupados = []
    for estilista in posibles_estilistas:
        if not estilista_esta_ocupado(estilista, hora, fecha):
            estilistas_desocupados.append(estilista)
    return estilistas_desocupados[0]


def cita_ya_paso(id_cita):
    fecha,hora = get_fecha_hora_de_cita(id_cita)
    hora_formateada = datetime.datetime.strptime(hora, '%H:%M').time()
    fecha_formateada = datetime.datetime.strptime(fecha, '%d/%m/%Y')
    fecha_hora_cita = datetime.datetime.combine(fecha_formateada, hora_formateada)
    if fecha_hora_cita < datetime.datetime.now():
        return True
    else:
        return False

if __name__ == '__main__':
    horas_salida = datetime.timedelta(minutes=180)
    h1 = datetime.datetime.strptime('10:30', "%H:%M")

    hora_fin = h1 + horas_salida
    print(hora_fin)

    # print(str(get_lista_info_citas_usuario('id_cliente', 1)))
    # print(get_horas_disponibles('1', '2023-10-08', ['1', '2', '3']))
    # print(hay_estilista_para_horayservicio('10:30','3','2023-10-08','1'))
    # print(estilista_tiene_cita('10:30','3','2023-10-08'))
    # print(estilista_tiene_cita('8:30', 3, '2023-10-18'))
