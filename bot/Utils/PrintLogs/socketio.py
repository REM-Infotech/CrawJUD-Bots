from socketio import Client


class SocketIo_CrawJUD:

    def __init__(self, **kwrgs):
        self.__dict__.update(kwrgs)

    socketio = Client()

    @socketio.event(namespace="/log")
    def connect():
        pass

    @socketio.event(namespace="/log")
    def disconnect():
        pass

    def send_message(self, data: dict, url_socket: str):

        self.socketio.connect(f"https://{url_socket}")
        self.connect = True

        self.socketio.emit(
            "log_message",
            data=data,
            namespace="/log",
        )

        self.socketio.disconnect()
