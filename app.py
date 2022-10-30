from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort


app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'

@app.route('/')
def hello_world():  # put application's code here
    return render_template("prueba.html")

@app.route('/login')
def inicio_sesion():  # put application's code here
    return render_template("login.html")

@app.route('/signup')
def signup():  # put application's code here
    return render_template("signup.html")

@app.route('/inicio')
def inicio():  # put application's code here
    return render_template("inicio.html")

@app.route('/agendar_cita')
def agendar_cita():  # put application's code here
    return render_template("agendar_cita.html")

@app.route('/fecha_cita')
def fecha_cita():  # put application's code here
    return render_template("fecha_cita.html")

@app.route('/hora_cita')
def hora_cita():  # put application's code here
    return render_template("hora_cita.html")

@app.route('/consultar_citas')
def consultar_citas():  # put application's code here
    return render_template("consultar_citas.html")

@app.route('/informacion_cita')
def informacion_cita():  # put application's code here
    return render_template("informacion_cita.html")

@app.route('/reparacion')
def reparacion():  # put application's code here
    return render_template("reparacion.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

