from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/vet_app"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models.vet import Vet
from models.animal import Animal
from models.owner import Owner

from controllers.vets_controller import vets_blueprint
app.register_blueprint(vets_blueprint)

from controllers.animals_controller import animals_blueprint
app.register_blueprint(animals_blueprint)

from controllers.owners_controller import owners_blueprint
app.register_blueprint(owners_blueprint)

from controllers.home_controller import home_blueprint
app.register_blueprint(home_blueprint)