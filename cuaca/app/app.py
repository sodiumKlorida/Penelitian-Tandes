from flask import Flask

from routes.BMKG import bmkg_bp
from routes.AQICN import aqicn_bp
from routes.DASHBOARD import dashboard_bp

app = Flask(__name__)

# daftar blueprint
# api bmkg
app.register_blueprint(bmkg_bp)
# api bmkg

#api aqicn
app.register_blueprint(aqicn_bp)
#api aqicn

#dashboard
app.register_blueprint(dashboard_bp)
#dashboard

if __name__ == "__main__":
    app.run(debug=True)

