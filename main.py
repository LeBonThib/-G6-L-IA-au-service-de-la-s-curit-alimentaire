from website import create_app

app = create_app()

if __name__ == '__main__': #prevents web server starting without running main.py (e.g: can't import it and run it from another file)
    app.run(debug=True)