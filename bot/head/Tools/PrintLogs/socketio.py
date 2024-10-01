from socketio import Client

socketio = Client()
cache_connection = []

@socketio.event(namespace='/log')
def connect():
     pass

@socketio.event(namespace='/log')
def disconnect():
    pass
    
    
def connect_socket(pid: str, url_socket: str):
    # Conecta ao servidor SocketIO no URL especificado
    
    if len(cache_connection) == 0:
        
        server_url = f"https://{url_socket}"
        
        try:
            socketio.connect(server_url)
            cache_connection.append("Already connected")
        except Exception as e:
            
            print(e)

def disconnect_socket():
    # Desconecta do servidor SocketIO
    socketio.disconnect()
    
    
def socket_message(pid: str, formatted_message: str, url_socket: str, 
                   type: str, pos: int):
    
    try:
        connect_socket(pid, url_socket)
        # Envia a mensagem de log formatada para o servidor SocketIO
        if len(cache_connection) != 0:
            data = {'message': formatted_message, 
                    'pid': pid,
                    "type": type,
                    "pos": pos}
            
            socketio.emit('log_message', data, namespace='/log')
        
    except Exception as e:
        print(e)
        