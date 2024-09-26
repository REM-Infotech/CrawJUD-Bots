from app import app, socketio
from dotenv import  dotenv_values
import os

if __name__ == "__main__":  
    
    debug = dotenv_values().get('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')
    
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
