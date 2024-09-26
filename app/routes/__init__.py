from flask_socketio import emit, join_room, leave_room
from app import app, socketio

from app.routes.bot import bot
app.register_blueprint(bot)

@socketio.on('connect', namespace='/log')
def handle_connect():
    pass

@socketio.on('disconnect', namespace='/log')
def handle_disconnect():
    pass

@socketio.on('join', namespace='/log')
def handle_join(data):
    room = data['pid']
    join_room(room)
    # print(f"Client {request.sid} joined room {room}")

@socketio.on('leave', namespace='/log')
def handle_leave(data):
    room = data['pid']
    leave_room(room)
    # print(f"Client {request.sid} left room {room}")

@socketio.on('log_message', namespace='/log')
def handle_message(data):
    pid = data['pid']
    message = data['message']
    emit('log_message', {'message': message, 'pid': pid}, room=pid)
    # print("mensagem enviada")