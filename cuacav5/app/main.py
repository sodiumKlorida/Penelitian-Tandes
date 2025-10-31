from flask import Flask
from routes.api_mobile import api_bp_mobile
from routes.api_web import api_bp_web
from routes.api_model import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp_mobile)
app.register_blueprint(api_bp_web)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5010)