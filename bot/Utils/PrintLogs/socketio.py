from socketio import Client
from contextlib import suppress


class SocketIo_CrawJUD:

    socketio = Client()

    @socketio.event(namespace="/log")
    def connect():
        pass

    @socketio.event(namespace="/log")
    def disconnect():
        pass

    @property
    def connected(self) -> bool:
        return self.connect

    @connected.setter
    def connected(self, is_connected: bool):
        self.conectado = is_connected

    def connect_socket(pid):
        # Conecta ao servidor SocketIO no URL especificado

        if connect:

            server_url = f"https://{url_socket(pid)}"

            with suppress(Exception):
                socketio.connect(server_url)

    def disconnect_socket():
        # Desconecta do servidor SocketIO
        socketio.disconnect()

    def socket_message(pid, formatted_message):

        try:
            pass

        finally:
            try:
                connect_socket(pid)
                # Envia a mensagem de log formatada para o servidor SocketIO
                socketio.emit(
                    "log_message",
                    {"message": formatted_message, "pid": pid},
                    namespace="/log",
                )

            except Exception as e:
                print(e)
