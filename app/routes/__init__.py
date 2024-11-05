from app import app, io, db
from app.routes.bot import bot
from app.routes import handler
from bot.Utils.StartStop_Notify import SetStatus
from flask_socketio import join_room, leave_room, emit
from app.models import CacheLogs, Executions
from flask import abort, request

app.register_blueprint(bot)
__all__ = [handler]


@io.on("connect", namespace="/log")
def handle_connect():
    pass


@io.on("disconnect", namespace="/log")
def handle_disconnect():
    pass


@io.on("join", namespace="/log")
def handle_join(data):

    room = data["pid"]
    try:
        join_room(room)
        app.logger.info(f"Client {request.sid} joined room {room}")
    except Exception:
        emit("log_message", data, room=room)


@io.on("leave", namespace="/log")
def handle_leave(data):
    room = data["pid"]
    leave_room(room)
    app.logger.info(f"Client {request.sid} left room {data["pid"]}")


@io.on("log_message", namespace="/log")
def handle_message(data: dict[str, str | int]):

    try:
        pid = data["pid"]
        data = serverSide(data, pid)
        emit("log_message", data, room=pid)
        app.logger.info(f"Client {request.sid} sended message {data["message"]}")

    except Exception as e:
        abort(500, description=str(e))


def serverSide(data, pid):

    chk_infos = [data.get("system"), data.get("typebot")]

    if all(chk_infos):

        SetStatus(
            status="Finalizado",
            pid=pid,
            system=data["system"],
            typebot=data["system"],
        ).botstop()

    log_pid = CacheLogs.query.filter(CacheLogs.pid == data["pid"]).first()
    if not log_pid:

        execut = (
            db.session.query(Executions).filter(Executions.pid == data["pid"]).first()
        )
        log_pid = CacheLogs(
            pid=data["pid"],
            pos=int(data["pos"]),
            total=int(execut.total_rows) - 1,
            remaining=int(execut.total_rows) - 1,
            success=0,
            errors=0,
            status=execut.status,
            last_log=data["message"],
        )
        db.session.add(log_pid)

    elif log_pid:

        log_pid.pos = int(data["pos"])

        type_S1 = data["type"] == "success"
        type_S2 = data["type"] == "info"
        type_S3 = data["graphicMode"] != "doughnut"

        typeSuccess = type_S1 or type_S2 and type_S3

        if typeSuccess:

            log_pid.remaining -= 1
            if "fim da execução" not in data["message"].lower():
                log_pid.success += 1

            log_pid.last_log = data["message"]

        elif data["type"] == "error":

            log_pid.remaining -= 1
            log_pid.errors += 1
            log_pid.last_log = data["message"]

            if data["pos"] == 0:
                log_pid.errors = log_pid.total
                log_pid.remaining = 0

        if "fim da execução" in data["message"].lower():
            log_pid.remaining = 0
            log_pid.status = "Finalizado"

    db.session.commit()
    data.update(
        {
            "pid": data["pid"],
            "pos": int(data["pos"]),
            "total": log_pid.total,
            "remaining": log_pid.remaining,
            "success": log_pid.success,
            "errors": log_pid.errors,
            "status": log_pid.status,
            "last_log": log_pid.last_log,
        }
    )

    return data
