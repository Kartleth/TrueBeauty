from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort
from passlib.hash import sha256_crypt
import bd

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

@app.route('/agendar_cita')
def agendar_cita():
    return render_template("agendar_cita.html")

@app.route('/fecha_cita')
def fecha_cita():
    return render_template("fecha_cita.html")

@app.route('/hora_cita')
def hora_cita():
    return render_template("hora_cita.html")

@app.route('/consultar_citas')
def consultar_citas():
    session['logeado'] = True
    session['tipo'] = 'cliente'
    session['id_usuario']=4
    if 'logeado' in session.keys():
        if session['logeado']:
            if session['tipo']=='cliente':
                citas = bd.get_citas_de_usuario(session['id_usuario'])
                return render_template("consultar_citas.html",lista_citas=citas)
    else:
        return redirect('/')
    # return render_template("consultar_citas.html")

@app.route('/informacion_cita')
def informacion_cita():
    return render_template("informacion_cita.html")

@app.route('/reparacion')
def reparacion():

    return render_template("reparacion.html")


@app.route('/pruebabd')
def pruebabd():
    return str(bd.get_usuarios())


if __name__ == '__main__':


    app.run(debug=True, host='0.0.0.0', port=5000)

