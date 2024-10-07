
from app import app, io, db
from app.routes.bot import bot

from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.models import CacheLogs, Executions

from time import sleep

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
    sleep(3)
    log_pid = CacheLogs.query.filter(CacheLogs.pid == room).first()    
    if log_pid:
        data={
            "pid" : room,
            "pos" : log_pid.pos,
            "total" : log_pid.total,
            "remaining" : log_pid.remaining,
            "success" : log_pid.success,
            "errors" : log_pid.errors,
            "status" : log_pid.status,
            "last_log" : log_pid.last_log}
    
    try:
        join_room(room)
        emit('log_message', data, room=room)
        # print(f"Client {request.sid} joined room {room}")
    except:
        emit('log_message', data, room=room)

@io.on('leave', namespace='/log')
def handle_leave(data):
    room = data['pid']
    leave_room(room)
    # print(f"Client {request.sid} left room {room}")

@io.on('log_message', namespace='/log')
def handle_message(data: dict[str, str | int]):
    
    pid = data['pid']
    emit('log_message', data, room=pid)
    # print("mensagem enviada")