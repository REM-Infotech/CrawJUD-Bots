from app import app

from app.routes.bot import bot


app.register_blueprint(bot)