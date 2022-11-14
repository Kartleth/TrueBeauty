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

def obtener_horas_disponibles(id_sucursal,fecha,lista_servicios):
    lista_estilistas_de_sucursal = get_lista_estilistas_de_sucursal(id_sucursal)
    lista_horas = ['8:00','16:00','12:00']
    return lista_horas

