from website import create_app
#pode fazer isso por causa do __init__.py

app = create_app()

if __name__ == '__main__': #only if we run this file
    app.run(debug=True) #auto rerun webserver, turn off in production

