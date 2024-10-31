from app import app, io
from dotenv import dotenv_values

if __name__ == "__main__":

    values = dotenv_values()
    port = int(values.get("PORT", 5000))
    debug = values.get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")

    io.run(app, "0.0.0.0", port=int(port), debug=debug)
