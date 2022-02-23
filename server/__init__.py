from flask import Flask
from server import hotspot, rover, ui
import os

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

    app.register_blueprint(hotspot.bp)
    app.register_blueprint(rover.bp)
    app.register_blueprint(ui.bp)

    return app