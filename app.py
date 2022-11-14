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

lista_servicios_sel = []
lista_horas_disponibles = []


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


# METODO DE PRUEBA
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
                    global lista_servicios_sel
                    lista_servicios_sel = obtener_servicios(request.form.to_dict())
                    global lista_horas_disponibles
                    lista_horas_disponibles = obtener_horas_disponibles(id_sucursal, fecha, lista_servicios_sel)

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
            if request.method == 'GET':

                return render_template("hora_cita.html", horas_disponibles=lista_horas_disponibles)
            elif request.method == 'POST':
                print()
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render_template("hora_cita.html")


@app.route('/consultar_citas')
def consultar_citas():
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] == 'cliente' or session['tipo'] == 'estilista':
                citas = get_citas_de_usuario('id_' + session['tipo'], session['id_usuario'])
                return render_template("consultar_citas.html", lista_citas=citas)
            elif session['tipo'] == 'recepcionista':
                return redirect('/')
            elif session['tipo'] == 'gerente':
                return redirect('/')
            else:
                return redirect('/')

    else:

        return redirect('/')
    # return render_template("consultar_citas.html")


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
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/reparacion')
def reparacion():
    return render_template("reparacion.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
