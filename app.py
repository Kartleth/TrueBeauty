from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, abort


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("prueba.html")


if __name__ == '__main__':
    app.run()
