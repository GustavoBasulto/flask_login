import os
from flask_app.models.user import User
from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt(app)

@app.route("/")
def index():
    if 'mail' in session:
        return redirect("/main")
    else:
        return render_template("login.html")
    

@app.route("/main")
def thoughts():
    if 'mail' in session:
        return render_template("user.html")
    else:
        flash("debes iniciar sesion", "error")
        return redirect("/")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    if not User.validate_user(request.form):
        return redirect('/')

    if User.email_bbdd(request.form['mail']):
        flash(f"El correo {request.form['mail']} ya esta registrado", "error")
        return redirect('/')
    
    hash_pass = bcrypt.generate_password_hash(request.form['contraseña'])
    
    data = {
        "nombre": request.form["nombre"],
        "apellido" : request.form["apellido"],
        "mail" : request.form["mail"],
        "contraseña" : hash_pass
    }
    
    print(data)
    User.save(data)
    flash(f"exito al agregar el usuario {data['nombre']}", "success")
    return redirect("/")

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    if not User.validate_login(request.form):
        return redirect('/')

    usuario=User.email_bbdd(request.form['mail'])
    if not usuario:
        flash("Usuario o clave incorrecta", "error")    
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.get('password'), request.form['contraseña']):
        flash("Usuario o clave incorrecta", "error")
        return redirect("/")

    session['mail']=usuario.get('email')
    session['usuario']=usuario.get('first_name')
    return redirect("/main")
    
@app.route("/cerrar_session")
def cerrar_session():
    session.clear()
    return redirect ("/")
