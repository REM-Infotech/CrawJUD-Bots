
from app import app, io, db
from app.routes.bot import bot

from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.models import CacheLogs, Executions

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
def handle_message(data: dict[str, str | int]):
    
    pid = data['pid']
    message = data['message']
    pos = int(data["pos"])
    
    log_pid = CacheLogs.query.filter(CacheLogs.pid == pid).first()
    if not log_pid:
        
        execut = Executions.query.filter(Executions.pid == pid).first()
        log_pid = CacheLogs(
            pid = pid,
            pos = int(data["pos"]),
            total = execut.total_rows,
            remaining = execut.total_rows,
            success = 0,
            errors = 0,
            status = execut.status,
            last_log = message
        )
        db.session.add(log_pid)
        
    elif log_pid:
        
        log_pid.pos = int(data["pos"])
        if data["type"] == "success":
            log_pid.remaining -= 1
            log_pid.success += 1
            log_pid.last_log = message
        
        elif data["type"] == "error":
            
            log_pid.remaining -= 1
            log_pid.errors += 1
            log_pid.last_log = message
            
            if pos == 0:
                log_pid.errors = log_pid.total
                log_pid.remaining = 0

        if "fim da execução" in message.lower():
            log_pid.status = "Finalizado"
    
    db.session.commit()
    data.update(
        {"pid" : pid,
        "pos" : int(data["pos"]),
        "total" : log_pid.total,
        "remaining" : log_pid.remaining,
        "success" : log_pid.success,
        "errors" : log_pid.errors,
        "status" : log_pid.status,
        "last_log" : log_pid.last_log}
    )
    
    emit('log_message', data, room=pid)
    # print("mensagem enviada")