from app import app
from app import db

url_cache = []

def url_socket(pid) -> str:
    
    
    if len(url_cache) > 0:
        return url_cache[0]
    
    with app.app_context():
        
        url_Server = ExecutionsTable.query.filter_by(pid=pid).first()
        url_srv = url_Server.url_socket
        
        db.session.close()
    
    url_cache.append(url_srv)
    return url_srv
    
    
