from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort
from passlib.hash import sha256_crypt
from bd import *
from herramientas import *

app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'


@app.route('/login')
def inicio_sesion():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/')
def inicio():
    return render_template("inicio.html")


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
    session['logeado'] = True
    session['tipo'] = 'cliente'
    session['id_usuario'] = 3
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo'] != 'estilista':
                if request.method == 'GET':
                    sucursales = get_lista_sucursales()
                    servicios = get_lista_servicios()

                    fecha = get_cur_datetime()
                    return render_template('escoger_cita.html',
                                           lista_sucursales=get_lista_sucursales(),
                                           lista_servicios=get_lista_servicios(),
                                           date_min=fecha['fecha_actual'],
                                           date_max=fecha['fecha_fin'])
                elif request.method == 'POST':
                    print(request.form['fecha'])
                    print(request.form['tipo_servicio'])
                    print(request.form['tipo_sucursal'])
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


@app.route('/hora_cita')
def hora_cita():
    return render_template("hora_cita.html")


@app.route('/consultar_citas')
def consultar_citas():
    session['logeado'] = True
    session['tipo'] = 'estilista'
    session['id_usuario'] = 3
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
    session['logeado'] = True
    session['tipo'] = 'estilista'
    session['id_usuario'] = 3
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

    return render_template("informacion_cita.html")


@app.route('/reparacion')
def reparacion():
    return render_template("reparacion.html")


@app.route('/pruebabd')
def pruebabd():
    return str(bd.get_usuarios())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
