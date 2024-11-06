from app import app, db
from flask import request, abort
from flask_socketio import emit, join_room, Namespace
from ...loggers import info_logger

from status import SetStatus
from app.models import CacheLogs, Executions

with app.app_context():

    class LogNamespace(Namespace):

        def on_connect(self):
            emit("connected!")

        def on_disconnect(self):
            emit("disconnected!")

        def on_join(self, data: dict[str, str]):
            request
            info_logger.info("Joined")
            room = data["pid"]
            status = get_Status(room)
            try:
                join_room(room)
                app.logger.info(f"Client {request.sid} joined room {room}")
            except Exception:
                emit("log_message", data, room=room)

        def on_stop_bot(self, data: dict[str, str]):

            pid = data["pid"]
            SetStatus(pid=pid, status=data["status"]).botstop()
            emit("statusbot", data=data)

        def on_statusbot(self, data: dict):
            app.logger.info(f"Client {request.sid} stop bot {data["pid"]}")

        def on_log_message(self, data: dict[str, str]):

            try:
                pid = data["pid"]
                data = serverSide(data, pid)
                emit("log_message", data, room=pid)
                app.logger.info(
                    f"Client {request.sid} sended message {data["message"]}"
                )

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
                db.session.query(Executions)
                .filter(Executions.pid == data["pid"])
                .first()
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

    def get_Status(pid: str):

        execut = db.session.query(Executions).filter(Executions.pid == pid).first()
        if execut:
            pass
        
        return execut
