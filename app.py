from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/vet_app"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models.vet import Vet
from models.animal import Animal
from models.owner import Owner
from models.treatment import Treatment
from models.appointment import Appointment

from controllers.vets_controller import vets_blueprint
app.register_blueprint(vets_blueprint)

from controllers.animals_controller import animals_blueprint
app.register_blueprint(animals_blueprint)

from controllers.owners_controller import owners_blueprint
app.register_blueprint(owners_blueprint)

from controllers.treatments_controller import treatments_blueprint
app.register_blueprint(treatments_blueprint)

from controllers.home_controller import home_blueprint
app.register_blueprint(home_blueprint)

from controllers.appointments_controller import appointments_blueprint
app.register_blueprint(appointments_blueprint)