from bot import PORT, DEBUG, app
from waitress import serve

if __name__ == "__main__":
    # Start server
    if DEBUG:
        app.run(host="0.0.0.0", port=PORT, debug=True)
    else:
        serve(app, listen="*:" + PORT)