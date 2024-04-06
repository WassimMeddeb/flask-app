from flask import Flask
from routes.auth_routes import auth_routes
from routes.main_routes import main_routes
import os
from dotenv import load_dotenv
load_dotenv
app = Flask(__name__)
app.secret_key = b'5b3b4208abcca6b4e69e71288deb57cd3cf5860c'


app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True)
