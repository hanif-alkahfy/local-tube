from flask import Flask
from flask_cors import CORS
from routes.api import api

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix="/api")

@app.route("/")
def index():
    return "LocalTube Backend is Running!"

if __name__ == "__main__":
    app.run(debug=True)
