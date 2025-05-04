from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click


db = SQLAlchemy()
ma = Marshmallow()



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foods.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from calorieTracker.routes import bp
    app.register_blueprint(bp)

    @app.cli.command("create-db")
    @with_appcontext
    def create_db():
        db.create_all()
        click.echo("database created.")

    if __name__ == "__main__":
        app.run(debug=True)

    return app













