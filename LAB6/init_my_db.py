from models.database import db


def init_database(app):
    with app.app_context():
        db.create_all()
    return app
