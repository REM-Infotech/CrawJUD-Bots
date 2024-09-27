from app import create_app

if __name__ == "__main__":
    
    app, port, debug, io = create_app()
    io.run(app, "0.0.0.0", port=int(port), debug=debug)