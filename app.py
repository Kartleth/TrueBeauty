from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort
from passlib.hash import sha256_crypt
from bd import *
from usuarios import *
from dicc_menu import *
from funciones import *
from random import randint
from herramientas import *
from datetime import datetime
import json 

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
            if usuario_existe('correo', correo):
                flash('El correo pertence a otro usuario existente')
                #return render_template("signup.html")
                return redirect('/signup')
            password = request.form['password1']
            password2 = request.form['password2']

            if password != password2:
                flash('Contraseñas no concuerdan, intente de nuevo')
                return render_template("signup.html")
            else:
                nombre = request.form['nombre']
                apellido_paterno = request.form['apellido1']
                apellido_materno = request.form['apellido2']            

                telefono = request.form['telefono']
                tipo_usuario = 'cliente'
                # insertar_usuario(nombre, apellido_paterno, apellido_materno, correo, sha256_crypt.hash(password),
                #                  telefono, tipo_usuario)               
                mensaje = f'Se envió un código de confirmación a su correo a ({correo})'
                codigo = ''
                for i in range(4):
                    numero = randint(0, 9)
                    codigo += str(numero)
                session['usuario_codigo'] = correo
                session['codigo'] = codigo
                # MANDAR CODIGO POR CORREO DE LA PERSONA
                mandar_correo_codigo('petvetreal@gmail.com', correo, 'aozykokpzeaqcnzv', codigo)            
                flash(mensaje)
                session['bool']=True
                session['nombre']=nombre 
                session['apellido_paterno']=apellido_paterno
                session['apellido_materno']=apellido_materno
                session['password']=password
                session['telefono']=telefono
                session['tipo_usuario']=tipo_usuario
                
                return redirect('/reset_code')
                
    else:
        return redirect("/")
    

@app.route('/confirmar_correo', methods=['GET','POST'])
def confirmar_correo():  
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
                session['bool']= False
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
            if codigo_usuario == codigo and session['bool']==False:
                return redirect('/new_password')
            elif codigo_usuario == codigo and session['bool']:
                insertar_usuario(session['nombre'], session['apellido_paterno'], session['apellido_materno'], username, sha256_crypt.hash(session['password']),
                                  session['telefono'], session['tipo_usuario']) 
                return redirect('/login')
            
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


@app.route('/escoger_cita/', methods=['GET', 'POST'])
@app.route('/escoger_cita/<int:id_cliente>', methods=['GET', 'POST'])
def escoger_cita(id_cliente=None):
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if request.method == 'GET':
                    if id_cliente is None:
                        if session['tipo'] != 'cliente':
                            flash('Primero escoga o cree un usuario para agendar una cita:')
                            return redirect('/consultar_clientes')
                        else:
                            fecha = get_cur_datetime()
                            return render_template('escoger_cita.html',
                                                   lista_sucursales=get_lista_sucursales(),
                                                   lista_servicios=get_lista_servicios(),
                                                   date_min=fecha['now'],#date_min=fecha['fecha_actual'],
                                                   date_max=fecha['fecha_fin'])
                    elif session['tipo'] == 'cliente':
                        return redirect('/escoger_cita')
                    else:
                        session['id_cliente'] = str(id_cliente)
                        fecha = get_cur_datetime()
                        return render_template('escoger_cita.html',
                                               lista_sucursales=get_lista_sucursales(),
                                               lista_servicios=get_lista_servicios(),
                                               date_min=fecha['now'],#fecha['fecha_actual'],
                                               date_max=fecha['fecha_fin'])
                elif request.method == 'POST':
                    id_sucursal = request.form['tipo_sucursal']
                    fecha = request.form['fecha']

                    session['lista_servicios_sel'] = obtener_servicios(request.form.to_dict())
                    if len(session['lista_servicios_sel']) == 0:
                        flash('Por favor, seleccione algún servicio para continuar')
                        if id_cliente is None:
                            return redirect('/escoger_cita')
                        else:
                            return redirect('/escoger_cita/' + str(id_cliente))

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
            if 'id_sucursal' in request.args.keys() and 'fecha' in request.args.keys():
                id_sucursal = request.args['id_sucursal']
                fecha = request.args['fecha']

                if 'id_cliente' in session.keys():
                    id_cliente = session['id_cliente']
                else:
                    id_cliente = session['id_usuario']
                lista_horas_disponibles = get_horas_disponibles(id_sucursal, fecha, session['lista_servicios_sel'],
                                                                id_cliente)

                if request.method == 'GET':
                    if len(lista_horas_disponibles) == 0:
                        flash(
                            'No hay horas disponibles con esos requerimientos. Por favor, escoge otra fecha, otra sucursal u otros servicios.' + str(
                                lista_horas_disponibles))
                        if 'id_cliente' in session.keys():
                            return redirect('/escoger_cita/' + session['id_cliente'])
                        else:
                            return redirect('/escoger_cita')
                    else:
                        return render_template("hora_cita.html", horas_disponibles=lista_horas_disponibles)
                elif request.method == 'POST':
                    hora = request.form['hora']

                    return redirect(url_for('confirmar_cita', fecha=fecha, id_sucursal=id_sucursal, hora=hora))
            elif 'id_cliente' in session.keys():
                flash('Por favor, primero llene estos campos para escoger la hora')

                return redirect('/escoger_cita/' + session['id_cliente'])
            else:
                flash('Por favor, primero llene estos campos para escoger la hora')
                return redirect('/escoger_cita')
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
                    dicc_info_cita['iva'] = round(dicc_info_cita['monto'] * 0.16, 2)
                    dicc_info_cita['total'] = round(dicc_info_cita['iva'] + dicc_info_cita['monto'], 2)
                    if 'id_cliente' in session.keys():
                        dicc_info_cliente = get_info_cliente(session['id_cliente'])
                        return render_template('confirmar_cita.html', info_cita=dicc_info_cita,
                                               info_cliente=dicc_info_cliente)
                    else:
                        return render_template('confirmar_cita.html', info_cita=dicc_info_cita)
                elif request.method == 'POST':
                    fecha = request.form['fecha']
                    id_sucursal = request.form['id_sucursal']
                    hora = request.form['hora']

                    monto = request.form['monto']
                    if 'id_cliente' in session.keys():
                        id_cliente = session['id_cliente']
                        session.pop('id_cliente')
                    else:
                        id_cliente = session['id_usuario']

                    guardar_cita(fecha, hora, id_cliente, id_sucursal, monto, session['lista_servicios_sel'])

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
            if session['tipo'] == 'cliente':
                citas = get_lista_info_citas_usuario('id_' + session['tipo'], session['id_usuario'])
                return render_template("consultar_citas.html", lista_citas=citas)
            elif session['tipo'] == 'estilista':
                servicios_programados = get_citas_de_estilista(session['id_usuario'])
                return render_template('consultar_citas_de_estilista.html', servicios_programados=servicios_programados)

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
                    print(nombre_servicio, precio, tiempo_duracion, descripcion)
                    update_servicio(id_servicio, nombre_servicio, precio, descripcion, tiempo_duracion)
                    return redirect('/consultar_servicios')
            else:
                return redirect('consultar_servicios')
    else:
        return redirect('/')


@app.route('/agregar_servicio', methods=['GET', 'POST'])
def agregar_servicio():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente':
                if request.method == 'GET':
                    return render_template('registrar_servicio.html')
                elif request.method == 'POST':
                    nombre = request.form['nombre']
                    precio = request.form['precio']
                    tiempo = request.form['tiempo']
                    descripcion = request.form['descripcion']
                    print(str(request.form.to_dict()))
                    if hay_servicio_con_ese_nombre(nombre):
                        flash('Ya existe un servicio con ese nombre.')
                        return redirect('/agregar_servicio')
                    insert_into_servicio(nombre, precio, descripcion, tiempo)
                    return redirect('/consultar_servicios')

        else:
            return redirect('/')
    else:
        return redirect('/')
    return render_template('registrar_servicio.html')


@app.route('/informacion_cita/<id_cita>', methods=['GET', 'POST'])
def informacion_cita(id_cita):
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if not cita_existe(id_cita):
                    return redirect('/consultar_citas')
                fecha_actual = datetime.now()
                if session['tipo'] == 'cliente':
                    if cita_pertenece_a_usuario('id_' + str(session['tipo']), session['id_usuario'], id_cita):

                        citas = get_citas_de_usuario('id_' + str(session['tipo']), session['id_usuario'])
                        citas = agregar_fechas_en_formato_datetime(citas)
                        info_cita = get_dicc_info_cita(id_cita)

                        return render_template("informacion_cita.html", lista_citas=citas, dicc_cita=info_cita,
                                               fecha_actual=fecha_actual)

                    else:
                        return redirect('/consultar_citas')
                else:
                    info_cita = get_dicc_info_cita(id_cita)

                    return render_template("info_cita_gerente_recepcionista.html", dicc_cita=info_cita, fecha_actual=fecha_actual)
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/modificar_cita/<id_cita>', methods=['GET', 'POST'])
def modificar_cita(id_cita):
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if not cita_existe(id_cita):
                    return redirect('/consultar_citas')
                if request.method == 'GET':

                    if cita_ya_paso(id_cita):
                        flash('No puedes modificar citas que ya pasaron')
                        return redirect('/informacion_cita/'+str(id_cita))

                    if session['tipo'] == 'recepcionista' or session['tipo'] == 'gerente':
                        fecha = get_cur_datetime()
                        info_cita = get_dicc_info_cita(id_cita)
                        info_cita['fecha'] = formatear_fecha_para_input(info_cita['fecha'])
                        return render_template('modificar_cita.html', info_cita=info_cita,
                                               lista_sucursales=get_lista_sucursales(),
                                               lista_servicios=get_lista_servicios(),
                                               date_min=fecha['now'],#fecha['fecha_actual'],
                                               date_max=fecha['fecha_fin'])
                    else:
                        if cita_pertenece_a_usuario('id_cliente', session['id_usuario'], id_cita):
                            fecha = get_cur_datetime()
                            info_cita = get_dicc_info_cita(id_cita)
                            info_cita['fecha'] = formatear_fecha_para_input(info_cita['fecha'])
                            return render_template('modificar_cita.html', info_cita=info_cita,
                                                   lista_sucursales=get_lista_sucursales(),
                                                   lista_servicios=get_lista_servicios(),
                                                   date_min=fecha['now'],#fecha['fecha_actual'],
                                                   date_max=fecha['fecha_fin'])
                        else:
                            return redirect('/consultar_citas')

                elif request.method == 'POST':

                    session['lista_servicios_sel'] = obtener_servicios(request.form.to_dict())
                    if len(session['lista_servicios_sel']) == 0:
                        flash('Por favor, seleccione algún servicio para continuar')

                        return redirect('modifcar_cita/' + str(id_cita))
                    id_sucursal = request.form['tipo_sucursal']
                    fecha = request.form['fecha']
                    id_cliente = get_cliente_que_agendo_cita(id_cita)
                    return redirect(url_for('modificar_hora_cita', id_sucursal=id_sucursal, fecha=fecha, id_cliente=id_cliente, id_cita=id_cita))
                else:
                    return redirect('/')

            else:
                return redirect('/')

        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/modificar_hora_cita', methods=['GET', 'POST'])
def modificar_hora_cita():
    if 'logeado' in session.keys():
        if session['logeado']:
            if 'id_sucursal' in request.args.keys() and 'fecha' in request.args.keys() and 'id_cliente' in request.args.keys() and 'id_cita' in request.args.keys():
                id_sucursal = int(request.args['id_sucursal'])
                fecha = request.args['fecha']
                id_cliente = str(request.args['id_cliente'])
                id_cita = str(request.args['id_cita'])
                if id_sucursal == int(get_sucursal_de_cita(id_cita)):
                    lista_horas_disponibles = get_horas_disponibles( str(id_sucursal), fecha, session['lista_servicios_sel'],id_cliente,id_cita)
                else:
                    lista_horas_disponibles = get_horas_disponibles(str(id_sucursal),fecha,session['lista_servicios_sel'],id_cliente)

                if request.method == 'GET':
                    if len(lista_horas_disponibles) == 0:
                        flash(
                            'No hay horas disponibles con esos requerimientos. Por favor, escoge otra fecha, otra sucursal u otros servicios.' + str(
                                lista_horas_disponibles))

                        return redirect('/modificar_cita/' + id_cita)

                    else:
                        return render_template("hora_cita.html", horas_disponibles=lista_horas_disponibles)
                elif request.method == 'POST':
                    hora = request.form['hora']

                    return redirect(url_for('confirmar_cambios_cita', fecha=fecha, id_sucursal=id_sucursal, hora=hora, id_cliente=id_cliente,id_cita=id_cita))

            else:
                flash('Por favor, primero escoga la cita que quiere modificar')
                return redirect('/consultar_citas')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/confirmar_cambios_cita', methods=['GET', 'POST'])
def confirmar_cambios_cita():
    if 'logeado' in session.keys():

        if session['logeado']:
            if 'id_sucursal' in request.args.keys() or 'fecha' in request.args.keys() or 'hora' in request.args.keys() and 'id_cliente' in request.args.keys() and 'id_cita' in request.args.keys():
                id_sucursal = request.args['id_sucursal']
                fecha = request.args['fecha']
                hora = request.args['hora']
                id_cliente = str(request.args['id_cliente'])
                id_cita = str(request.args['id_cita'])

                if request.method == 'GET':
                    dicc_info_cita = crear_dicc_info_cita(id_sucursal, fecha, hora, session['lista_servicios_sel'])
                    dicc_info_cita['iva'] = round(dicc_info_cita['monto'] * 0.16, 2)
                    dicc_info_cita['total'] = round(dicc_info_cita['iva'] + dicc_info_cita['monto'], 2)

                    dicc_info_cliente = get_info_cliente(id_cliente)
                    return render_template('confirmar_cita.html', info_cita=dicc_info_cita,
                                           info_cliente=dicc_info_cliente)

                elif request.method == 'POST':
                    fecha = request.form['fecha']
                    id_sucursal = str(request.form['id_sucursal'])
                    hora = request.form['hora']

                    monto = request.form['monto']

                    delete_cita(id_cita)
                    guardar_cita(fecha, hora, id_cliente, id_sucursal, monto, session['lista_servicios_sel'])

                    session.pop('lista_servicios_sel')
                    return redirect('/consultar_citas')
            else:
                return redirect('/consultar_citas')
        else:
            return redirect('/')
    else:
        return redirect('/')





@app.route('/info_cuenta/', methods=['GET', 'POST'])
@app.route('/info_cuenta/<int:id_usuario>', methods=['GET', 'POST'])
def info_cuenta(id_usuario=None):
    if 'logeado' in session.keys():
        if session['logeado']:
            if request.method == 'GET':
                if id_usuario is None:
                    id_usuario = session['id_usuario']
                if session['tipo'] == 'estilista' or session['tipo'] == 'cliente':
                    dicc_usuario = get_info_usuario(session['id_usuario'])
                    print(str(dicc_usuario))
                    return render_template('informacion_usuario.html', info_cuenta=dicc_usuario,
                                           tipo_usuario=session['tipo'], id_consultante=session['id_usuario'])
                else:
                    dicc_usuario = get_info_usuario(id_usuario)
                    return render_template('informacion_usuario.html', info_cuenta=dicc_usuario,
                                           tipo_usuario=session['tipo'], id_consultante=session['id_usuario'])
            elif request.method == 'POST':
                if id_usuario is None:
                    id_usuario = session['id_usuario']
                correo_a_modificar = request.form['correo']
                correo_anterior = get_correo_de_usuario(id_usuario)
                if correo_anterior != correo_a_modificar:
                    if usuario_existe('correo', correo_a_modificar):
                        flash('El correo "' + correo_a_modificar + '" ya esta registrado por otro usuario')
                        return redirect('/info_cuenta/' + str(id_usuario))

                nombre = request.form['nombre']
                apellido1 = request.form['apellido1']
                apellido2 = request.form['apellido2']
                telefono = request.form['telefono']
                if session['tipo'] == 'gerente' or session['tipo'] == 'recepcionista':
                    tipo_usuario = request.form['tipo_usuario']
                else:
                    tipo_usuario = session['tipo']

                update_usuario(id_usuario, nombre, apellido1, apellido2, correo_a_modificar, telefono, tipo_usuario)
                return redirect('/consultar_clientes')

        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/eliminar_cita/<id_cita>', methods = ['GET','POST'])
def eliminar_cita(id_cita):
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if not cita_existe(id_cita):
                    return redirect('/consultar_citas')
                if session['tipo'] == 'cliente' and not cita_pertenece_a_usuario('id_cliente',session['id_usuario'], id_cita):
                    abort(403)
                if cita_ya_paso(id_cita):
                    flash('No puedes eliminar citas pasadas')
                    return redirect('/información_cita/'+str(id_cita))

                if request.method == 'GET':
                    info_cita = get_dicc_info_cita(id_cita)
                    return render_template('eliminar_cita.html',dicc_cita=info_cita)
                elif request.method == 'POST':
                    delete_cita(id_cita)
                    return redirect('/consultar_citas')
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)



@app.route('/consultar_clientes')
def consultar_clientes():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente' or session['tipo'] == 'recepcionista':
                clientes = get_lista_clientes()
                return render_template('consultar_clientes.html', lista_clientes=clientes)
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/consultar_usuarios')
def consultar_usuarios():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente':
                usuarios = get_lista_usuarios()
                return render_template('consultar_usuarios.html', lista_usuarios=usuarios)
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/cambiar_password', methods=['GET', 'POST'])
def cambiar_password():
    if 'logeado' in session.keys():
        if session['logeado']:
            if request.method == 'GET':
                return render_template('cambiar_password.html')
            elif request.method == 'POST':
                password = request.form['old_password']
                print('ANTIGUA CONTRASEÑA --> ',password)
                usr = get_usuario('id_usuario', session['id_usuario'])
                if sha256_crypt.verify(password, usr['contrasenia']):
                    new_password1 = request.form['new_password1']
                    new_password2 = request.form['new_password2']
                    if new_password1 != new_password2:
                        flash('Contraseñas no concuerdan, intente de nuevo')
                        return redirect('/cambiar_password')
                    else:
                        print('Contraseña a cambiar -->',password)
                        update_password(session['id_usuario'] ,sha256_crypt.hash(new_password1))
                        flash('Contraseña cambiada exitosamente')
                        return redirect('/info_cuenta')
                else:

                    flash('Contraseña incorrecta')
                    return redirect('/cambiar_password')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente' or session['tipo'] == 'recepcionista':
                if request.method == 'GET':
                    return render_template('registrar_usuario.html', tipo_usuario=session['tipo'])
                elif request.method == 'POST':
                    correo = request.form['correo']
                    if usuario_existe('correo', correo):
                        flash('El correo "' + correo + '" ya esta registrado por otro usuario')
                        return redirect(
                            'registrar_usuario')

                    nombre = request.form['nombre']
                    apellido1 = request.form['apellido1']
                    apellido2 = request.form['apellido2']
                    telefono = request.form['telefono']

                    tipo_usuario = request.form['tipo_usuario']
                    password = generar_password()

                    insertar_usuario(nombre, apellido1, apellido2, correo, sha256_crypt.hash(password),
                                     telefono, tipo_usuario)
                    mandar_correo_de_password('petvetreal@gmail.com', correo, 'aozykokpzeaqcnzv',password)
                    return redirect('/')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/informacion_usuario')
def informacion_usuario():
    return render_template("informacion_usuario.html")


@app.route('/reparacion')
def reparacion():
    return render_template("reparacion.html")


# Informes se va a dividir en diaria, mensual y en rango.

@app.route("/informe_ventas/diaria", methods=['GET', 'POST'])
def informe_ventas_diaria():
    ''' Se asegura que la cuenta tenga permisos de administrador.
    Regresa el template con toda la información del sistema para mostrar su respectivo informe de ventas.
    Si se selecciona alguna fecha en especifico la información cambia dependiendo de la misma.
    '''
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'gerente' or session['tipo'] == 'recepcionista':
                if request.method == 'GET' :
                    horas = []
                    fecha = get_cur_datetime()
                    desde = fecha['now']
                    hasta = fecha['now']
                    citas = get_lista_citas_fechas(desde, hasta) 
                    usuarios = get_lista_usuarios_fechas(desde, hasta) 
                    servicios = get_lista_serv_de_citas()  
                    suma = get_suma_citas(desde, hasta)
                    total_citas_subtotal = suma['SUM(monto)']
                    total_citas_iva = suma['SUM(iva)']
                    total_citas_total = suma['SUM(total)']
                    
                    data_dict = get_datos_grafica_diaria(desde)

                    return render_template("reporte.html", lista_usuarios=usuarios,
                                        total_citas_subtotal=total_citas_subtotal,
                                        total_citas_iva=total_citas_iva,
                                        total_citas_total=total_citas_total,
                                        lista_citas=citas, lista_servicios=servicios,
                                        tipo='Diario', date=fecha['now'], data=json.dumps(data_dict))

                if request.method == 'POST':             
                    fecha = request.form['fecha']                   
                    citas = get_lista_citas_fechas(fecha, fecha) 
                    usuarios = get_lista_usuarios_fechas(fecha, fecha) 
                    servicios = get_lista_serv_de_citas()  
                    suma = get_suma_citas(fecha, fecha)
                    total_citas_subtotal = suma['SUM(monto)']
                    total_citas_iva = suma['SUM(iva)']
                    total_citas_total = suma['SUM(total)']
                    
                    data_dict = get_datos_grafica_diaria(fecha)

                    return render_template("reporte.html", lista_usuarios=usuarios,
                                        total_citas_subtotal=total_citas_subtotal,
                                        total_citas_iva=total_citas_iva,
                                        total_citas_total=total_citas_total,
                                        lista_citas=citas, lista_servicios=servicios,
                                        tipo='Diario', date=fecha, data=json.dumps(data_dict))
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)
        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
