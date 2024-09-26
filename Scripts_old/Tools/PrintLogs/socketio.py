from socketio import Client
from Scripts.Tools.get_url_socket import url_socket

from socketio.exceptions import ConnectionError

socketio = Client()

cache_connection = []


@socketio.event(namespace='/log')
def connect():
     pass

@socketio.event(namespace='/log')
def disconnect():
    pass
    
    
def connect_socket(pid):
    # Conecta ao servidor SocketIO no URL especificado
    
    if len(cache_connection) < 1:
        
        server_url = f"{url_socket(pid)}"
        
        try:
            socketio.connect(server_url)
            
        except Exception as e:
            
            pass
            
        cache_connection.append("Already connected")


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
            socketio.emit('log_message', {'message': formatted_message, 'pid': pid}, namespace='/log')
            
        except Exception as e:
            print(e)