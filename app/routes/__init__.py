from app import app, io
from app.routes import handler
from app.routes.bot import bot
from app.routes.logs import LogNamespace

app.register_blueprint(bot)
io.on_namespace(LogNamespace("/log"))

__all__ = [handler]
