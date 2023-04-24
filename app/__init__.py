from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
    )

    from .import cgna_database 

    app.register_blueprint(cgna_database.bp)

    return app

