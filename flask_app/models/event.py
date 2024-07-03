from flask_app.config.mysqlconnection import connectToMySQL    # Importación de la conexión con SQL
from flask import flash 

from datetime import datetime    # Manipular fechas   # encargado de entregar mensajes 

# Creamos la clase de eventos
class Event:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.director = data['director']
        self.date = data['date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user_name = data['user_name']    # Columna extra que obtenemos al hacer una consulta JOIN

    # Método para CREATE
    @classmethod
    def create(cls, form):
        # Insertamos toda la información de nuestros evenetos
        query = 'INSERT INTO events (name, director, date, details, user_id) VALUES(%(name)s, %(director)s, %(date)s, %(details)s, %(user_id)s)' 
        return connectToMySQL('movies_examen').query_db(query, form)


    # Método para READ
    @classmethod
    def read_one(cls, data):
        query = "SELECT events.*, users.first_name as user_name FROM events JOIN users ON events.user_id = users.id WHERE events.id = %(id)s;"
        result = connectToMySQL('movies_examen').query_db(query, data)
        # result = [{"id": 1, "name": "Examen", "location", "Casa", "data": 2024-06-28...}]
        event = cls(result[0])    # Objeto de event
        return event    # Devolvemos el objeto de event
    
    @classmethod
    def read_all(cls):
        query = "SELECT events.*, users.first_name as user_name FROM events JOIN users ON events.user_id = users.id WHERE date >= CURDATE() ORDER BY date ASC;"
        results = connectToMySQL("movies_examen").query_db(query)
        events = []
        for ev in results:
            events.append(cls(ev))
        return events


    @staticmethod
    def validate_event(form):
        is_valid = True
        if len(form['name']) < 3:    # Si el tamaño de name es menor de 3 entonces flash
            flash("El nombre del evento debe tener al menos 3 caracteres", "evento")    #(mensaje, categoria)
            is_valid = False

        if len(form['director']) < 3:    # Si el tamaño de name es menor de 3 entonces flash
            flash("El director de la pelicula debe tener al menos 3 caracteres", "evento")    #(mensaje, categoria)
            is_valid = False

        if len(form['details']) < 3:    # Si el tamaño de name es menor de 3 entonces flash
            flash("Los detalles del evento debe tener al menos 3 caracteres", "evento")    #(mensaje, categoria)
            is_valid = False

        if form['date'] == "":
            flash('Ingrese una fecha', 'evento')
            is_valid = False

        else:
            # Validar que la fecha sea en el futuro
            fecha_obj = datetime.strptime(form['date'], '%Y-%m-%d')
            hoy = datetime.now()
            # Comparamos
            if hoy > fecha_obj:
                flash('La fecha no puede ser en el pasado', 'evento')
                is_valid = False
            # Validación ---> Fecha en el futuro


        # if form["name"] == form["name"]:
        #     flash("No se puede registrar el mismo nombre de evento, cambialo", "evento")
        #     is_valid = False


        return is_valid



    # Método para UPDATE
    @classmethod
    def update(cls, form):
        # form = {la infromación que se enció en el formulario}
        query = "UPDATE events SET name=%(name)s, director=%(director)s, date=%(date)s, details=%(details)s, user_id=%(user_id)s WHERE id=%(id)s "
        return connectToMySQL('movies_examen').query_db(query, form)



    # Método para DELETE
    @classmethod
    def delete(cls, data):
        # data = {"id": 2}
        query = "DELETE FROM events WHERE id = %(id)s"
        return connectToMySQL("movies_examen").query_db(query, data)



# Bonus
# 1. Orden de Dashboard que sea en base a fecha asc LISTO
# 2. En Dashboard no aparezcan eventos del pasado. LISTO
# 3. Cuando se cree un evento, solo se puedan registrar eventos sean futuros. Validar que el evento sea en el futuro. LISTO
# 4. Al editar hace un double check de que la persona de sesión sea el creador del evento. LISTO
# 5. Revisar que el nombre del evento sea único --> Validamos en edición se debe cambiar un poco. 
# 6. Almacenar detalle en algún lado, para si hay errores no volverlos a escribir. LISTO