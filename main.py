from app import app
app.env = 'development'
app.secret_key = 'bnfdgijbb137'
app.run(port=5000, host='localhost', debug=True)
