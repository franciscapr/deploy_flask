from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data.get("updated_at")  # Utiliza get() para evitar el KeyError si no existe
        self.event_id = data["event_id"]
        self.user_id = data['user_id']
        self.user_name = data.get("user_name")  # Utiliza get() por si no está presente

    @classmethod
    def save(cls, form):
        query = "INSERT INTO comments (content, user_id, event_id) VALUES (%(content)s, %(user_id)s, %(event_id)s)"
        return connectToMySQL("movies_examen").query_db(query, form)

    @classmethod
    def get_by_event_id(cls, event_id):
        query = """
                SELECT comments.id, comments.content, comments.created_at, comments.updated_at, 
                       comments.event_id, comments.user_id, users.first_name AS user_name
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.event_id = %(event_id)s 
                """
        data = {'event_id': event_id}
        results = connectToMySQL("movies_examen").query_db(query, data)
        comments = []
        for row in results:
            comments.append(cls(row))
        return comments

    @classmethod
    def get_by_id(cls, comment_id):
        query = "SELECT * FROM comments WHERE id = %(id)s"
        data = {'id': comment_id}
        result = connectToMySQL("movies_examen").query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @staticmethod
    def validate_comment(form):
        is_valid = True
        if len(form["content"]) < 1:
            flash("Comment content is required", "comment")
            is_valid = False
        return is_valid

    @classmethod
    def delete(cls, comment_id):
        query = "DELETE FROM comments WHERE id = %(id)s"
        data = {'id': comment_id}
        connectToMySQL("movies_examen").query_db(query, data)
        flash("Comentario eliminado exitosamente.", "success")
