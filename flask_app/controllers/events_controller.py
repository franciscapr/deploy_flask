from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

# Importamos los modelos
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.comment import Comment


# Creamos la ruta new
@app.route('/new')
def new():
    # Revisamos si inicio sesión el usuario
    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    
    # Guardamos en sesión los detalles
    session['details'] = request.form['details']

    if not Event.validate_event(request.form):
        return redirect('/new')

    Event.create(request.form)
    session.pop('details')
    return redirect("/dashboard")

@app.route('/ver/<int:id>')    # Recibimos la información
def read(id):    # id = 1
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')
    
    dicc = {"id": id}    # {"id": 1}
    event = Event.read_one(dicc)    # Invoco a la clase Event a read_one, enviamos el diccionario y recibimos un objeto Events
    comments = Comment.get_by_event_id(id)  # Cambia esta línea para llamar a get_by_event_id
    
    # Manejar el caso cuando no hay comentarios
    if not comments:
        comments = []  # Inicializa como una lista vacía si no hay comentarios
    
    return render_template('view.html', event=event, comments=comments, post_id=id)



@app.route('/borrar/<int:id>')
def delete(id):
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Verificar si hay comentarios asociados al evento
    comments = Comment.get_by_event_id(id)
    if comments:
        flash("Solo puedes aliminar peliculas sin comentarios asociados", "error")
        return redirect('/dashboard')


    dicc = {"id": id}
    Event.delete(dicc)
    return redirect('/dashboard')


@app.route('/editar/<int:id>')
def edit(id):
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')
    
    dicc = {"id": id}
    event = Event.read_one(dicc)

    # Revisar que si sea el usuario en sesión el que creó el evento
    if session['user_id'] != event.user_id:
        return redirect('/dashboard')
    

    return render_template('editar.html', event=event)

@app.route('/update', methods=['POST'])
def update():
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Recibir request.form = diccionario con la infromación del formulario

    # Validamos
    if not Event.validate_event(request.form):
        return redirect('/editar/'+request.form['id'])
    
    Event.update(request.form)
    return redirect('/dashboard')








# Objetos: user.id
# Diccionario session["user_id"]
# Listas: result[0]