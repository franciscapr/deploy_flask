from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash    # encargado de entregar mensajes 

import re    # Expresiones Regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')    # Expresion regular de email


# Creamos la clase usuario
class User:
    def __init__(self, data):
        # data es un diccionario con toda la info de la instancia
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Método para crear un nuevo registro ---> INSERT
    @classmethod
    def save(cls, form):
        # form = diccionario con toda la información de nuestro usuario
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUE(%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        # Regresamos el resultado de esto -> conección con la db -> nombre de la db
        return connectToMySQL('movies_examen').query_db(query, form)
    
    # Método que regresa objeto de Usuario en base a e-mail
    @classmethod
    def get_by_email(cls, form):
        # form = {"email": "elena@cd.com", "password": "hola123"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("movies_examen").query_db(query, form)    # Regresa una lista de diccionarios
        if len(result) < 1:    # Revisa que mi lista esté vacía
            return False
        else:
            # llama al constructor de la clase 'cls' y le pasa el diccionario 'result[0]' para crear una nueva instancia de la clase con esos datos.
            user = cls(result[0])
            # Devuelve la instancia de usuario creada.
            return user
        
    # Método para validar la información que viene desde form
    @staticmethod
    def validate_user(form):
        # form = {diccionario con toda la info del formulario}
        is_valid = True

        # Validamos que el nombre tenga al menos 2 caracteres
        if len(form["first_name"]) < 2:
            flash("First name must have at least 2 chars", "register")
            is_valid = False

        if len(form["last_name"]) < 2:
            flash("Last name must have at least 2 chars", "register")
            is_valid = False

        if len(form["password"]) < 6:
            flash("Password must have at least 6 chars", "register")
            is_valid = False

        # Validar que el correo sea único
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('movies_examen').query_db(query, form)
        if len(result) >= 1:
            # si existe ese correro en mi BDs
            flash("E-mail already registered", "register")
            is_valid = False

        # Verificamos que las contraseñas coincidan
        if form["password"] != form["confirm"]:
            flash("Passwords do not match", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form["email"]):
            flash("E-mail not valid", "register")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_id(cls, data):
        #data = {"id": 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('movies_examen').query_db(query, data)    
        user = cls(result[0])
        return user