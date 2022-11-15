import os
import smtplib, ssl
from email.message import EmailMessage
from bd import *


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


def get_horas_disponibles(id_sucursal, fecha, lista_servicios):
    # dicc_estilistas_horas_libres = {}
    #
    # estilistas = []
    # for id_servicio in lista_servicios:
    #     estilistas.append(get_lista_estilista_por_sucursal_servicio(id_sucursal,id_servicio))
    # print(str(estilistas))

    posibles_horas_disponibles = []
    for i in range(8, 20):
        posibles_horas_disponibles.append(f"{i}:00")
        posibles_horas_disponibles.append(f"{i}:30")
    print('HORAS POSIBLES DISPONIBLES:' + str(posibles_horas_disponibles))
    horas_disponibles = []
    for hora in posibles_horas_disponibles:
        if hora_esta_disponible(hora, lista_servicios, id_sucursal, fecha):
            horas_disponibles.append(hora)

    return horas_disponibles


def hora_esta_disponible(hora, lista_servicios, id_sucursal, fecha):
    # buscar que exista estilista disponible a esa hora en esa sucursal

    for id_servicio in lista_servicios:
        if not hay_estilista_para_horayservicio(hora, id_servicio, fecha, id_sucursal):
            print(
                f"No hay estilista para la hora:{hora} para el servicio {id_servicio} para la fecha: {fecha} para la sucursal {id_sucursal}")
            return False
        else:
            if lista_servicios[-1] == id_servicio:
                return True
            else:
                hora = agregar_tiempo_de_servicio(hora, id_servicio)

    # estilistas = get_estilista_por_sucursal_servicio(id_sucursal, )
    return True


def agregar_tiempo_de_servicio(hora, id_servicio):
    hora_separada = hora.split(':')
    horas = int(hora_separada[0])
    minutos = hora_separada[1]
    hora_siguiente = ''
    if minutos[0] == '3':
        return str(horas + 1) + ':00'
    else:
        return str(horas) + ':30'


def hay_estilista_para_horayservicio(hora, id_servicio, fecha, id_sucursal) -> bool:
    estilistas = get_lista_estilista_por_sucursal_servicio(id_sucursal, id_servicio)
    for estilista in estilistas:
        if not estilista_tiene_cita(hora, estilista['id_usuario'], fecha):
            return True

    return False


def crear_dicc_info_cita(id_sucursal, fecha, hora, servicios_seleccionados) -> dict:
    dicc = {}
    lista_de_diccs_servicios = get_servs_por_lista_id(servicios_seleccionados)
    info_sucursal = get_info_sucursal(id_sucursal)

    dicc['lista_servicios'] = lista_de_diccs_servicios
    dicc['info_sucursal'] = info_sucursal
    dicc['fecha'] = fecha
    dicc['hora'] = hora
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


if __name__ == '__main__':
    print(str(get_lista_info_citas()))
    # print(get_horas_disponibles('1', '2023-10-08', ['1', '2', '3']))
    # print(hay_estilista_para_horayservicio('10:30','3','2023-10-08','1'))
    # print(estilista_tiene_cita('10:30','3','2023-10-08'))
    # print(estilista_tiene_cita('8:30', 3, '2023-10-18'))
