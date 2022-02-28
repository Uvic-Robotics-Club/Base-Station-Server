from flask import Flask
import os
from server import api_hotspot, api_rover, api_joystick, connection

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ros-base-station-server.sqlite')
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ping page.
    @app.route('/')
    def root():
        return {'status': 'success', 'message': 'Base station server is alive'}

    app.register_blueprint(connection.bp)
    app.register_blueprint(api_hotspot.bp)
    app.register_blueprint(api_rover.bp)
    app.register_blueprint(api_joystick.bp)

    return app