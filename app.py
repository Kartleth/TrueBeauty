from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort


app = Flask(__name__)
app.secret_key = 'lwiu74dhn2SuF3j'

@app.route('/')
def hello_world():  # put application's code here
    return render_template("prueba.html")

@app.route('/login')
def inicio_sesion():  # put application's code here
    return render_template("login.html")

@app.route('/inicio')
def inicio():  # put application's code here
    return render_template("inicio.html")

@app.route('/agendar_cita')
def agendar_cita():  # put application's code here
    return render_template("agendar_cita.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
