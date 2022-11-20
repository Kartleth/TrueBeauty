from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort
from passlib.hash import sha256_crypt
from bd import *
from usuarios import *
from dicc_menu import *
from funciones import *
from random import randint
from herramientas import *

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'

diccionario_menu = get_dicc_menu()


# dicc_lista_servicios_sel = {}

@app.context_processor
def handle_context():
    """Controla lo información mostrada dependiendo de si el usuario esta logeado y sus permisos"""
    if 'logeado' in session.keys():
        if session['logeado']:
            accesos = diccionario_menu[session['tipo']]

            # return render_template("index.html", accesos=accesos, log=['Log Out', '/logout'], usuario=usuario)
            return {'accesos': accesos, 'logeado': 'yes'}
        else:
            return {'logeado': 'no'}
    else:
        return {'logeado': 'no'}


@app.route('/login', methods=['GET', 'POST'])
def inicio_sesion():
    """
    Este método sirve para checar si el usuario que se quiere
    logear exista en la base de datos
    """
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']
        if usuario_existe('correo', correo):
            usr = get_usuario('correo', correo)
            # password = sha256_crypt.encrypt(str(password))
            if sha256_crypt.verify(password, usr['contrasenia']):
                session['id_usuario'] = usr['id_usuario']
                session['nombre'] = usr['nombre']
                session['correo'] = usr['correo']
                session['logeado'] = True
                session['tipo'] = usr['tipo_usuario']
                return redirect("/")
            else:
                mensaje = 'Contraseña incorrecta'
                flash(mensaje)
                return render_template("login.html")
        else:
            mensaje = 'Ese correo o usuario no esta registrado'
            flash(mensaje)
            return render_template("login.html")


@app.route("/logout", methods=['GET'])
def logout():
    """Cierra la sesión del usuario borrando el dicc session y lo redirige a index"""
    session.clear()
    return redirect("/")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'logeado' not in session.keys():
        if request.method == 'GET':
            return render_template("signup.html")
        elif request.method == 'POST':
            correo = request.form['correo']
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido1']
            apellido_materno = request.form['apellido2']
            password = request.form['password1']
            password2 = request.form['password2']
            telefono = request.form['telefono']
            tipo_usuario = 'cliente'
            if usuario_existe('correo', correo):
                flash('El correo pertence a otro usuario existente')
                return render_template("signup.html")
            if password != password2:
                flash('Contraseñas no concuerdan, intente de nuevo')
                return render_template("signup.html")
            else:

                insertar_usuario(nombre, apellido_paterno, apellido_materno, correo, sha256_crypt.hash(password),
                                 telefono, tipo_usuario)
                return redirect('/login')
    else:
        return redirect("/")


@app.route('/error')
def error():
    return render_template("error.html")

@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    """Controla restablecer contraseña.
    Se asegura que no haya una sesion iniciada.
    Se confirma que el usuario exista y se envia un codigo de recuperación.
    Se redirige a reset_code"""
    if 'logeado' not in session.keys():
        if request.method == 'GET':
            return render_template("forgot_password.html")
        elif request.method == 'POST':
            correo = request.form['correo']
            usr = get_usuario('correo', correo)
            if usuario_existe('correo', correo):
                correo = usr['correo']
                mensaje = f'Se envió un código para cambiar la contraseña a su correo ({correo})'
                codigo = ''
                for i in range(4):
                    numero = randint(0, 9)
                    codigo += str(numero)
                session['usuario_codigo'] = usr['correo']
                session['codigo'] = codigo
                # MANDAR CODIGO POR CORREO DE LA PERSONA
                mandar_correo_codigo('petvetreal@gmail.com', usr['correo'], 'aozykokpzeaqcnzv', codigo)
                flash(mensaje)
                return redirect('/reset_code')
            else:
                mensaje = 'El correo o usuario no está registrado'
                flash(mensaje)
                return render_template("forgot_password.html")
    else:
        return redirect("/")


@app.route("/reset_code", methods=['GET', 'POST'])
def reset_code():
    """ Se asegura que el codigo sea correcto.1|
    Se redirige para cambiar contraseña a '/new_password'"""
    if 'logeado' not in session.keys():
        if request.method == 'GET':
            return render_template('reset_code.html')
        elif request.method == 'POST':
            codigo_usuario = request.form['codigo']
            username = session['usuario_codigo']
            codigo = session['codigo']
            if codigo_usuario == codigo:
                return redirect('/new_password')
            else:
                mensaje = 'Codigo Incorrecto, pruebe de nuevo'
                flash(mensaje)
                return render_template('reset_code.html')
    else:
        return redirect("/")


@app.route("/new_password", methods=['GET', 'POST'])
def new_password():
    """Permite al usuario introducir su nueva contraseña.
    Si las dos coiciden se guardan los camnios.
    Se redirige a '/password_changed'"""
    if 'logged_in' not in session.keys():
        if request.method == 'GET':
            return render_template("new_password.html")
        elif request.method == 'POST':
            password1 = request.form['password1']
            password2 = request.form['password2']
            usr = get_usuario('correo', session['usuario_codigo'])
            if password1 == password2:
                # cambiar contraseña
                nueva_contraseña = sha256_crypt.hash(password1)
                actualizar_usuario(usr['id_usuario'], 'contrasenia', nueva_contraseña)
                return redirect('/login')
            else:
                mensaje = 'Contraseñas no concuerdan, intente de nuevo'
                flash(mensaje)
                return render_template("new_password.html")
    else:
        return redirect("/")


@app.route('/')
def inicio():
    return render_template("inicio.html")


@app.route('/inicio_cliente')
def inicio_cliente():
    return render_template("inicio_cliente.html")


@app.route('/registrar_servicio')
def registrar_servicio():
    return render_template("registrar_servicio.html")


@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    # if 'logeado' in session.keys():
    #     if session['logeado']:
    #         if session['tipo']!='estilista':
    #             if request.method == 'GET':
    #
    #
    # else:
    #     return redirect('/')

    return render_template("agendar_cita.html")


@app.route('/escoger_cita', methods=['GET', 'POST'])
def escoger_cita():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if request.method == 'GET':
                    fecha = get_cur_datetime()
                    return render_template('escoger_cita.html',
                                           lista_sucursales=get_lista_sucursales(),
                                           lista_servicios=get_lista_servicios(),
                                           date_min=fecha['fecha_actual'],
                                           date_max=fecha['fecha_fin'])
                elif request.method == 'POST':
                    id_sucursal = request.form['tipo_sucursal']
                    fecha = request.form['fecha']
                    session['lista_servicios_sel'] = obtener_servicios(request.form.to_dict())

                    return redirect(url_for('hora_cita', id_sucursal=id_sucursal, fecha=fecha))
                else:
                    return redirect('/')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/fecha_cita')
def fecha_cita():
    return render_template("fecha_cita.html")


@app.route('/hora_cita', methods=['GET', 'POST'])
def hora_cita():
    if 'logeado' in session.keys():
        if session['logeado']:

            id_sucursal = request.args['id_sucursal']
            fecha = request.args['fecha']

            lista_horas_disponibles = get_horas_disponibles(id_sucursal, fecha, session['lista_servicios_sel'])

            if request.method == 'GET':
                if lista_horas_disponibles is None:
                    return redirect('/escoger_cita')
                else:
                    return render_template("hora_cita.html", horas_disponibles=lista_horas_disponibles)
            elif request.method == 'POST':
                hora = request.form['hora']

                return redirect(url_for('confirmar_cita', fecha=fecha, id_sucursal=id_sucursal, hora=hora))

        else:
            return redirect('/')
    else:
        return redirect('/')
    return render_template("hora_cita.html")


@app.route('/confirmar_cita', methods=['GET', 'POST'])
def confirmar_cita():
    if 'logeado' in session.keys():

        if session['logeado']:
            if 'id_sucursal' in request.args.keys() or 'fecha' in request.args.keys() or 'hora' in request.args.keys():
                id_sucursal = request.args['id_sucursal']
                fecha = request.args['fecha']
                hora = request.args['hora']

                if request.method == 'GET':
                    dicc_info_cita = crear_dicc_info_cita(id_sucursal, fecha, hora, session['lista_servicios_sel'])
                    return render_template('confirmar_cita.html', info_cita=dicc_info_cita)
                elif request.method == 'POST':
                    fecha = request.form['fecha']
                    id_sucursal = request.form['id_sucursal']
                    hora = request.form['hora']

                    monto = request.form['monto']
                    print(fecha, hora, id_sucursal, monto)
                    guardar_cita(fecha, hora, session['id_usuario'], id_sucursal, monto, session['lista_servicios_sel'])

                    session.pop('lista_servicios_sel')
                    return redirect('/consultar_citas')
            else:
                return redirect('/escoger_cita')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/ver_cita_gerente_recepcionista')
def ver_cita_gerente_recepcionista():
    return render_template("consultar_citas_gerente_recepcionista.html")


@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")


@app.route('/consultar_servicios')
def consultar_servicios():
    if 'logeado' in session.keys():
        if session['logeado']:
            servicios = get_lista_servicios()
            return render_template('consultar_servicios.html', lista_servicios=servicios, tipo_usuario=session['tipo'])
    else:

        return redirect('/')


@app.route('/consultar_citas')
def consultar_citas():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'cliente' or session['tipo'] == 'estilista':
                citas = get_lista_info_citas_usuario('id_' + session['tipo'], session['id_usuario'])
                return render_template("consultar_citas.html", lista_citas=citas)
            elif session['tipo'] == 'recepcionista' or session['tipo'] == 'gerente':
                lista_citas = get_lista_info_citas()
                return render_template('consultar_citas_gerente_recepcionista.html', citas=lista_citas)
            else:
                return redirect('/')

    else:

        return redirect('/')



@app.route('/informacion_servicio/<id_servicio>', methods=['GET', 'POST'])
def informacion_servicio(id_servicio):
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente':
                if request.method == 'GET':
                    info_servicio = get_servicio(id_servicio)
                    if info_servicio is None:
                        return redirect('/consultar_servicios')
                    else:
                        info_servicio = info_servicio[0]

                    lista_servicios = get_lista_servicios()

                    return render_template('informacion_servicio.html', info_servicio=info_servicio,
                                           lista_servicios=lista_servicios)
                elif request.method == 'POST':
                    nombre_servicio = request.form['nombre']
                    precio = request.form['precio']
                    tiempo_duracion = request.form['tiempo']
                    descripcion = request.form['descripcion']
                    print(nombre_servicio,precio,tiempo_duracion,descripcion)
                    return redirect('/consultar_servicios')
            else:
                return redirect('consultar_servicios')
    else:
        return redirect('/')



@app.route('/informacion_cita/<id_cita>', methods=['GET', 'POST'])
def informacion_cita(id_cita):
    if session['logeado']:
        if session['tipo'] == 'cliente' or session['tipo'] == 'estilista':
            if cita_pertenece_a_usuario('id_' + str(session['tipo']), session['id_usuario'], id_cita):
                citas = get_citas_de_usuario('id_' + str(session['tipo']), session['id_usuario'])
                info_cita = get_info_cita(id_cita)
                servicios = get_lista_servicios()
                return render_template("informacion_cita.html", lista_citas=citas, dicc_cita=info_cita,
                                       lista_servicios=servicios)

            else:
                return redirect('/escoger_cita')
        else:
            info_cita = get_dicc_info_cita(id_cita)

            return render_template("info_cita_gerente_recepcionista.html", dicc_cita=info_cita)


    else:
        return redirect('/')


@app.route('/reparacion')
def reparacion():
    return render_template("reparacion.html")


# Informes se va a dividir en diaria, mensual y en rango.
""" 
@app.route("/informe_ventas/diaria", methods=['GET', 'POST'])
def informe_ventas_diario():
 Se asegura que la cuenta tenga permisos de administrador.
    Regresa el template con toda la información del sistema para mostrar su respectivo informe de ventas.
    Si se selecciona alguna fecha en especifico la información cambia dependiendo de la misma.
    if 'logged_in' in session.keys():
            if session['logeado']:
                if session['type'] == 'gerente':
                    if request.method == 'GET' :
                        horas = []
                        fecha = get_cur_datetime()
                        desde = fecha['now']
                        hasta = fecha['now']
                        citas = get_lista_citas_fechas(desde, hasta) #atenciones/citas
                        usuarios = get_lista_usuarios_fechas(desde, hasta) #crear usuarios
                        servicios = get_lista_serv_de_atenciones()  #
                        suma = get_suma_atenciones(desde, hasta)
                        total_atenciones_subtotal = suma['SUM(subtotal)']
                        total_atenciones_iva = suma['SUM(iva)']
                        total_atenciones_total = suma['SUM(total)']
                        
                        data_dict = get_datos_grafica_diaria(desde)

                        return render_template("reporte.html", lista_usuarios=usuarios,
                                            total_atenciones_subtotal=total_atenciones_subtotal,
                                            total_atenciones_iva=total_atenciones_iva,
                                            total_atenciones_total=total_atenciones_total,
                                            lista_atenciones=citas, lista_servicios=servicios,
                                            tipo='Diario', date=fecha['now'], data=json.dumps(data_dict))
    
                    if request.method == 'POST':
                        fecha = request.form['fecha']
                        citas = get_lista_citas_fechas(fecha, fecha)
                        usuarios = get_lista_usuarios_fechas(fecha, fecha)
                        servicios = get_lista_serv_de_atenciones()       
                        suma = get_suma_atenciones(fecha, fecha)
                        total_atenciones_subtotal = suma['SUM(subtotal)']
                        total_atenciones_iva = suma['SUM(iva)']
                        total_atenciones_total = suma['SUM(total)']
                        print(fecha, fecha, suma)

                        data_dict = get_datos_grafica_diaria(fecha)
                        return render_template("reporte.html", lista_usuarios=usuarios,
                                            total_atenciones_subtotal=total_atenciones_subtotal,
                                            total_atenciones_iva=total_atenciones_iva,
                                            total_atenciones_total=total_atenciones_total,
                                            lista_atenciones=citas, lista_servicios=servicios,
                                            tipo='Diario',
                                                date=fecha, data=json.dumps(data_dict))
                else:
                    abort(403)
            else:
                abort(403)
        

"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
