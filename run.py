from bot import PORT, app

if __name__ == "__main__":
    # Start server
    app.run(host="0.0.0.0", port=PORT, debug=True)