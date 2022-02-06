from flask import Flask
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

    # A simple page that says hello
    @app.route('/')
    def root():
        return 'Hello, World!2'

    from server import hotspot
    app.register_blueprint(hotspot.bp)

    return app