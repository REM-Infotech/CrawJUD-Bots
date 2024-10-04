from socketio import Client

socketio = Client()
cache_connection = {}

@socketio.event(namespace='/log')
def connect():
     pass

@socketio.event(namespace='/log')
def disconnect():
    pass
    
    
def connect_socket(pid: str, url_socket: str):
    # Conecta ao servidor SocketIO no URL especificado
    
    if not cache_connection.get("pid", None):
        server_url = f"https://{url_socket}"
        
        try:
            socketio.connect(server_url)
            cache_connection.update({"pid": pid})
        except Exception as e:
            
            print(e)

def disconnect_socket():
    # Desconecta do servidor SocketIO
    socketio.disconnect()
    
    
def socket_message(pid: str, formatted_message: str, url_socket: str, 
                   type: str, pos: int):
    
    try:
        connect_socket(pid, url_socket)
        data = {'message': formatted_message,'pid': pid,"type": type,"pos": pos}
        if cache_connection.get("pid", None):
            emitMessage(data)
        
    except Exception as e:
        print(e)
        cache_connection.pop("pid")
        connect_socket(pid, url_socket)
        emitMessage(data)
        
def emitMessage(data: dict[str, str]):
    socketio.emit('log_message', data, namespace='/log')