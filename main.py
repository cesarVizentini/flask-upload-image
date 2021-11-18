from flask import Flask, flash, render_template, request, redirect, url_for, session

import urllib.request
import os
from werkzeug.utils import secure_filename

import psycopg2 #pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = ""
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

DB_HOST = "localhost"
DB_NAME = "upload-image"
DB_USER = "postgres"
DB_PASS = ""
# db = MySQL(app)
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'email' in request.form and 'senha' in request.form:
            email = request.form['email']
            senha = request.form['senha']
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM login_info WHERE email=%s AND senha=%s", (email, senha))
            info = cursor.fetchone()
            # se nao encontra nenhum registro com as credencias fornecidas o objeto info fica vazio
            # mexer na validacao abaixo (18:00)
            print("#########################")
            print(info)
            if info is not None:
                session['loginsuccess'] = True
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))

    return render_template("login.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form and "four" in request.form and "five" in request.form:
            nome = request.form['one']
            email = request.form['two']
            # data_nascimento = request.form['three']
            data_nascimento = "2021-12-12"
            genero = request.form['four']
            senha = request.form['five']
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("INSERT INTO login_info (nome, email, data_nascimento, genero, senha) VALUES (%s, %s, %s, %s, %s)", (nome, email, data_nascimento, genero, senha))
            conn.commit()
            return redirect(url_for('index'))

    return render_template("register.html")

@app.route('/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template("profile.html")

@app.route('/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))


# @app.route('/', methods=['POST'])
# def upload_image():
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         # print('upload_image filename: ' + filename)
#
#         cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
#         conn.commit()
#
#         flash('Image successfully uploaded and displayed below')
#         return render_template('index.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)