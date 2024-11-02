from socketio import Client


class SocketIo_CrawJUD:

    def __init__(self, **kwrgs):
        self.__dict__.update(kwrgs)

    socketio = Client()
    conectado = False

    @socketio.event(namespace="/log")
    def connect():
        pass

    @socketio.event(namespace="/log")
    def disconnect():
        pass

    @property
    def connected(self):
        return self.conectado

    @connected.setter
    def connected(self, is_connected: bool):
        self.conectado = is_connected

    def send_message(self, data: dict, url_socket: str):

        if not self.connect:
            self.socketio.connect(self.url)
            self.connect = True

        self.socketio.emit(
            "log_message",
            data=data,
            namespace="/log",
        )
