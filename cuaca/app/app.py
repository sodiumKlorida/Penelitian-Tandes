# from flask import Flask, render_template
# # from BMKG import get_cuaca

# app = Flask(__name__)

# # call html
# @app.route("/")
# def home():
#     # cuaca = get_cuaca()
#     return render_template("dashboard.html")

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template
from routes.BMKG import bmkg_bp
from routes.AQICN import aqicn_bp

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

# daftar blueprint
app.register_blueprint(bmkg_bp)
app.register_blueprint(aqicn_bp)

if __name__ == "__main__":
    app.run(debug=True)
