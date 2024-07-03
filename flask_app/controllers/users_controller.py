from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

# Importamos los modelos
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.comment import Comment


# Importar BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Ruta que recibe el formulario
@app.route('/register', methods=['POST'])
def register():
    #request.form = {"first_name": "Elena", "last_name": "De Troya"...}

    # Validar la info que recibimos
    if not User.validate_user(request.form):
        # No es valida la info, redirecciono al form
        return redirect('/')

    # Encriptar la contraseña
    pass_hash = bcrypt.generate_password_hash(request.form['password'])

    # Crear un diccionario que simule el form, incluyendo la contraseña hasheada
    form = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pass_hash
    }

    id = User.save(form)    # Recibo el ID del nuevo usuario
    session['user_id'] = id    # Guardamos en sesión el ID del usuario
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')
    
    dicc = {'id': session['user_id']}
    user = User.get_by_id(dicc)

    events = Event.read_all()
    
    return render_template('dashboard.html', user=user, events=events)




@app.route('/login', methods=['POST'])
def login():
    # request.form = {"email": "elena@gmail.com", "password": "Hola123"}
    # Verifico que el email esté en mi BD
    user = User.get_by_email(request.form)    # Recibimos False en caso de que no exista el usuario o regresa el objeto si existe
    if not user:    # Si user = False
        flash("E-mail not foud", "login")
        return redirect('/')
    # Si user si es objeto user
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrect", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')