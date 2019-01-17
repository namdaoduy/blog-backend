from main import app

if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost',
            port=5000,
            threaded=True)
