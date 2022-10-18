from flask import Flask, render_template
import socket
import os
from PyAccessPoint import pyaccesspoint

#   First use: make wireless hotspot
access_point = pyaccesspoint.AccessPoint(wlan='wlan1', ssid='Janus')
access_point.start()
access_point.is_running()
# access_point.stop()

#   Serves the web-interface
def create_app (test_config=None):
    app = Flask(__name__, template_folder='web', instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass


    @app.route("/")
    def home_page():
        return render_template('index.html')

    @app.route("/its_ip")
    def its_ip():
        return socket.gethostbyname(socket.gethostname())

    from . import db
    db.init_app(app)

    return app

#   "Lib": Functions that controls the GPIO

#   Handler between Client and GPIO

#   Slave mode (comunicates to another janus controller)
