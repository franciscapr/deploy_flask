from flask import request, redirect, flash, session
from flask_app import app
from flask_app.models.event import Event  
from flask_app.models.comment import Comment

@app.route('/events/<int:event_id>/comments', methods=['POST'])
def create_comment(event_id):
    form = request.form.to_dict()  

    event = Event.read_one({"id": event_id})

    if session.get('user_id') == event.user_id:
        flash("No puedes comentar en tu propio evento.", "error")
        return redirect(f'/ver/{event_id}')

    if not Comment.validate_comment(form):
        return redirect(f'/ver/{event_id}')

    form['user_id'] = session['user_id']
    form['event_id'] = event_id

    Comment.save(form)
    flash("Comentario guardado exitosamente.", "success")
    return redirect(f'/ver/{event_id}')

@app.route('/events/<int:event_id>/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(event_id, comment_id):
    comment = Comment.get_by_id(comment_id)
    if comment and comment.user_id == session['user_id']:
        Comment.delete(comment_id)
        flash("Comentario eliminado exitosamente.", "success")
    else:
        flash("No tienes permiso para eliminar este comentario.", "error")
    return redirect(f'/ver/{event_id}')