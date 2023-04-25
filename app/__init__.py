from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )

    from . import db
    db.init_app(app)

    from . import cgna_database 

    app.register_blueprint(cgna_database.bp)

    return app

