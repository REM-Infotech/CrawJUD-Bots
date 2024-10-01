
from app import app, io
from app.routes.bot import bot

from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit


app.register_blueprint(bot)
    
@io.on('connect', namespace='/log')
def handle_connect():
    pass

@io.on('disconnect', namespace='/log')
def handle_disconnect():
    pass

@io.on('join', namespace='/log')
def handle_join(data):
    room = data['pid']
    join_room(room)
    # print(f"Client {request.sid} joined room {room}")

@io.on('leave', namespace='/log')
def handle_leave(data):
    room = data['pid']
    leave_room(room)
    # print(f"Client {request.sid} left room {room}")

@io.on('log_message', namespace='/log')
def handle_message(data):
    pid = data['pid']
    message = data['message']
    emit('log_message', data, room=pid)
    # print("mensagem enviada")