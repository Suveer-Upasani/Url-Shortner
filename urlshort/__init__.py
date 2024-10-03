from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'S1v2u3e4e5r6'  # Set your secret key

    # Import and register the blueprint
    from . import urlshort  
    app.register_blueprint(urlshort.bp)

    return app
