from flask import Flask
from models.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/scooterdb'
    db.init_app(app)
    migrate = Migrate(app, db)

    SWAGGER_URL = '/apidocs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Electro-Scooter API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)
    return app


if __name__ == '__main__':
    app = create_app()
    # app = init_database(app)
    import routes
    app.run()
